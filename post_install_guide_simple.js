#!/usr/bin/env node

/**
 * DNASPEC Quick Setup Guide - Post-installation Introduction
 * Shows brief overview and usage instructions after npm install
 */

function showQuickGuide() {
    console.log('');
    console.log('🧬 DNASPEC v1.0.37 - DNA Specification Context System');
    console.log('=' .repeat(60));
    console.log('');

    console.log('📖 QUICK OVERVIEW:');
    console.log('   Professional context engineering toolkit for AI-assisted development');
    console.log('   Enhances your AI interaction with advanced analysis and optimization');
    console.log('');

    console.log('🚀 GETTING STARTED:');
    console.log('   dnaspec init           # Initialize and setup');
    console.log('   dnaspec validate       # Verify installation');
    console.log('   dnaspec deploy         # Deploy to AI platforms');
    console.log('   dnaspec list           # Show available skills');
    console.log('');

    console.log('💡 EXAMPLE USAGE:');
    console.log('   In Claude/Gemini/Qwen: ');
    console.log('   /speckit.dnaspec.context-analysis "Analyze this code..."');
    console.log('   /speckit.dnaspec.architect "Design system for..."');
    console.log('');

    console.log('🔗 INTEGRATION:');
    console.log('   • Stigmergy: npm install -g stigmergy && stigmergy setup');
    console.log('   • Then run: dnaspec integrate --stigmergy');
    console.log('   • Supports: Claude, Gemini, Qwen, iFlow, CodeBuddy, Copilot');
    console.log('');

    console.log('📚 MORE INFO:');
    console.log('   dnaspec help           # Show detailed help');
    console.log('   dnaspec guide          # Full installation guide');
    console.log('   https://github.com/ptreezh/dnaSpec');
    console.log('');

    console.log('✅ Installation completed successfully!');
    console.log('   Ready to enhance your AI development experience');
}

// Check if this is a postinstall scenario (no arguments)
const isPostInstall = process.argv.length === 2 ||
                     (process.argv.length === 3 && process.argv[2] === 'postinstall');

if (isPostInstall) {
    showQuickGuide();
} else {
    // Full guide mode - call the original post_install_guide.js
    try {
        require('./post_install_guide.js');
    } catch (error) {
        console.error('Error loading full guide:', error.message);
        showQuickGuide();
    }
}

module.exports = { showQuickGuide };