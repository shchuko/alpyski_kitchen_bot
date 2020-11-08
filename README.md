# A bot helps you not to forget clean the kitchen!

It's an open-source part of bot sources used as submodule of the private repo with access token
 
Based on [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI#pytelegrambotapi)

# Dependicies: 

* pyTelegramBotAPI

* requests

* PySocks

* gunicorn

* urllib3

* preprocessing

* datetime 


#### "botconfig.py" file configuration example

```py
# /src/botconfig.py example
import preprocessing


main_config = {
    'token' : 'your_bot_token',
    'chat_id' : '-1001412969097'
    }
```

