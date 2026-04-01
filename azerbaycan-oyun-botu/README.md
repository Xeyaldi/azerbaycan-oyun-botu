# 🎮 Azərbaycan Oyun Botu

Azərbaycan dilində tam işləyən Telegram oyun botu!

## 🎯 Oyunlar

| Oyun | Açıqlama | Xal |
|------|----------|-----|
| 🎯 Söz İzahı | İzahdan sözü tap | 10-30 xal |
| 📝 Boşluq Doldurma | Cümləni tamamla | 10 xal |
| 🧠 Bilik Oyunu | Trivia sualları | 10-35 xal (seriya bonusu) |
| ⭕ XOX | Tic-Tac-Toe bota qarşı | 20 xal (qazansanız) |
| 🚩 Bayraq Oyunu | Bayrağa görə ölkəni tap | 10 xal |
| 🏛 Paytaxt Tapmaca | Ölkəyə görə paytaxtı tap | 10 xal |
| 🔗 Söz Zənciri | Sözlər zənciri qur | 5 xal/söz |

## 🚀 Qurulum

### 1. BotFather ilə bot yaradın
1. Telegram-da [@BotFather](https://t.me/BotFather) tapın
2. `/newbot` yazın
3. Bot adını və username-ini daxil edin
4. Sizə verilən **BOT_TOKEN**-i saxlayın

### 2. Kodu yükləyin
```bash
git clone https://github.com/SIZIN_USERNAME/azerbaycan-oyun-botu.git
cd azerbaycan-oyun-botu
```

### 3. Lokal işə salmaq
```bash
# Virtual environment yaradın
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Asılılıqları yükləyin
pip install -r requirements.txt

# .env faylı yaradın
cp .env.example .env
# .env faylında BOT_TOKEN-i yazın

# Botu işə salın
python bot.py
```

### 4. Heroku-ya Deploy

#### Heroku CLI ilə:
```bash
# Heroku-ya login olun
heroku login

# Yeni app yaradın
heroku create sizin-bot-adi

# BOT_TOKEN əlavə edin
heroku config:set BOT_TOKEN=your_token_here

# Deploy edin
git add .
git commit -m "Initial deploy"
git push heroku main

# Worker dyno-nu işə salın
heroku ps:scale worker=1
```

#### Heroku Dashboard ilə:
1. [heroku.com](https://heroku.com) saytına daxil olun
2. "New App" yaradın
3. GitHub repo-nuzla bağlayın
4. **Settings → Config Vars** bölməsindən `BOT_TOKEN` əlavə edin
5. **Resources** bölməsindən `worker` dyno-nu aktivləşdirin

## 📁 Fayl Strukturu
```
azerbaycan-oyun-botu/
├── bot.py                    # Ana bot faylı
├── games/
│   ├── __init__.py
│   ├── base_game.py          # Əsas oyun sinifi
│   ├── soz_izahi.py          # Söz İzahı
│   ├── bosluq_doldurma.py    # Boşluq Doldurma
│   ├── bilgi_oyunu.py        # Bilik Oyunu
│   ├── xox.py                # XOX
│   ├── bayraq_oyunu.py       # Bayraq Oyunu
│   ├── paytaxt_tapmaca.py    # Paytaxt Tapmaca
│   └── soz_zenciri.py        # Söz Zənciri
├── requirements.txt
├── Procfile                  # Heroku üçün
├── runtime.txt               # Python versiyası
├── .env.example
├── .gitignore
└── README.md
```

## 🤖 Bot Komandaları
- `/start` — Botu başlat
- `/menu` — Ana menü
- `/xal` — Xalınıza baxın
- `/dur` — Aktiv oyunu dayandır

## ➕ Yeni Oyun Əlavə Etmək
1. `games/` qovluğunda yeni fayl yaradın
2. `BaseGame` sinifini miras alın
3. `start_game()` və `handle_callback()` metodlarını implement edin
4. `bot.py`-dəki `GAMES` lüğətinə əlavə edin
5. Ana menüyə düymə əlavə edin

## 📝 Lisenziya
MIT License
