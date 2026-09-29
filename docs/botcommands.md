# MeshMapper Bot Commands

The MeshMapper Discord bot responds to commands starting with `!` and to questions when it's tagged. You can use a command, or ask in natural language and the bot will work out what you mean.

For example, both of these work:

- `!settings YOW`
- `@MeshMapper what are the settings for YOW?`

---

## Command Reference

| Command | Description |
| --- | --- |
| `!help` | Displays a help message with information about the bot and some available commands. |
| `!status {IATA}` | Displays the status of a region (you can also use its name). For pending regions, shows MQTT verification status. For active/inactive regions, shows data point, repeater, and observer counts. |
| `!settings {IATA}` | Displays the region's settings: max wardriving sessions, flood traffic, enforce hybrid mode, min active/hybrid interval, stale repeater age, new repeaters enter pending, duplicate ID detection, failed DISC as DROP, hop bytes, and RX channels. |
| `!admins {IATA}` | Lists the administrators for a region. For contact details, use **Region Info** on the region's map. |
| `!bug {description}` | Submits a bug report to GitHub. Can also reply to a message to use its content as the description. The bot first asks you to confirm (react ✅) after checking the [Troubleshooting](troubleshooting.md) page. The confirmation times out after 2 minutes. The bot uses AI to generate a concise title. Rate limited to 5 per user per hour. |
| `!issue {description}` | Alias for `!bug`. |
| `!feature {description}` | Submits a feature request to GitHub. Works like `!bug` but creates a feature request instead (no confirmation step). |
| `!resetpassword` | Points you to **Forgot password** on the MeshMapper portal. If you use Discord sign-in, no password is needed. The bot does not reset passwords or send credentials. |
| `!myissues` | Lists up to 15 of your bug reports and feature requests submitted through the bot, with their status. Issues submitted through the website form aren't included. |

!!! note "Additional Commands"
    Additional commands are available for users with the Developers or Moderator roles. These commands are not listed here.

## General Questions

In addition to commands, you can tag the bot with any question about MeshMapper and it will answer using its knowledge of the [MeshMapper Wiki](https://wiki.meshmapper.net). For example:

- `@MeshMapper how do I set up an MQTT observer?`
- `@MeshMapper what is hybrid mode?`
- `@MeshMapper how do multi-byte repeaters work?`

The bot can also be messaged directly (DM) without needing to tag it.

The bot's wiki knowledge refreshes automatically (it re-reads the wiki every 4 hours), so recently updated documentation makes its way into answers without any manual step.

## Commenting on Issues

After submitting a bug report or feature request, anyone can add comments to the GitHub issue by replying to the bot's message that contains the issue link. The bot will automatically add your reply as a comment on the corresponding GitHub issue, with a link back to your Discord message. A ✅ reaction confirms the comment was added; ❌ means it failed.

It works in the other direction too: when your issue is commented on, labelled or closed on GitHub, the bot posts an update back into the original Discord thread — so you'll see progress on your report without leaving Discord.

## Notes

- Commands starting with `!` work without tagging the bot. Natural-language requests and general questions need the bot to be tagged, except in DMs.
- When submitting bugs or features by replying to a message, the "Submitted by" field credits the original poster, not the person who tagged the bot.
- Replying to a bug or feature request does not require tagging the bot.
