import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import GiftEvent, ConnectEvent

# Buraya TikTok kullanıcı adını yaz (başında @ işareti olmadan)
TIKTOK_HANDLE = "kullanici_adin_buraya"

# İstemciyi (client) başlatıyoruz
client: TikTokLiveClient = TikTokLiveClient(unique_id=TIKTOK_HANDLE)

# Yayına bağlandığında çalışacak kısım
@client.on("connect")
async def on_connect(event: ConnectEvent):
    print(f"[*] Başarıyla canlı yayına bağlanıldı: @{client.unique_id}")

# Biri hediye (jeton) attığında çalışacak kısım
@client.on("gift")
async def on_gift(event: GiftEvent):
    # Sadece arka arkaya gelen hediyelerin ilkini veya tamamını yakalayabiliriz
    if event.gift.streakable and event.gift.repeat_count > 1:
        if event.gift.repeat_end:
            print(f"[HEDIYE] {event.user.nickname} ({event.user.unique_id}), {event.gift.repeat_count} adet {event.gift.name} attı!")
    else:
        print(f"[HEDIYE] {event.user.nickname} ({event.user.unique_id}), {event.gift.name} attı!")
        
        # BURAYA JETON ATILDIĞINDA YAPilACAKLAR GELECEK (Tarot yapay zekası vb.)
        # Örn: kullanıcının adını ve hediye bilgisini alıp tarot yorumlatacağız.

if __name__ == '__main__':
    # Botu çalıştır
    client.run()
