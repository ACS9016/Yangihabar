import asyncio
import random
import logging
from datetime import datetime
import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = "8733785603:AAFuV0MXZnB7tCmF_iz7iOaSjB3UgtoUAFU"
CHANNEL_ID = "@dasturmax"
ANTHROPIC_API_KEY = "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"
SERPER_API_KEY = "c1d470e67764e69e88681325739a647d54885617"

SEARCH_QUERIES = [
    "Qamashi tumani yangiliklari",
    "Qamashi Qashqadaryo yangilik",
    "Qamashi district news Uzbekistan",
    "Қамаши тумани янгиликлар",
    "Qamashi iqtisodiyot infratuzilma",
    "Qamashi qishloq xo'jaligi",
]

POST_TIMES = ["08:00", "11:00", "14:00", "17:00", "20:00"]


async def search_news(query: str) -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                "https://google.serper.dev/news",
                headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
                json={"q": query, "num": 5, "hl": "uz", "gl": "uz"},
            )
            data = resp.json()
            return data.get("news", [])
    except Exception as e:
        logger.error(f"Qidiruv xatosi: {e}")
        return []


async def generate_post(news_items: list[dict], language: str) -> str:
    if news_items:
        news_text = "\n".join(
            [f"- {item.get('title', '')} ({item.get('source', '')}): {item.get('snippet', '')}"
             for item in news_items[:3]]
        )
        prompt = f"""Quyidagi Qamashi tumani haqidagi yangiliklar asosida Telegram kanal uchun {'o\'zbekcha' if language == 'uz' else 'ruscha'} post yoz.

Yangiliklar:
{news_text}

Talablar:
- 150-250 so'z
- Telegram formatida (emoji, paragraflar)
- Sarlavha bo'lsin (emoji bilan)
- Oxirida #Qamashi #{'Yangiliklar' if language == 'uz' else 'Новости'} hashtaglar
- Jonli, qiziqarli til
- Faqat postning o'zini yoz, boshqa narsa yozma"""
    else:
        topics_uz = [
            "Qamashi tumanining tarixi va madaniyati",
            "Qamashi tabiatining go'zalligi",
            "Qamashi dehqonchilik an'analari",
            "Qamashi yoshlarining yutuqlari",
            "Qamashi infratuzilmasi rivojlanishi",
        ]
        topics_ru = [
            "История и культура Камашинского района",
            "Красота природы Камаши",
            "Сельскохозяйственные традиции Камаши",
            "Достижения молодёжи Камаши",
            "Развитие инфраструктуры Камаши",
        ]
        topic = random.choice(topics_uz if language == "uz" else topics_ru)
        prompt = f"""Qamashi tumani (Qashqadaryo viloyati, O'zbekiston) haqida "{topic}" mavzusida Telegram kanal uchun {'o\'zbekcha' if language == 'uz' else 'ruscha'} post yoz.

Talablar:
- 150-250 so'z
- Telegram formatida (emoji, paragraflar)
- Sarlavha bo'lsin (emoji bilan)
- Oxirida #Qamashi hashtaglar
- Jonli, qiziqarli, ma'lumotli til
- Faqat postning o'zini yoz"""

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-6",
                    "max_tokens": 1000,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            data = resp.json()
            return data["content"][0]["text"]
    except Exception as e:
        logger.error(f"AI xatosi: {e}")
        return ""


async def send_post():
    logger.info("Post tayyorlanmoqda...")
    hour = datetime.now().hour
    language = "uz" if hour % 2 == 0 else "ru"
    query = random.choice(SEARCH_QUERIES)
    news_items = await search_news(query)
    logger.info(f"Topilgan yangiliklar: {len(news_items)} ta | Til: {language}")
    post_text = await generate_post(news_items, language)
    if not post_text:
        logger.warning("Post yaratilmadi, o'tkazib yuborildi")
        return
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=CHANNEL_ID, text=post_text, parse_mode="HTML")
        logger.info("✅ Post muvaffaqiyatli yuborildi!")
    except Exception as e:
        logger.error(f"Yuborish xatosi: {e}")
        try:
            bot = Bot(token=TELEGRAM_TOKEN)
            await bot.send_message(chat_id=CHANNEL_ID, text=post_text)
            logger.info("✅ Post (plain text) yuborildi!")
        except Exception as e2:
            logger.error(f"Ikkinchi urinish ham xato: {e2}")


async def main():
    logger.info("🤖 Qamashi Bot ishga tushdi!")
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
    for time_str in POST_TIMES:
        hour, minute = map(int, time_str.split(":"))
        scheduler.add_job(send_post, "cron", hour=hour, minute=minute)
        logger.info(f"📅 Post rejasi: {time_str}")
    scheduler.start()
    logger.info("✅ Scheduler ishga tushdi. Bot kutmoqda...")
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
