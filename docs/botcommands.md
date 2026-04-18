# MeshMapper Bot Commands

The MeshMapper Discord bot responds to commands when tagged in a message. Commands can be issued using the `!` prefix or by asking in natural language — the bot will detect your intent automatically.

For example, both of these work:

- `@MeshMapper !settings YOW`
- `@MeshMapper what are the settings for YOW?`

---

## Command Reference

| Command | Description |
| --- | --- |
| `!help` | Displays a help message with information about the bot and some available commands. |
| `!status {IATA}` | Displays the status of a region. For pending regions, shows MQTT verification status. For active/inactive regions, shows data point, repeater, and observer counts. |
| `!settings {IATA}` | Displays the region's configuration settings including hop bytes, flood traffic, hybrid mode, stale repeater age, duplicate ID detection, and RX channels. |
| `!admins {IATA}` | Lists the administrators for a region along with their contact information. |
| `!bug {description}` | Submits a bug report to GitHub. Can also reply to a message to use its content as the description. The bot uses AI to generate a concise title. Rate limited to 5 per user per hour. |
| `!issue {description}` | Alias for `!bug`. |
| `!feature {description}` | Submits a feature request to GitHub. Works the same as `!bug` but creates a feature request instead. |
| `!resetpassword` | Resets your own admin password if your Discord name matches an account in the system. New credentials are sent via DM. |
| `!myissues` | Lists your open bug reports and feature requests that were submitted through the bot. |

!!! note "Additional Commands"
    Additional commands are available for users with the Developers or Moderator roles. These commands are not listed here.

## General Questions

In addition to commands, you can tag the bot with any question about MeshMapper and it will answer using its knowledge of the [MeshMapper Wiki](https://wiki.meshmapper.net). For example:

- `@MeshMapper how do I set up an MQTT observer?`
- `@MeshMapper what is hybrid mode?`
- `@MeshMapper how do multi-byte repeaters work?`

The bot can also be messaged directly (DM) without needing to tag it.

## Notes

- All commands require the bot to be tagged (e.g. `@MeshMapper !status YOW`), except in DMs where tagging is not required.
- When submitting bugs or features by replying to a message, the "Submitted by" field credits the original poster, not the person who tagged the bot.
