
import pygame
from helper import utils, config
from objs import basic



gifters_dataset:dict = utils.read_json(config.GIFTER_JSON_PATH)
MAX_RANKING_COUNT = 3

class Gifter:
    
    def __init__(self, ranking:int) -> None:
        self.ranking = ranking
        
        padding:int = int(config.WIDTH*0.05)
        size = int(config.WIDTH*0.2)
        coef:int = (ranking-(MAX_RANKING_COUNT-1))
        span = (size + padding) * coef
        print(size)
        x = int((config.WIDTH*0.5) + span) - size//2
        self.rect:pygame.Rect = pygame.Rect(x, int((config.HEIGHT*0.255)),  size , size) 
         
        self.name = basic.Text(f"#{ranking}", self.rect.center)
        self.pfp = basic.Image(config.DEFAULT_PFP_PATH, self.rect.center, self.rect.size)
    
    def __abv_name(self, name:str)->str:
        return f"{self.ranking}.{name[0:3]}-"

    def set_gifter(self, gifter_info:dict):
        pfp_path = basic.Image.download_img(gifter_info["pfp_url"], str(gifter_info["id"]))
        
        self.name = basic.Text(self.__abv_name(gifter_info["name"]), self.rect.center)
        self.pfp = basic.Image(pfp_path, self.rect.center, self.rect.size)

    def draw(self, screen:pygame.Surface):
        self.pfp.draw(screen)
        self.name.draw(screen)

    @staticmethod
    def interface(id:int, name:str, total_dono:int, pfp_url:str):
        return {
            "id":id,
            "name":name,
            "total_dono":total_dono,
            "pfp_url":pfp_url,
        }


class Scene:
    
    def __init__(self) -> None:
        self.gifter1 = Gifter(1)
        self.gifter2 = Gifter(2)
        self.gifter3 = Gifter(3)
        
        self.dono_sound = pygame.mixer.Sound(config.DONO_SOUND_PATH)
        
        
    def combine_gifters_data(new_gifters:list[dict]):
        global gifters_dataset
        
        for new_gifter in new_gifters:
            new_g = gifters_dataset.get(new_gifter["id"])
            new_gifter["total_coins"] = new_gifter["total_coins"] if not new_g else new_g["total_coins"] + new_gifter["total_coins"]
            gifters_dataset[new_gifter["id"]] = new_gifter

        utils.write_json(config.GIFTER_JSON_PATH, gifters_dataset)
            
        gifters_lst = list(gifters_dataset.values())
        sortedGifters = sorted(gifters_lst, key=lambda d: d['total_coins'], reverse=True) 
        return sortedGifters
        
    def update_gifters(self, new_gifters:list[dict]):
        sortedGifters = self.combine_gifters_data(new_gifters)

        if len(sortedGifters) >= 1: self.gifter1.set_gifter(sortedGifters[0])
        if len(sortedGifters) >= 2: self.gifter2.set_gifter(sortedGifters[1])
        if len(sortedGifters) >= 3: self.gifter3.set_gifter(sortedGifters[2])
        
        self.dono_sound.play()
        
        
        
        
    def draw(self, screen):
        self.gifter1.draw(screen)
        self.gifter2.draw(screen)
        self.gifter3.draw(screen)