import pygame
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import ConnectEvent, Gift, User, GiftEvent
import concurrent.futures 
from helper import utils, config
import objs

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(config.MUSIC_SOUND_PATH) 
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(0.1)



# ===================================================
tiktokEvents:list[dict] = []


def game():
    global tiktokEvents
    
    scene = objs.Scene()
    
    bg = pygame.image.load(config.BG_TEMPLATE_PATH)
    bg = pygame.transform.scale(bg, (config.WIDTH, config.HEIGHT))
    
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

    running = True
    while running:
        
        if len(tiktokEvents) > 0:
            scene.update_gifters(tiktokEvents)
            tiktokEvents = []
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        screen.blit(bg, (0,0))
        scene.draw(screen)
        pygame.display.flip()

    pygame.quit()



# wwyrpick
tiktok_user ="@crece.sara.follo"
client: TikTokLiveClient = TikTokLiveClient(unique_id=tiktok_user)
print(f"Connecting to {tiktok_user}")


@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)

@client.on("gift")
async def on_gift(event:GiftEvent):
    global tiktokEvents
    
    # if event.gift.streakable and not event.gift.streaking:
        # print(f"{event.user.nickname} x{event.gift.count} {event.gift.info.name}")
        
    gift:Gift = event.gift
    user:User = event.user
    
    
    if gift.streakable and not gift.streaking:
        coins = gift.count * gift.info.diamond_count
        tiktokEvents.append(
            objs.Gifter.interface(
                id=user.user_id,
                name=user.nickname,
                total_dono=coins,
                pfp_url=user.avatar.url,
        ))
        
    elif not gift.streakable:
        coins = gift.info.diamond_count
        tiktokEvents.append(
            objs.Gifter.interface(
                id=user.user_id,
                name=user.nickname,
                total_dono=coins,
                pfp_url=user.avatar.url,
        ))
        
    print(len(tiktokEvents))
    


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor() as executor:
        game_future = executor.submit(game)
        client_future = executor.submit(client.run)
        
    # game()
    # client.run()
