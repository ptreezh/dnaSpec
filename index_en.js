#!/usr/bin/env node

/**
 * DNA SPEC Context System (dnaspec) - npm installation entry point
 * Provides one-click installation and auto configuration functionality based on npm
 */

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

function runCommand(cmd, description) {
    console.log(`🔧 ${description}...`);
    try {
        const result = execSync(cmd, { encoding: 'utf-8', stdio: 'inherit' });
        console.log(`✅ ${description} succeeded\n`);
        return true;
    } catch (error) {
        console.error(`❌ ${description} failed:`);
        console.error(error.message);
        return false;
    }
}

function checkDependencies() {
    console.log('🔍 Checking dependencies...');

    // Check Python
    try {
        execSync('python --version', { stdio: 'pipe' });
        console.log('✅ Detected Python');
    } catch (error) {
        try {
            execSync('python3 --version', { stdio: 'pipe' });
            console.log('✅ Detected Python3');
        } catch (error2) {
            console.error('❌ Python or Python3 not found, please install Python 3.8+ first');
            return false;
        }
    }

    // Check Git
    try {
        execSync('git --version', { stdio: 'pipe' });
        console.log('✅ Detected Git');
    } catch (error) {
        console.error('❌ Git not found, please install Git');
        return false;
    }

    console.log('✅ Dependencies check passed\n');
    return true;
}

function installAndConfigure() {
    console.log('🚀 Starting DNA SPEC Context System (dnaspec) installation and configuration...\n');

    // Check dependencies
    if (!checkDependencies()) {
        process.exit(1);
    }

    // Get current working directory
    const initialDir = process.cwd();

    // Check if current directory is project directory (by checking key files)
    const isProjectDir = fs.existsSync('src') &&
                         fs.existsSync('pyproject.toml') &&
                         fs.existsSync('package.json');

    let projectDir = initialDir;

    if (!isProjectDir) {
        // If not in project directory, create temp directory and clone project
        const tempDir = 'dnaspec-install-tmp';

        // Create and enter temp directory
        if (!fs.existsSync(tempDir)) {
            fs.mkdirSync(tempDir);
        }
        process.chdir(tempDir);

        // Clone project
        const repoDir = 'dnaspec-context-engineering';
        if (fs.existsSync(repoDir) && fs.lstatSync(repoDir).isDirectory()) {
            console.log('🔄 Updating existing project...');
            process.chdir(repoDir);
        } else {
            console.log('📦 Cloning project...');
            if (!runCommand('git clone https://github.com/ptreezh/dnaSpec.git .', 'Clone project')) {
                process.chdir(initialDir);
                fs.rmSync(tempDir, { recursive: true, force: true });
                process.exit(1);
            }
        }

        projectDir = process.cwd(); // Update project directory to cloned directory
    } else {
        console.log('📋 Detected project directory...');
    }

    // Install Python package
    if (!runCommand('pip install -e .', 'Install DNASPEC package')) {
        // Try using python -m pip
        if (!runCommand('python -m pip install -e .', 'Install DNASPEC package (alternative method)')) {
            if (!runCommand('python3 -m pip install -e .', 'Install DNASPEC package (alternative method 2)')) {
                console.error('❌ All installation methods failed');
                if (!isProjectDir) {
                    process.chdir(initialDir);
                    const tempDir = path.join(initialDir, 'dnaspec-install-tmp');
                    if (fs.existsSync(tempDir)) {
                        fs.rmSync(tempDir, { recursive: true, force: true });
                    }
                }
                process.exit(1);
            }
        }
    }

    // Run auto configuration
    console.log('⚙️  Running auto configuration...');

    // Determine the full path of the configuration script
    const configScriptPath = path.join(projectDir, 'run_auto_config.py');
    console.log(`   Executing: python ${configScriptPath}`);

    const configProcess = spawn('python', [configScriptPath], {
        stdio: 'inherit',
        cwd: projectDir, // Make sure to run in project directory
        env: {
            ...process.env,
            PYTHONIOENCODING: 'utf-8',  // Set Python encoding to UTF-8 to avoid GBK errors
            LANG: 'en_US.UTF-8'         // Set language environment
        }
    });

    configProcess.on('close', (code) => {
        if (!isProjectDir) {
            // Cleanup temp directory if not original project directory
            process.chdir(initialDir);
            const tempDir = path.join(initialDir, 'dnaspec-install-tmp');
            if (fs.existsSync(tempDir)) {
                fs.rmSync(tempDir, { recursive: true, force: true });
            }
        }

        if (code === 0) {
            console.log('\n🎉 Installation and configuration completed successfully!');
            console.log('\nNow you can use the following commands in your AI CLI tools:');
            console.log('  /speckit.dnaspec.context-analysis [context] - Analyze context quality');
            console.log('  /speckit.dnaspec.context-optimization [context] - Optimize context');
            console.log('  /speckit.dnaspec.cognitive-template [task] - Apply cognitive template');
            console.log('  /speckit.dnaspec.architect [requirements] - System architecture design');
            console.log('  ...and other DNASPEC professional skills');
            console.log('\nWelcome to use dnaspec tool! You can run configuration again with `dnaspec` command.');
        } else {
            console.error(`\n❌ Configuration process failed, exit code: ${code}`);
            process.exit(1);
        }
    });

    configProcess.on('error', (err) => {
        if (!isProjectDir) {
            // Cleanup temp directory if not original project directory
            process.chdir(initialDir);
            const tempDir = path.join(initialDir, 'dnaspec-install-tmp');
            if (fs.existsSync(tempDir)) {
                fs.rmSync(tempDir, { recursive: true, force: true });
            }
        }

        console.error(`\n❌ Error running configuration: ${err.message}`);
        process.exit(1);
    });
}

// Run installation and configuration
installAndConfigure();