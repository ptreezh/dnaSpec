// test/command-handler.test.js
const { CommandHandler } = require('../lib/command-handler');

describe('Command Handler', () => {
  let commandHandler;

  beforeEach(() => {
    commandHandler = new CommandHandler();
  });

  test('should handle valid architect command', async () => {
    const result = await commandHandler.handleCommand('/speckit.dsgs.architect "Design a system"');
    expect(result.success).toBe(true);
    expect(result.skill).toBe('architect');
    expect(result.result).toContain('Designed system architecture for: "Design a system"');
  });

  test('should handle valid agent-creator command', async () => {
    const result = await commandHandler.handleCommand('/speckit.dsgs.agent-creator "Create an agent"');
    expect(result.success).toBe(true);
    expect(result.skill).toBe('agent-creator');
    expect(result.result).toContain('Created intelligent agent for: "Create an agent"');
  });

  test('should reject invalid command format', async () => {
    const result = await commandHandler.handleCommand('/invalid.command');
    expect(result.success).toBe(false);
    expect(result.error).toBe('Invalid command prefix');
  });

  test('should list available skills', () => {
    const skills = commandHandler.getAvailableSkills();
    expect(skills).toContain('architect');
    expect(skills).toContain('agent-creator');
    expect(skills).toContain('task-decomposer');
  });
});