#!/usr/bin/env node

const { Command } = require('commander');
const { CommandHandler } = require('../lib/command-handler');
const { SkillExecutor } = require('../lib/skill-executor');
const packageJson = require('../package.json');

const program = new Command();
const skillExecutor = new SkillExecutor();
const commandHandler = new CommandHandler(skillExecutor);

program
  .name('dsgs-spec-kit')
  .description('DSGS Skills for spec.kit integration')
  .version(packageJson.version);

program
  .command('init')
  .description('Initialize DSGS spec.kit integration')
  .option('-a, --auto', 'Automatic configuration')
  .option('-i, --interactive', 'Interactive configuration wizard')
  .action((options) => {
    console.log('Initializing DSGS spec.kit integration...');
    if (options.auto) {
      console.log('Running automatic configuration...');
    } else if (options.interactive) {
      console.log('Starting interactive configuration wizard...');
    } else {
      console.log('Please specify configuration mode:');
      console.log('  --auto for automatic configuration');
      console.log('  --interactive for interactive wizard');
    }
  });

program
  .command('integrate')
  .description('Integrate with AI CLI tools')
  .option('-d, --detect', 'Detect installed AI CLI tools')
  .action((options) => {
    console.log('Integrating with AI CLI tools...');
    if (options.detect) {
      console.log('Detecting installed AI CLI tools...');
    }
  });

program
  .command('exec')
  .description('Execute a DSGS skill command')
  .argument('<command>', 'The command to execute')
  .action(async (command) => {
    try {
      const result = await commandHandler.handleCommand(command);
      if (result.success) {
        console.log('Result:', result.result);
      } else {
        console.error('Error:', result.error);
      }
    } catch (error) {
      console.error('Execution failed:', error.message);
    }
  });

program
  .command('list')
  .description('List available skills')
  .action(() => {
    console.log('Available DSGS Skills:');
    const commands = commandHandler.getAvailableCommands();
    commands.forEach(cmd => console.log(`  ${cmd}`));
  });

program.parse();