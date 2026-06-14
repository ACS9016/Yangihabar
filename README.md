# 🤖 Qamashi Kanal Boti

Qamashi tumani haqida yangiliklarni **avtomatik** topib, AI yordamida boyitib, Telegram kanalga **kuniga 5 ta** post tashlaydi.

## ⚙️ Sozlash (bir marta qilinadi)

### 1. Telegram Bot yaratish
1. Telegramda **@BotFather** ga boring
2. `/newbot` yozing
3. Bot nomini bering (masalan: `QamashiNewsBot`)
4. **Token** ni saqlang: `7123456789:AAFxxxx...`

### 2. Botni kanalga qo'shish
1. Kanalingizga kiring → **Adminlar** → **Admin qo'shish**
2. Botingiz nomini qidiring va **admin qiling**
3. Kerakli huquqlar: **Xabar yuborish** ✅

### 3. Channel ID olish
- Kanal `@username` bo'lsa: `@qamashi_yangiliklar`
- Yoki @userinfobot orqali raqamli ID oling: `-1001234567890`

### 4. API kalitlarini olish

**Anthropic (Claude AI):**
- https://console.anthropic.com → API Keys → Create Key

**Serper (Google Search) — BEPUL 2500/oy:**
- https://serper.dev → Sign up → Dashboard → API Key

### 5. Railway'ga deploy qilish

1. **GitHub**ga yuklang:
   ```bash
   git init
   git add .
   git commit -m "Qamashi bot"
   git push
   ```

2. **railway.app** ga kiring → New Project → Deploy from GitHub

3. **Environment Variables** qo'shing:
   ```
   TELEGRAM_TOKEN   = 7123456789:AAFxxxx...
   CHANNEL_ID       = @sizning_kanalingiz
   ANTHROPIC_API_KEY = sk-ant-xxxx...
   SERPER_API_KEY   = xxxx...
   ```

4. Deploy tugagach bot 24/7 ishlaydi! ✅

## 🕐 Post jadvali (Toshkent vaqti)
| Vaqt | Til |
|------|-----|
| 08:00 | O'zbekcha |
| 11:00 | Ruscha |
| 14:00 | O'zbekcha |
| 17:00 | Ruscha |
| 20:00 | O'zbekcha |

## 📁 Fayllar
```
qamashi_bot/
├── bot.py          # Asosiy kod
├── requirements.txt
├── Procfile
├── railway.toml
└── README.md
```

## 💰 Narx
| Xizmat | Bepul limit | Oylik narx |
|--------|-------------|------------|
| Railway | $5 kredit/oy | Bepul yetadi |
| Anthropic | Yo'q | ~$1-3/oy |
| Serper | 2500 so'rov/oy | Bepul yetadi |

**Jami: ~$1-3/oy** ✅
