import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.events import GiftEvent, ConnectEvent
from openai import OpenAI
from gtts import gTTS

# OpenAI API anahtarın
client_openai = OpenAI(api_key="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")

# TikTok kullanıcı adın
TIKTOK_HANDLE = "bilgiyapayy"

client_tiktok: TikTokLiveClient = TikTokLiveClient(unique_id=TIKTOK_HANDLE)

@client_tiktok.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"[*] Başarıyla canlı yayına bağlanıldı: @{client_tiktok.unique_id}")

@client_tiktok.on(GiftEvent)
async def on_gift(event: GiftEvent):
    if event.gift.streakable and event.gift.repeat_count > 1 and not event.gift.repeat_end:
        return

    user_name = event.user.nickname
    gift_name = event.gift.name
    print(f"\n[HEDIYE] {user_name}, {gift_name} attı! Tarot yorumu hazırlanıyor...")

    try:
        # 1. OpenAI'den Tarot Yorumu Al
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
        print(f"--- TAROT YORUMU ({user_name}) ---")
        print(tarot_yorumu)
        print("----------------------------------")

        # 2. Metni Sese Dönüştür (TTS)
        tts = gTTS(text=f"{user_name}, {gift_name} attığın için teşekkürler. İşte tarot falın: {tarot_yorumu}", lang='tr', slow=False)
        ses_dosyasi = "fal.mp3"
        tts.save(ses_dosyasi)
        print(f"[SES] Ses dosyası oluşturuldu: {ses_dosyasi}")
        
    except Exception as e:
        print(f"[HATA] Bir sorun oluştu: {e}")

if __name__ == '__main__':
    try:
        client_tiktok.run()
    except Exception as e:
        print(f"[KRITIK HATA]: {e}")
