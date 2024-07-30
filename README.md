<h2>Telegram auto posting cryptocurrency from CoinMarketCap websoket</h2>
<p align="center">
    <a href="https://www.python.org/downloads/">
        <img src="https://img.shields.io/badge/python-3.11%2B-blue.svg?style=flat-square&logo=python&logoColor=white&color=blue" alt="python 3.11">
    </a>
    <a href="https://github.com/zdky/telegram_crypto_currency/issues">
        <img src="https://img.shields.io/github/issues/zdky/telegram_crypto_currency?style=flat-square" alt="open issues">
    </a>
    <a href="https://github.com/zdky/telegram_crypto_currency/issues?q=is%3Aissue+is%3Aclosed">
        <img src="https://img.shields.io/github/issues-closed/zdky/telegram_crypto_currency?style=flat-square" alt="closed issues">
    </a>
    <a href="https://t.me/Zhidky" target="_blank">
        <img src="https://img.shields.io/badge/Telegram-Join-Blue.svg?style=flat-square&logo=telegram&logoColor=white&color=blue" alt="Telegram">
    </a>
    <a href="https://www.donationalerts.com/r/zhidky" target="_blank">
        <img src="https://img.shields.io/badge/DonationAlerts-Thanks-blue.svg?style=flat-square&logo=paypal&logoColor=fff" alt="Support me">
    </a>
</p>

## Features ⚙️

* Edit a post in telegram channel every 5 seconds

## Getting Started 🚀

<details>
<summary>Expand to see guide for Linux (Ubuntu)</summary>

- **Step 1**: Clone the repository using command:

```bash
git clone https://github.com/zdky/telegram_crypto_currency.git
```

- **Step 2**: Open project folder:

```bash
cd tgbot
```

- **Step 0**: Edit app.py with your data:

```bash
tg_token = 'YOUR_TOKEN'
tg_public_id = 1382779547
tg_post_id = 12
```

- **Step 3**: Check your python version:

```bash
python3.11 --version
```

If your version is below 3.11, install python:

```bash
apt install software-properties-common -y
add-apt-repository "ppa:deadsnakes/ppa" -y
apt update && apt install python3.11 python3.11-venv
```

- **Step 4**: Create virtual environment:

```bash
python3.11 -m venv .
```

- **Step 5**: Run virtual environment:

```bash
source bin/activate
```

- **Step 6**: Install requirements:

```bash
pip install -r requirements.txt
```

- **Step 7**: Grant rights:

```bash
chmod +x app.py
```

- **Step 8**: Create service:

```bash
nano /etc/systemd/system/tgbot.service
```

- **Step 9**: Put in file tgbot.service:

```bash
[Unit]
Description=tg_bot
After=syslog.target
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/tgbot
ExecStart=/root/tgbot/bin/python3.11 /root/tgbot/app.py
RestartSec=5
Restart=always

[Install]
WantedBy=multi-user.target
```

Save and exit:

```bash
CTRL+O > Enter > CTRL+X
```

- **Step 10**: Start service:

```bash
systemctl enable tgbot.service
systemctl start tgbot.service
```

</details>
<br>
<details>
<summary>Expand to see guide for debug on Linux (Ubuntu)</summary>

- **Debug**: Check status service:

```bash
systemctl status tgbot
```

- **Debug**: Check program logs:

```bash
journalctl -u tgbot.service
```

- **Debug**: Reload service:

```bash
systemctl reload-or-restart tgbot.service
```

- **Stop program**:

```bash
systemctl stop tgbot.service
```
</details>

### Reporting Bugs 🕵

If you've found something that doesn't work as it should, or would like to suggest a new feature, then go ahead and raise a ticket on GitHub.
For bugs, please outline the steps needed to reproduce, and include relevant info like system info and resulting logs.

[![Raise an Issue](https://img.shields.io/badge/Raise_an_Issue-GitHub-%23060606?style=for-the-badge&logo=github&logoColor=fff)](https://github.com/zdky/telegram_crypto_currency/issues/)

## License

> _**[zdky/telegram_crypto_currency](https://github.com/zdky/telegram_crypto_currency)** is licensed under [MIT](https://github.com/zdky/telegram_crypto_currency/blob/main/LICENSE) © [zdky](https://t.me/Zhidky) 2024._<br>
> <sup align="right">For information, see <a href="https://tldrlegal.com/license/mit-license">TLDR Legal > MIT</a></sup>
