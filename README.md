# 🎮 Azərbaycan Oyun Botu

Tam Azərbaycan dilində **18 oyunlu** Telegram qrup botu!
✍️ Oyunların çoxunda **özünüz yazırsınız** — buton yox!

## 🎯 Oyunlar

| # | Oyun | Necə oynanır | Tur/Xal |
|---|------|-------------|---------|
| 1 | 🎯 Söz İzahı | İzahı oxu → *yaz* | 10 tur, +10/sual |
| 2 | 📝 Boşluq Doldurma | Cümləni tamamla → *yaz* | 10 tur, +10/sual |
| 3 | 🔄 Söz Sarmalı | 5 hərf Wordle → *yaz* | 6 cəhd, +15-90 |
| 4 | ⚡ Sürətli Riyaziyyat | Cavabı → *yaz* | Sonsuz seriya |
| 5 | 🎲 Rəqəm Tapmaca | 1-100 → *yaz* | 7 cəhd |
| 6 | ❓ Tap Görəlim | Doğru/Yanlış → düymə | 10 tur |
| 7 | 🧠 Bilik Oyunu | Cavabı → *yaz* | 10 tur, +10/sual |
| 8 | 🚩 Bayraq Oyunu | Ölkəni → *yaz* | 10 tur, +10/sual |
| 9 | 🔗 Söz Zənciri | Söz → *yaz* | Sonsuz, +5/söz |
| 10 | 🏛 Paytaxt Tapmaca | 2 mod → *yaz* | 10 tur, +10/sual |
| 11 | 🚗 Plaka Oyunu | 2 mod → *yaz* | 10 tur, +10/sual |
| 12 | π Pi Oyunu | Rəqəmi → *yaz* | Sonsuz, +5/rəqəm |
| 13 | ⭕ XOX | 2 nəfər → düymə | +25 qalib |
| 14 | 🎭 Doğru/Cəsarət | Seç → düymə | — |
| 15 | 🎮 Buton Oyunu | Yaşıl düymə → tez bas | 8 raund |
| 16 | ⚡ Yaddaş Şimşəyi | Emoji ardıcıllığı → düymə | Sonsuz |
| 17 | 🌡 İsti Soyuq | 1-50 → *yaz* | Sonsuz |
| 18 | 📚 Əsər-Müəllif | Müəllifi → *yaz* | 10 tur, +10/sual |

## 🚀 Qurulum

### 1. Bot yaradın
```
@BotFather → /newbot → TOKEN alın
```

### 2. Lokal işə salmaq
```bash
git clone https://github.com/USERNAME/azerbaycan-oyun-botu.git
cd azerbaycan-oyun-botu
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # TOKEN-i yazın
python bot.py
```

### 3. Heroku Deploy
```bash
heroku create sizin-bot-adi
heroku config:set BOT_TOKEN=your_token
heroku config:set OWNER_LINK=https://t.me/username
heroku config:set CHANNEL_LINK=https://t.me/channel
heroku config:set BOT_USERNAME=bot_username
git push heroku main
heroku ps:scale worker=1
```

## ⚙️ Heroku Config Vars

| Dəyişən | Nümunə |
|---------|--------|
| `BOT_TOKEN` | `123456:ABC...` |
| `OWNER_LINK` | `https://t.me/username` |
| `CHANNEL_LINK` | `https://t.me/channel` |
| `BOT_USERNAME` | `my_game_bot` |

## 🤖 Komandalar
| Komanda | İzah |
|---------|------|
| `/start` | Botu başlat |
| `/menu` | Oyun menyusu (qrupda) |
| `/xal` | Xalınıza baxın |
| `/dur` | Oyunu dayandır |
