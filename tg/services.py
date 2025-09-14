import os
import requests

TG_BASE = "https://api.telegram.org/bot{token}/{method}"


def tg_get_updates():
    token = os.getenv("TG_TOKEN", "")
    if not token:
        raise RuntimeError("TG_TOKEN is empty")
    url = TG_BASE.format(token=token, method="getUpdates")
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data}")
    return data


def send_telegram_message(chat_id: int | str, text: str):
    token = os.getenv("TG_TOKEN", "")
    if not token:
        raise RuntimeError("TG_TOKEN is empty")
    url = TG_BASE.format(token=token, method="sendMessage")
    r = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=10)
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data}")
    return data
