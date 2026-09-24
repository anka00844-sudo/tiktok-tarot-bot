import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import GiftEvent, ConnectEvent
from openai import OpenAI

# OpenAI API anahtarını buraya yapıştıracaksın (OpenAI hesabından alınıyor)
client_openai = OpenAI(api_key="BURAYA_OPENAI_API_KEY_YAZ")

# TikTok kullanıcı adın (başında @ olmadan)
TIKTOK_HANDLE = "kullanici_adin_buraya"

client_tiktok: TikTokLiveClient = TikTokLiveClient(unique_id=TIKTOK_HANDLE)

@client_tiktok.on("connect")
async def on_connect(event: ConnectEvent):
    print(f"[*] Başarıyla canlı yayına bağlanıldı: @{client_tiktok.unique_id}")

@client_tiktok.on("gift")
async def on_gift(event: GiftEvent):
    # Sadece tekli hediyeleri veya tekrar edenlerin bitişini yakalayalım ki üst üste tetiklenmesin
    if event.gift.streakable and event.gift.repeat_count > 1 and not event.gift.repeat_end:
        return

    user_name = event.user.nickname
    gift_name = event.gift.name
    print(f"[HEDIYE] {user_name}, {gift_name} attı! Tarot yorumu hazırlanıyor...")

    # Yapay zekaya tarot yorumu yaptırıyoruz
    try:
        response = client_openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Sen TikTok canlı yayınındaki mistik, gizemli ve eğlenceli bir tarot falcısısın. Sana ismi ve attığı jeton söylenen kişiye rastgele bir tarot kartı çekerek 2-3 cümlelik çok kısa, heyecan verici ve mistik bir gelecek yorumu yap."
                },
                {
                    "role": "user",
                    "content": f"Kullanıcı adı: {user_name}, Attığı hediye: {gift_name}"
                }
            ],
            max_tokens=150
        )
        
        tarot_yorumu = response.choices[0].message.content
        print(f"\n--- TAROT YORUMU ({user_name}) ---")
        print(tarot_yorumu)
        print("----------------------------------\n")

        # BURAYA SESLENDİRME (TTS) KODLARI GELECEK
        
    except Exception as e:
        print(f"[HATA] Yapay zekâ yorum yaparken hata oluştu: {e}")

if __name__ == '__main__':
    client_tiktok.run()
