#!/usr/bin/env node

/**
 * DNA SPEC Context System (dnaspec) - npm installation entry point
 * Provides one-click installation and auto-configuration based on npm
 */

const { execSync, spawn, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function runCommand(cmd, description) {
    console.log(`[SETUP] ${description}...`);
    try {
        const result = execSync(cmd, { encoding: 'utf-8', stdio: 'inherit' });
        console.log(`[SUCCESS] ${description} completed\n`);
        return true;
    } catch (error) {
        console.error(`[ERROR] ${description} failed:`);
        console.error(error.message);
        return false;
    }
}

function checkDependencies() {
    console.log('[CHECK] Checking dependencies...');

    // Check Python
    try {
        execSync('python --version', { stdio: 'pipe' });
        console.log('[OK] Python detected');
    } catch (error) {
        try {
            execSync('python3 --version', { stdio: 'pipe' });
            console.log('[OK] Python3 detected');
        } catch (error2) {
            console.error('[ERROR] Python or Python3 not found, please install Python 3.8+');
            return false;
        }
    }

    // Check Git
    try {
        execSync('git --version', { stdio: 'pipe' });
        console.log('[OK] Git detected');
    } catch (error) {
        console.error('[ERROR] Git not found, please install Git');
        return false;
    }

    console.log('[SUCCESS] All dependencies passed\n');
    return true;
}

function runQueryCommand(command, pythonScript, description) {
    // For query commands, run installed Python packages directly
    console.log(`[QUERY] Processing ${command} command...`);

    // Check dependencies
    if (!checkDependencies()) {
        process.exit(1);
    }

    // Run Python script directly using installed modules
    const commandProcess = spawn('python', ['-c', `
import subprocess
import sys
import os

# Use correct module path with working directory setup
command_result = subprocess.run([
    sys.executable,
    '-c',
    '''
import sys
import os
# Add current directory and src to Python path
sys.path.insert(0, ".")
sys.path.insert(0, os.path.join(os.getcwd(), "src"))
# Import and run the correct module
from dna_spec_kit_integration.cli import main
sys.argv = ["dnaspec", "${command}"]
main()
'''
], capture_output=False, text=True, env=os.environ.copy())

sys.exit(command_result.returncode)
    `], {
        stdio: 'inherit',
        env: {
            ...process.env,
            PYTHONIOENCODING: 'utf-8',
            LANG: 'en_US.UTF-8'
        }
    });

    commandProcess.on('close', (code) => {
        if (code === 0) {
            console.log(`[SUCCESS] ${command} command executed successfully!`);
        } else {
            // If direct call fails, try using standalone_cli
            console.log(`[FALLBACK] Trying alternative method for ${command}...`);

            const fallbackProcess = spawn('python', ['-c', `
import sys
import os
sys.path.insert(0, ".")
sys.path.insert(0, os.path.join(os.getcwd(), "src"))
from dna_spec_kit_integration.cli import main
sys.argv = ["dnaspec", "${command}"]
try:
    main()
except SystemExit:
    pass
          `], {
                stdio: 'inherit',
                env: {
                    ...process.env,
                    PYTHONIOENCODING: 'utf-8',
                    LANG: 'en_US.UTF-8'
                }
            });

            fallbackProcess.on('close', (fallbackCode) => {
                if (fallbackCode === 0) {
                    console.log(`[SUCCESS] ${command} command executed successfully!`);
                } else {
                    console.error(`[ERROR] ${command} command execution failed, exit code: ${fallbackCode}`);
                    process.exit(fallbackCode);
                }
            });
        }
    });

    commandProcess.on('error', (err) => {
        console.error(`[ERROR] Error running ${command} command: ${err.message}`);
        process.exit(1);
    });
}

function installAndConfigure() {
    const command = determineCommand();

    // Get current working directory (declare once)
    const initialDir = process.cwd();

    // Check if current directory is project directory (by checking key files)
    const isProjectDir = fs.existsSync('src') &&
                         fs.existsSync('pyproject.toml') &&
                         fs.existsSync('package.json');

    // For query commands (no installation needed), use installed modules directly
    const queryCommands = ['list', 'validate', '--list', '--version', 'help'];
    const shouldRunFullInstall = !queryCommands.includes(command);

    let projectDir = initialDir;
    let pythonScript;
    let description;

    switch (command) {
        // Ensure init command runs complete initialization with secure workflow
        case 'init':
            description = 'Complete DNASPEC Initialization with Secure Workflow';
            pythonScript = 'init_dnaspec_complete.py';
            break;

        case 'deploy':
            // Deploy command also needs full installation
            description = 'Deployment and Integration';
            pythonScript = 'deploy_cli.py';
            break;

        case 'integrate':
            // Integration command also needs full installation
            description = 'Platform Integration';
            pythonScript = 'run_auto_config.py';
            break;

        case 'list':
        case 'validate':
            // Query commands: use installed packages
            description = `Query: ${command}`;
            console.log(`[QUERY] Processing ${command} command...`);
            return runQueryCommand(command, 'auto_configurator.py', description);

        case '--version':
            // Run installed modules directly, no installation
            description = 'Version Check';
            console.log('[QUERY] Processing version command...');
            return runQueryCommand(command, 'auto_configurator.py', description);

        default:
            // Other commands: execute full installation process
            description = 'Configuration';
            pythonScript = 'run_auto_config.py';
            break;
    }

    // Check dependencies
    if (!checkDependencies()) {
        console.error('[ERROR] Required dependencies not found');
        process.exit(1);
    }

    // If not in project directory, create temp directory and clone project
    if (!isProjectDir && shouldRunFullInstall) {
        // Create and enter temp directory
        const tempDir = 'dnaspec-install-tmp';
        if (fs.existsSync(tempDir)) {
            fs.rmSync(tempDir, { recursive: true, force: true });
        }
        fs.mkdirSync(tempDir);
        process.chdir(tempDir);

        // Clone project - add multiple sources and retry mechanism
        console.log('[SETUP] Cloning project...');
        const gitUrls = [
            'https://github.com/ptreezh/dnaSpec.git',
            'https://gitclone.com/github.com/ptreezh/dnaSpec.git',
            'https://hub.fastgit.xyz/ptreezh/dnaSpec.git'
        ];

        let cloned = false;
        for (let i = 0; i < gitUrls.length; i++) {
            const url = gitUrls[i];
            console.log(`[ATTEMPT] Trying source ${i+1}/${gitUrls.length}: ${url}`);

            try {
                execSync(`git clone --depth 1 ${url}`, {
                    stdio: 'pipe',
                    timeout: 120000
                });
                console.log(`[SUCCESS] Source ${i+1} cloned successfully`);
                cloned = true;
                break;
            } catch (error) {
                console.log(`[FAILED] Source ${i+1} clone failed, trying next...`);
                if (i === gitUrls.length - 1) {
                    console.log(`[ERROR] Source ${i+1} clone error: ${error.message}, trying next...`);
                }
            }
        }

        if (!cloned) {
            console.error('[ERROR] All sources failed to clone project');
            process.exit(1);
        }

        process.chdir('dnaSpec');
        projectDir = process.cwd(); // Update project directory to cloned directory
    } else if (isProjectDir) {
        console.log('[SETUP] Detected already in project directory...');
    }

    // Install Python package
    if (!runCommand('pip install -e .', 'Install DNASPEC package')) {
        console.error('[ERROR] Failed to install DNASPEC package');
        if (!isProjectDir) {
            const tempDir = path.join(initialDir, 'dnaspec-install-tmp');
            process.chdir(initialDir);
            fs.rmSync(tempDir, { recursive: true, force: true });
        }
        process.exit(1);
    }

    console.log('[SUCCESS] DNASPEC package installed successfully\n');

    // Run configuration script
    if (pythonScript) {
        console.log(`[CONFIG] Running ${description}...`);
        console.log(`[EXEC] Executing: python ${pythonScript}`);

        const scriptPath = path.join(projectDir, pythonScript);
        const configProcess = spawn('python', [scriptPath], {
            stdio: 'inherit',
            env: {
                ...process.env,
                PYTHONIOENCODING: 'utf-8',
                LANG: 'en_US.UTF-8'
            }
        });

        configProcess.on('close', (code) => {
            // If not original project directory, clean temp directory
            if (!isProjectDir) {
                process.chdir(initialDir);
                const tempDir = path.join(initialDir, 'dnaspec-install-tmp');
                if (fs.existsSync(tempDir)) {
                    fs.rmSync(tempDir, { recursive: true, force: true });
                }
            }

            if (code === 0) {
                // Display English ANSI compatible output
                console.log('\n[COMPLETE] Installation and configuration completed successfully!');

                // Show post-installation guide
                console.log('\nDNASPEC Context Engineering Skills - POST-INSTALLATION GUIDE');
                console.log('='.repeat(80));
                console.log('');
                console.log('Thank you for installing DNASPEC (DNA SPEC Context System)!');
                console.log('');
                console.log('DNASPEC is a professional context engineering toolkit that enhances your AI-assisted');
                console.log('development experience by providing advanced context analysis, optimization,');
                console.log('and cognitive template application capabilities.');
                console.log('');
                console.log('KEY FEATURES:');
                console.log('  * Context Quality Analysis: 5-dimensional assessment (clarity, relevance,');
                console.log('                               completeness, consistency, efficiency)');
                console.log('  * Context Optimization: AI-driven improvements based on specific goals');
                console.log('  * Cognitive Templates: Professional thinking frameworks (CoT, Verification, etc.)');
                console.log('  * Agentic Design: System architecture and task decomposition skills');
                console.log('  * Safety Workflows: Secure AI interaction with temporary workspaces');
                console.log('  * Multi-Platform Support: Claude, Qwen, Gemini, Cursor, Copilot');
                console.log('');
                console.log('GETTING STARTED - Next Steps:');
                console.log('');
                console.log('  1. Run automatic validation:');
                console.log('     dnaspec validate');
                console.log('');
                console.log('  2. Deploy skills to AI platforms (if you have AI CLI tools installed):');
                console.log('     dnaspec deploy');
                console.log('');
                console.log('  3. View all available commands:');
                console.log('     dnaspec list');
                console.log('');
                console.log('USAGE EXAMPLES in AI CLI Tools:');
                console.log('  /speckit.dnaspec.context-analysis "Analyze this requirement: ..."');
                console.log('  /speckit.dnaspec.context-optimization "Optimize this context: ..."');
                console.log('  /speckit.dnaspec.cognitive-template "Apply template to: ..." template=verification');
                console.log('  /speckit.dnaspec.architect "Design system for: ..."');
                console.log('');
                console.log('COMMAND REFERENCE:');
                console.log('  dnaspec deploy            - Deploy skills to AI platforms');
                console.log('  dnaspec deploy --list     - List detected AI platforms');
                console.log('  dnaspec validate          - Check integration status');
                console.log('  dnaspec list              - Show all available skills');
                console.log('  dnaspec help              - Show help information');
                console.log('');
                console.log('For support, visit: https://github.com/ptreezh/dnaSpec');
                console.log('Report issues at: https://github.com/ptreezh/dnaSpec/issues');
            } else {
                console.error(`\n[ERROR] ${description} process failed, exit code: ${code}`);
                if (!isProjectDir) {
                    process.chdir(initialDir);
                    const tempDir = path.join(initialDir, 'dnaspec-install-tmp');
                    if (fs.existsSync(tempDir)) {
                        fs.rmSync(tempDir, { recursive: true, force: true });
                    }
                }
                process.exit(1);
            }
        });

        configProcess.on('error', (err) => {
            if (!isProjectDir) {
                // If not original project directory, clean temp directory
                process.chdir(initialDir);
                const tempDir = path.join(initialDir, 'dnaspec-install-tmp');
                if (fs.existsSync(tempDir)) {
                    fs.rmSync(tempDir, { recursive: true, force: true });
                }
            }

            console.error(`\n[ERROR] Error running ${description}: ${err.message}`);
            process.exit(1);
        });
    }
}

function determineCommand() {
    // Analyze command line arguments
    const args = process.argv.slice(2);
    if (args.length > 0) {
        return args[0].toLowerCase();
    }
    return 'init'; // Default command
}

// Run installation and configuration
installAndConfigure();