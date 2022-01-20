# Yandex.Prakticum telegram bot
This app helps to track the status of your review on the platform <br>
The is made on Python with a help of package [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
## How to use
### Localy
Clone repository to your local machine
```shell
$ git clone https://github.com/fibboo/ya.prakticum_telegram_bot.git
```
Install python environment, activate and install requirements
```shell
$ cd ya.prakticum_telegram_bot
$ python3 -m venv venv
$ . ./venv/bin/activate
$ pip install -r requirments.txt
```
Make .env out of .env.template and insert your credentials
```shell
$ cp .env.template .env
$ nano .env
```
Run
```shell
python homework.py
```
### Using Heroku
Fork repository to your GitHub account.
1. Login into your Heroku account
2. Go to apps page https://dashboard.heroku.com/apps
3. Create new app (button New → Create new app)
<img src="https://pictures.s3.yandex.net/resources/S1_26_1633890383.png">
4. Connect you GitHub account to app. Go to section **Deploy**, in **Deployment method** choose **GitHub** and push **Connect to GitHub**
<img src="https://pictures.s3.yandex.net/resources/S1_22_1633890417.png">
Authorize and choose forked repository.
5. Add environment variables to Heroku app.
You can do it manly in section **Settings → Config Vars**. Press **Reveal Config Vars**
Look for example in _.env.template_ file
<img src="https://pictures.s3.yandex.net/resources/S07_12_1635158106.png">
6. Go to **Resources** and activate worker
<img src="https://pictures.s3.yandex.net/resources/S1_28_1633891678.png">
