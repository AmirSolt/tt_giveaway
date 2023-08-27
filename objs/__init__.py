
import pygame
from helper import utils, config
from objs import basic


MAX_RANKING_COUNT = 3

class Gifter:
    
    def __init__(self, ranking:int) -> None:
        self.ranking = ranking
        
        padding:int = int(config.WIDTH*0.07)
        mult = 1+((MAX_RANKING_COUNT-ranking)*0.1)
        size = int(config.WIDTH*0.2)*mult
        coef:int = (ranking-(MAX_RANKING_COUNT-1))
        span = size + padding
        x = int((config.WIDTH*0.5) + span*coef) - size//2
        y = int(config.HEIGHT*0.36) - size
        self.rect:pygame.Rect = pygame.Rect(x, y,  size , size) 
         
        self.name_center = (self.rect.center[0],self.rect.center[1]+span*0.65)
        self.name = basic.Text(f"#{ranking}", self.name_center, bg_color=None)
        self.pfp = basic.Pic(config.DEFAULT_PFP_PATH, self.rect.center, self.rect.size)
    
    def __abv_name(self, name:str, total_dono:int)->str:
        short_name = name[0:6]
        if len(short_name)<len(name):
            short_name += ".."
        return f"{self.ranking}.{short_name}\nCoins: {total_dono}"

    def set_gifter(self, gifter_info:dict):
        pfp_path = config.CACHED_IMGS_PATH + str(gifter_info["id"]) + ".png"
        if not utils.does_file_exist(pfp_path):
            pfp_path = config.CACHED_IMGS_PATH + str(gifter_info["id"]) + ".jpg"
            pfp_path = basic.Pic.download_img(gifter_info["pfp_url"], pfp_path)
            pfp_path = basic.Pic.make_rounded(pfp_path)
    
        self.name = basic.Text(self.__abv_name(gifter_info["name"], gifter_info["total_dono"]), self.name_center)
        self.pfp = basic.Pic(pfp_path, self.rect.center, self.rect.size)

    def draw(self, screen:pygame.Surface):
        self.pfp.draw_with_circle_border(screen)
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
        
        self.gifters_dataset:dict = utils.read_json(config.GIFTER_JSON_PATH)
        self.dono_sound = pygame.mixer.Sound(config.DONO_SOUND_PATH)
        
        self.update_gifters([])
        
    def combine_gifters_data(self, new_gifters:list[dict]):
        
        for new_gifter in new_gifters:
            new_g = self.gifters_dataset.get(str(new_gifter["id"]))
            new_gifter["total_dono"] = new_gifter["total_dono"] if not new_g else new_g["total_dono"] + new_gifter["total_dono"]
            self.gifters_dataset[str(new_gifter["id"])] = new_gifter

        utils.write_json(config.GIFTER_JSON_PATH, self.gifters_dataset)
            
        gifters_lst = list(self.gifters_dataset.values())
        sortedGifters = sorted(gifters_lst, key=lambda d: d['total_dono'], reverse=True) 
        return sortedGifters
        
    def update_gifters(self, new_gifters:list[dict]):
        sortedGifters = self.combine_gifters_data(new_gifters)

        if len(sortedGifters) >= 1: self.gifter1.set_gifter(sortedGifters[0])
        if len(sortedGifters) >= 2: self.gifter2.set_gifter(sortedGifters[1])
        if len(sortedGifters) >= 3: self.gifter3.set_gifter(sortedGifters[2])
        
        if len(new_gifters) > 0:
            self.dono_sound.play()
        
        
        
        
    def draw(self, screen):
        self.gifter1.draw(screen)
        self.gifter2.draw(screen)
        self.gifter3.draw(screen)