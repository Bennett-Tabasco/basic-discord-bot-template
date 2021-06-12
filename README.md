# basic-discord-bot-template
This is just a template for a discord bot scripted in discord.py, feel free to make changes on your own.

My code is mostly based on Lucas's code so be sure to check him out in this link https://www.youtube.com/channel/UCR-zOCvDCayyYy1flR5qaAg


if you're about to download my project, just download everything, make sure that everything is in its place

if the bot sent duplicate messages or the command doesn't work after you commited changes even if your syntax is correct, just regenarate the token and run the bot with that new token

# features
Bot's features:
- Settings:
 change prefix command (syntax: `<prefix>prefixSet <new prefix>`)
 ping command (syntax: `<prefix>ping`) [shows bot's latency]
 clear command (syntax: `<prefix>clear <amount>`) [default amount is 5, also amount of delete message can't be greater than 150]

- Security:
You can specify a member by getting his/her id or ping them.
 ban command (syntax: `<prefix>ban <member> <reason>`)
 kick command (syntax: `<prefix>kick <member> <reason>`)
 unban command (syntax: `<prefix>unban <member>`)
 tempban command (syntax: `<prefix>tempban <member> <duration (valid units: 's': seconds, 'm': minutes, 'h': hours)>`)
 mute command (syntax: `<prefix>mute <member> <reason>`)
 unmute command (syntax: `<prefix>unmute <member>`)
 
- Voice:
+ coming soon!

- Side features:
Error handlers


# updates
update notes (9th june 2021 7:20PM):
- setting abnormal characters for the bot's prefix is not available anymore (more information: https://stackoverflow.com/questions/67888572/setting-valid-prefixes-for-the-discord-bot-in-discord-py/67891510#67891510), you can use the old version if you want (check settings.py)

update notes (8th june 2021 9:16PM):
- help commands has been moved to help_commands.py file
- ban, tempban, unban, kick, mute and unmute commands has been moved to security.py file

upadate notes (4th june 2021 6:02PM):
- added mute and unmute commands
- error handlers are now available (check settings.py file)
- fixed unban command
 
