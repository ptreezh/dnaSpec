const { exec } = require('child_process');

describe('CLI Tool', () => {
  test('should show version', (done) => {
    exec('node ./bin/cli.js --version', (error, stdout, stderr) => {
      expect(error).toBeNull();
      expect(stdout).toMatch(/\d+\.\d+\.\d+/);
      done();
    });
  });

  test('should show help', (done) => {
    exec('node ./bin/cli.js --help', (error, stdout, stderr) => {
      expect(error).toBeNull();
      expect(stdout).toContain('Usage:');
      expect(stdout).toContain('Commands:');
      done();
    });
  });

  test('should list skills', (done) => {
    exec('node ./bin/cli.js list', (error, stdout, stderr) => {
      expect(error).toBeNull();
      expect(stdout).toContain('Available DSGS Skills');
      expect(stdout).toContain('architect');
      expect(stdout).toContain('agent-creator');
      done();
    });
  });
});