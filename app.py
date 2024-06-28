import asyncio
import json
from datetime import datetime, timezone, timedelta
from textwrap import dedent

import websockets
import aiohttp

# айдишники брать из https://coinmarketcap.com/currencies/bitcoin/
# там слева блок(где цена), называется UCID
# названия токена сам пиши, они будут отображены в мсдж поста
CUR = {
    1: "BTC",
    5426: "SOL",
    11419: "TON",
    1027: "ETH",
    28850: "NOT",
    1839: "BNB"
}
# ссылки сам вбивай, иначе всё упадёт
LINKS = {
    "BTC": "https://coinmarketcap.com/currencies/bitcoin/",
    "SOL": "https://coinmarketcap.com/currencies/solana/",
    "TON": "https://coinmarketcap.com/currencies/toncoin/",
    "ETH": "https://coinmarketcap.com/currencies/ethereum/",
    "NOT": "https://coinmarketcap.com/currencies/notcoin/",
    "BNB": "https://coinmarketcap.com/currencies/bnb/"
}
# как часто обновлять инфу в посте (1, 5, 10 и т.д)
upd_every_s = 5 # сек
# добавляете своего бота в паблик с админ правами на редакт мсджей
# вставляем API Token своего бота:
tg_token = "YOUR_TOKEN"
# в тг включаем: Settings - Advanced - Experimental settings - Show Peer IDs in Profile
# открываем свой паблик там будет написан айди, вставляем сюда:
tg_public_id = 123456789
# написать пост, скопировать ссылку на пост, 
# вставить сюда и оставить её айди (шо на конце ссылки)
tg_post_id = 123

# не трогаем
tg_chat_id = int(f"-100{tg_public_id}")
tz = timezone(timedelta(hours=3))
old_msg = ""
# ----------

async def edit_tg_post(msg):
    if msg != old_msg: # если курс не изменился, не редачим
        msg += f"\n\n⏳ <b>Обновлено:</b> {datetime.now(tz).strftime('%H:%M:%S %d/%m (MSK)')}"
        msg += "\n\n<b><i><a href='https://github.com/zdky/telegram_crypto_currency/blob/main/app.py'>как это сделано?</a></i></b>"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'https://api.telegram.org/bot{tg_token}/editMessageText',
                    data={
                        'chat_id': tg_chat_id,
                        'message_id': tg_post_id,
                        'text': dedent(msg),
                        "disable_web_page_preview": True,
                        "disable_notification": True,
                        "parse_mode": "HTML"
                    }
                ) as response:
                    if response.status != 200:
                        print(f"[Telegram] Ошибка редакта поста: {await response.text()}")
        except Exception as error:
            print(f"[ERROR] in edit_tg_post(): {error}")


def generate_msg(prices):
    msg = ""
    for idx, currency in enumerate(CUR.values()):
        if currency in ["NOT"]: # для мелких токенов
            price = f"{prices[currency]:.4f}"
        else:
            price = f"{prices[currency]:.2f}"
        cur_name = f"<b><a href='{LINKS[currency]}'>{currency}</a>:</b>"
        if idx == len(CUR) - 1:
            part = f"┃{cur_name} {price} $"
        else:
            part = f"┃{cur_name} {price} $\n"
        msg += part
    return msg


async def parser_CMC_json(data, prices):
    global old_msg
    if 'd' in data and 'id' in data['d']:
        cur_id = data['d']['id']
        price = data['d']['p']
        if cur_id in CUR:
            prices[CUR[cur_id]] = price
            # Если собраны все данные для заданных валют, выводим их
            if all(currency in prices for currency in CUR.values()):
                msg = generate_msg(prices)
                await edit_tg_post(msg)
                old_msg = msg
                # Очищаем словарь, чтобы начать сбор данных заново
                prices = {}
    return prices


async def listen_CMC_websocket(websocket):
    prices = {}
    while True: # Получаем и выводим данные из вебсокета
        response = await websocket.recv()
        data = json.loads(response)
        prices = await parser_CMC_json(data, prices)


async def sub_CMC_websocket():
    uri = "wss://push.coinmarketcap.com/ws?device=web&client_source=coin_detail_page"
    currency_ids = ",".join(map(str, CUR.keys()))
    async with websockets.connect(uri) as websocket:
        # Cообщение для подписки на вебсокет CoinMarketCap
        subscription_message = json.dumps({
            "method": "RSUBSCRIPTION",
            "params": [f"main-site@crypto_price_{upd_every_s}s@{{}}@normal", currency_ids]
        })
        await websocket.send(subscription_message)
        print("Подписался на вебсокет.")
        await listen_CMC_websocket(websocket)


async def main():
    try:
        await sub_CMC_websocket()
    except Exception as error:
        print(f"[ERROR] Вебсокет упал: {error}")
        print(f"[*] сплю 30s и перезапуск..")
        await asyncio.sleep(30)
        await main()


if __name__ == "__main__":
    asyncio.run(main())


# Такие данные приходят из вебсокета
# в listen_CMC_websocket одновременно с разными ID токенами
# {
#     "d": {
#         "id": 1,
#         "p": 69268.43919068537,
#         "p24h": -0.250205416124,
#         "p7d": 2.256262525427,
#         "p30d": 12.942590034731,
#         "p3m": 1.52894509485,
#         "p1y": 161.775528523465,
#         "pytd": 63.83172595468,
#         "pall": 112024354.11419825,
#         "as": 19709721,
#         "mc": 1365261610553.87,
#         "fmc24hpc": -0.250205416124
#     },
#     "t": "1717893112058",
#     "c": "main-site@crypto_price_5s@1@normal"
# }
