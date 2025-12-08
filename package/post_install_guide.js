#!/usr/bin/env node

/**
 * DNASPEC Context Engineering Skills - Post-installation Guide
 * Provides post-installation verification and usage guide
 */
const { execSync, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function checkInstallation() {
    console.log('DNASPEC Context Engineering Skills - Post-installation Verification');
    console.log('=' * 70);
    console.log('');

    // Check if dnaspec command is available
    console.log('1. Verifying dnaspec command availability...');
    try {
        const result = execSync('dnaspec --version', { encoding: 'utf-8' });
        console.log('   [OK] dnaspec command accessible');
        console.log(`   Version: ${result.trim()}`);
    } catch (error) {
        console.log('   [FAIL] dnaspec command not found in PATH');
        console.log('   Please ensure npm global bin directory is in your PATH');
        return false;
    }

    // Check Python integration
    console.log('');
    console.log('2. Verifying Python integration...');
    try {
        const result = execSync('python -c "from src.dnaspec_context_engineering.skills_system_final import execute; print(\'DNASPEC Core Module OK\')"', { encoding: 'utf-8' });
        console.log('   [OK] Python integration working');
        console.log(`   Result: ${result.trim()}`);
    } catch (error) {
        console.log('   [FAIL] Python integration error');
        console.log('   Error:', error.message.substring(0, 100));
        return false;
    }

    // Check AI CLI tools detection
    console.log('');
    console.log('3. Verifying AI CLI tools detection...');
    try {
        const result = execSync('python -c "from src.dnaspec_spec_kit_integration.core.cli_detector import CliDetector; detector = CliDetector(); results = detector.detect_all(); print(dict((k, v.get(\'installed\', False)) for k, v in results.items()))"', { encoding: 'utf-8' });
        console.log('   [OK] CLI detection system working');
        console.log(`   Detected tools: ${result.trim()}`);
    } catch (error) {
        console.log('   [FAIL] CLI detection system error');
        console.log('   Error:', error.message.substring(0, 100));
        return false;
    }

    return true;
}

function showUsageGuide() {
    console.log('');
    console.log('DNASPEC Context Engineering Skills - Usage Guide');
    console.log('=' * 70);
    console.log('');
    console.log('Congratulations! DNASPEC has been successfully installed and configured.');
    console.log('');
    console.log('Available Commands in AI CLI Tools:');
    console.log('  /speckit.dnaspec.context-analysis [context]    # Analyze context quality');
    console.log('  /speckit.dnaspec.context-optimization [context] # Optimize context');
    console.log('  /speckit.dnaspec.cognitive-template [task]      # Apply cognitive template');
    console.log('  /speckit.dnaspec.architect [requirements]       # System architecture design');
    console.log('  /speckit.dnaspec.agent-creator [spec]           # Create AI agent');
    console.log('  /speckit.dnaspec.task-decomposer [task]         # Decompose complex tasks');
    console.log('  /speckit.dnaspec.constraint-generator [reqs]    # Generate system constraints');
    console.log('  /speckit.dnaspec.modulizer [system]             # System modularization');
    console.log('  /speckit.dnaspec.dapi-checker [api]             # API interface validation');
    console.log('');
    console.log('Quick Start Examples:');
    console.log('  1. Context Analysis:');
    console.log('     /speckit.dnaspec.context-analysis "Design a user authentication system"');
    console.log('');
    console.log('  2. Context Optimization:');
    console.log('     /speckit.dnaspec.context-optimization "Create a web app"');
    console.log('');
    console.log('  3. Cognitive Template Application:');
    console.log('     /speckit.dnaspec.cognitive-template "How to optimize database queries" template=verification');
    console.log('');
    console.log('  4. System Architecture Design:');
    console.log('     /speckit.dnaspec.architect "Build an e-commerce platform"');
    console.log('');
    console.log('Advanced Features:');
    console.log('  - Agentic Design: Create specialized AI agents for specific tasks');
    console.log('  - Context Engineering: Professional context analysis and optimization');
    console.log('  - Cognitive Templates: Apply professional thinking frameworks');
    console.log('  - Safety Workflows: Protected AI interaction with temporary workspaces');
    console.log('');
    console.log('Troubleshooting:');
    console.log('  If AI CLI tools don\'t recognize DNASPEC commands:');
    console.log('    1. Wait a few minutes for AI tool to refresh tools list');
    console.log('    2. Restart your AI CLI client');
    console.log('    3. Run: dnaspec init (to re-run auto-configuration)');
    console.log('');
    console.log('Need help?');
    console.log('  - Visit: https://github.com/ptreezh/dnaSpec');
    console.log('  - Run: dnaspec help');
    console.log('  - Contact: 3061176@qq.com');
    console.log('');
    console.log('Happy Coding with DNASPEC Context Engineering Skills!');
}

function main() {
    console.log('Checking DNASPEC installation status...');
    
    const installationOk = checkInstallation();
    
    if (installationOk) {
        console.log('');
        console.log('[SUCCESS] DNASPEC installation verified successfully!');
        console.log('');
        showUsageGuide();
    } else {
        console.log('');
        console.log('[FAILURE] DNASPEC installation has issues.');
        console.log('Please reinstall using: npm install -g dnaspec');
    }
}

// Run the verification
main();