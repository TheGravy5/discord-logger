# Basic message deleting and image logging bot
This bot logs messages within a single server.
To set up, copy the files to a directory on your computer or server, then:
1. Create files `ids.txt` and `token.txt` within the directory.
2. Go to https://discord.com/developers/applications and create a bot.
3. Disable "allow anyone to invite this bot", as it won't work for them. Only allow `Guild install` on `Installation` tab and set default invite to `None`.
4. On the `Bot` tab, enable `Message Content` intent.
5. On the `OAuth` tab, select `bot` and then the permissions `Send Messages`, `Attach Files`, `Read Message History`, and `View Channels`. Open the link to invite the bot to your server.
6. Insert into `token.txt` your bot token
7. Insert into `ids.txt` two lines with the following:
```
Any number or a channel from your server (this is the channel used for logging; if not valid, messages won't be logged until step 4)
Your server ID
```
9. Run `bot.py` to run the bot.
8. Use /set to set or change the channel used for logging.
