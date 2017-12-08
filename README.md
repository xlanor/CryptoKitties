# Meow

A telegram bot to scan CryptoKitties API to report on kittens with a certain desirable trait.

Will clean up more when Im free and add more options to customize the parameters.

Please take note that this was a customized bot for my colleagues, I didn't expect to receive so much traffic on it.

Feel free to take it, modify the code, run it as your own instance, improve it, bla bla.

Thanks to [Python-Telegram-Bot](https://github.com/python-telegram-bot/python-telegram-bot).

## Requirements

* Python3
* ImageMagick
* Python Telegram Bot
* wand
* PyMySQL
* web3py (You can do manual calculation for all wei->usd instead and not use this)

## Sample Output
<img src="/github_images/catscreen.png" width="300">


## General Setup guide
* Install dependencies
* Setup a mysql db (reccomend you use Cryptokitties as the title)
* put your creds in tokens file.
* Put your bot api in the tokens file as well.
* Create a telegram channel to use for error messages (two if you want to broadcast to a channel) and place the IDs of the channel in tokens file accordingly.
* I'll be removing channel broadcast soon since that's mainly hardcoded for my colleagues
* Comment out the job repeating in cryptokitties.py (the one with a value of 300)
* Run createdb.py
* rename tokens-sample.py to tokens.py
* Replace filepaths in both modules.
* go to your bot and do a /register, register yourself. (Reccomend not using a gigantic offset value)
* Run the bot.

* .service file is included for users on systems that use systemd, modify it accordingly. 

## Licensing

Licensed under the MIT license. Do whatever you want to do with it.
