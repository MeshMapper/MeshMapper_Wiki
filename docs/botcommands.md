# MeshMapper Bot Commands

The MeshMapper Discord bot responds to commands when tagged in a message. Commands can be issued using the `!` prefix or by asking in natural language — the bot will detect your intent automatically.

For example, both of these work:

- `@MeshMapper !settings YOW`
- `@MeshMapper what are the settings for YOW?`

---

## Command Reference

| Command | Who Can Use | Description |
| --- | --- | --- |
| `!status {IATA}` | Everyone | Displays the status of a region. For pending regions, shows MQTT verification status. For active/inactive regions, shows data point, repeater, and observer counts. |
| `!settings {IATA}` | Everyone | Displays the region's configuration settings including hop bytes, flood traffic, hybrid mode, stale repeater age, duplicate ID detection, and RX channels. |
| `!admins {IATA}` | Everyone | Lists the administrators for a region along with their contact information. |
| `!bug {description}` | Everyone | Submits a bug report to GitHub. Can also reply to a message to use its content as the description. The bot uses AI to generate a concise title. Rate limited to 5 per user per hour (Developers and Moderators are exempt). |
| `!issue {description}` | Everyone | Alias for `!bug`. |
| `!feature {description}` | Everyone | Submits a feature request to GitHub. Works the same as `!bug` but creates a feature request instead. |
| `!resetpassword` | Everyone (self-service) | Resets your own admin password if your Discord name matches an account in the system. New credentials are sent via DM. Developers and Moderators can also reply to another user's message to reset their password. |
| `!createadmin {IATA}` | Developers, Moderators | Creates a new regional admin account. Must be used as a reply to the target user's message. If the user already has an account, the region is added to their existing account. Credentials are sent to the target user via DM. |
| `!remember {text}` | Developers, Moderators | Adds a fact to the bot's knowledge base. Can also reply to a message to remember its content. |
| `!forget {text}` | Developers, Moderators | Removes any remembered facts that match the provided text. |
| `!recall` | Developers, Moderators | Lists all remembered facts currently stored in the bot's memory. |
| `!delete {number}` | Developers, Moderators | Deletes a specific remembered fact by its number (use `!recall` to see the list). |
| `!refresh` | Developers, Moderators | Forces a rebuild of the bot's wiki knowledge base. |
| `!syncup` | Developers, Moderators | Pushes all locally stored remembered facts to the web admin panel. |

## General Questions

In addition to commands, you can tag the bot with any question about MeshMapper and it will answer using its knowledge of the [MeshMapper Wiki](https://wiki.meshmapper.net). For example:

- `@MeshMapper how do I set up an MQTT observer?`
- `@MeshMapper what is hybrid mode?`
- `@MeshMapper how do multi-byte repeaters work?`

The bot can also be messaged directly (DM) without needing to tag it.

## Notes

- All commands require the bot to be tagged (e.g. `@MeshMapper !status YOW`), except in DMs where tagging is not required.
- When submitting bugs or features by replying to a message, the "Submitted by" field credits the original poster, not the person who tagged the bot.
- The `!createadmin` and `!resetpassword` commands send credentials via DM. If the target user has DMs disabled, the bot will notify the channel that the DM could not be delivered.
