const { execFile } = require('node:child_process');
const { promisify } = require('node:util');

const execFileAsync = promisify(execFile);

/**
 * Runs the actual Hermes newsletter skill instead of duplicating its prompt here.
 * This makes Promptfoo a regression harness around the real workflow.
 */
module.exports = class HermesNewsletterProvider {
  constructor(options = {}) {
    this.config = options.config || {};
    this.providerId = options.id || 'hermes:weekly-ai-management-digest';
  }

  id() {
    return this.providerId;
  }

  async callApi(prompt) {
    const skill = this.config.skill || 'weekly-ai-management-digest';
    const timeout = Number(this.config.timeoutMs || 540000);
    const hermes = process.env.HERMES_BIN || 'hermes';
    const args = ['--skills', skill, 'chat', '--quiet', '--query', prompt];

    try {
      const { stdout, stderr } = await execFileAsync(hermes, args, {
        timeout,
        maxBuffer: 10 * 1024 * 1024,
        env: process.env,
      });
      const output = stdout.trim();
      if (!output) {
        return { error: `Hermes returned no text. stderr: ${stderr.trim()}` };
      }
      return {
        output,
        prompt,
        metadata: { skill, stderr: stderr.trim() || undefined },
      };
    } catch (error) {
      return {
        error: `Hermes newsletter workflow failed: ${error.message}`,
        metadata: { skill, code: error.code, signal: error.signal },
      };
    }
  }
};
