# Terms of Service — plugin-pilot

**Last updated:** April 4, 2026
**Version:** 1.0

## 1. Acceptance of Terms

By installing, enabling, or using the plugin-pilot plugin ("the Plugin"), you agree to be bound by these Terms of Service ("Terms"), the [Privacy Policy](PRIVACY.md), and the [Third-Party Plugin Disclaimer](DISCLAIMER.md). If you do not agree to these Terms, do not use the Plugin.

## 2. Description of Service

Plugin Pilot is an AI-driven plugin lifecycle manager for Claude Code that:
- Analyzes your current task context to suggest relevant plugins
- Searches configured marketplaces and GitHub for available plugins
- Tracks plugin usage locally to suggest cleanup of unused plugins
- Manages plugin installation and removal with user confirmation

## 3. Eligibility

You must be at least 13 years of age to use this Plugin. If you are under 18, you represent that your parent or legal guardian has reviewed and agreed to these Terms. The Plugin is not directed at children under 13 and does not knowingly collect data from children under 13 in compliance with COPPA (Children's Online Privacy Protection Act).

## 4. User Responsibilities

By using the Plugin, you agree to:

a) **Review before installing** — Examine the source code, documentation, and license of any plugin before authorizing installation, especially community plugins from GitHub.

b) **Maintain your credentials** — Ensure your GitHub token (used for community search) is kept secure. The Plugin accesses it through the locally configured `gh` CLI and does not store it separately.

c) **Comply with third-party terms** — When installing plugins that interact with third-party services (Steam, GitHub, Slack, etc.), comply with those services' terms of use.

d) **Report issues responsibly** — Report bugs, security vulnerabilities, or concerns through the GitHub issue tracker.

## 5. Intellectual Property

a) The Plugin is licensed under the [MIT License](LICENSE). You may use, modify, and distribute it under those terms.

b) Plugin names, logos, and trademarks mentioned in the catalog belong to their respective owners. Plugin Pilot does not claim ownership of any third-party plugin or service.

c) "Claude Code" and "Anthropic" are trademarks of Anthropic, PBC. Plugin Pilot is not affiliated with, endorsed by, or sponsored by Anthropic.

## 6. Token Usage and Costs

a) **Increased token consumption** — Plugin Pilot uses AI agents to analyze your project context, search for plugins, and generate recommendations. This **significantly increases token usage** compared to standard Claude Code operation. By using Plugin Pilot, you acknowledge and accept this increased consumption.

b) **Background agents** — Plugin Pilot may launch background agents (stack-scout, plugin-resolver) that consume tokens independently of your main conversation. These agents perform GitHub API searches, repository analysis, and plugin verification.

c) **Third-party API costs** — Some plugins discovered by Plugin Pilot may require paid third-party API keys (e.g., Gemini API for image generation). Plugin Pilot will note these costs when suggesting such plugins, but you are solely responsible for any charges incurred.

d) **No token guarantees** — Plugin Pilot does not guarantee or limit the number of tokens consumed per session. Token usage depends on project complexity, number of plugins analyzed, and frequency of checks.

e) **Third-party AI services** — Some plugins and stacks discovered by Plugin Pilot integrate with third-party AI models and services (e.g., Google Gemini, OpenAI, Stability AI, Replicate, and others). **Neither Plugin Pilot, Anthropic, nor any other party provides free access to these third-party AI services.** You are solely responsible for:
   - Obtaining your own API keys and accounts for any third-party AI service
   - Understanding and accepting the terms of service of each third-party AI provider
   - Paying all costs associated with third-party AI API usage
   - Ensuring your use complies with the third-party provider's acceptable use policies

Plugin Pilot will note when a suggested plugin requires third-party AI services, but cannot guarantee the accuracy or completeness of cost estimates.

## 7. Third-Party Plugins

a) **Official marketplace plugins** have undergone Anthropic's review process. Plugin Pilot surfaces these but is not responsible for their content or behavior.

b) **Community plugins** (from GitHub or unofficial marketplaces) are NOT reviewed by Plugin Pilot authors or Anthropic. See [DISCLAIMER.md](DISCLAIMER.md) for the full liability waiver.

c) **License compatibility** — Plugin Pilot will warn you about plugins with restrictive licenses (GPL, AGPL), missing licenses, or license incompatibilities. It is your responsibility to ensure compliance with all applicable licenses.

d) **Auto-updates** — Plugins may be updated by their authors at any time. Plugin Pilot does not control when or how plugins are updated. An update may introduce breaking changes, new permissions, or altered behavior. Plugin Pilot is not responsible for any consequences of plugin updates.

## 8. Limitation of Liability

TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW:

a) THE PLUGIN IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

b) IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE PLUGIN OR THE USE OR OTHER DEALINGS IN THE PLUGIN.

c) THIS INCLUDES BUT IS NOT LIMITED TO: DATA LOSS, SYSTEM DAMAGE, SECURITY BREACHES, FINANCIAL LOSS, OR ANY OTHER HARM RESULTING FROM:
   - Installation or use of any plugin suggested by Plugin Pilot
   - Errors, bugs, or malfunctions in Plugin Pilot or any third-party plugin
   - Unauthorized access to your system through a third-party plugin
   - Plugin conflicts, incompatibilities, or breaking updates

## 9. Indemnification

You agree to indemnify, defend, and hold harmless the Plugin authors from and against any claims, damages, losses, liabilities, costs, and expenses (including reasonable attorneys' fees) arising from:

a) Your use of the Plugin
b) Your installation or use of any third-party plugin
c) Your violation of these Terms
d) Your violation of any third-party rights or applicable laws

## 10. Data and Privacy

a) All data is stored locally on your device. See [PRIVACY.md](PRIVACY.md) for details.

b) **Right to deletion** — You may delete all Plugin Pilot data at any time by running `/plugin-pilot:pilot reset` or manually deleting the `data/` directory within the plugin installation path.

c) **GitHub API usage** — Community search uses the GitHub REST API, subject to [GitHub's Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) and [API rate limits](https://docs.github.com/en/rest/rate-limit). The Plugin uses your existing `gh` CLI authentication and does not create additional GitHub sessions.

## 11. Trust Score

The "trust score" is an automated structural assessment and NOT:
- A security audit
- An endorsement of safety
- A guarantee of quality
- A substitute for manual code review

A high trust score means the plugin has proper file structure, not that it is safe to use.

## 12. Modifications

The authors reserve the right to modify these Terms at any time. Material changes will be reflected in the "Last updated" date and version number. Continued use of the Plugin after changes constitutes acceptance of the modified Terms.

## 13. Termination

You may stop using the Plugin at any time by uninstalling it. The authors may discontinue the Plugin at any time without notice.

## 14. Governing Law

These Terms shall be governed by and construed in accordance with applicable international open-source software conventions. Any disputes shall be resolved through good-faith communication via the project's GitHub issue tracker before pursuing other remedies.

## 15. Severability

If any provision of these Terms is found to be unenforceable, the remaining provisions shall continue in full force and effect.

## 16. Entire Agreement

These Terms, together with the Privacy Policy and Third-Party Plugin Disclaimer, constitute the entire agreement between you and the Plugin authors regarding the use of the Plugin.

## Contact

For questions about these Terms, open an issue at https://github.com/wion4/plugin-pilot/issues or contact wion4@vk.com.
