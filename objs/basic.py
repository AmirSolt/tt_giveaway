import pygame
from helper import utils, config
import urllib.request


class Text:
    
    def __init__(self, text:str, center:tuple[int,int], font_size:int=32, color:tuple[int,int,int]=(0,0,0), bg_color:tuple[int,int,int]=(255,255,255)) -> None:
        self.color = color 
        self.bg_color = bg_color 
        
        self.font_size:int = font_size
        self.font:pygame.font.Font = pygame.font.Font(config.FONT_PATH, font_size)
        
        self.text:str = text
        self.target_center:tuple[int,int] = center
        
        self.labels:list[pygame.Surface] = self.__get_labels(text)
        self.label_rects:list[pygame.Rect] = self.__get_rects()
    
    def set_font_size(self, font_size:int):
        self.font_size = font_size
        self.font:pygame.font.Font = pygame.font.Font(config.FONT_PATH, font_size)
        self.labels:list[pygame.Surface] = self.__get_labels(self.text)
        self.label_rects:list[pygame.Rect] = self.__get_rects()
    
    def update(self, text:str, color:tuple[int,int,int]=(0,0,0), bg_color:tuple[int,int,int]=(255,255,255) ):
        self.text:str = text
        self.color = color 
        self.bg_color = bg_color
        self.labels:list[pygame.Surface] = self.__get_labels(text)
        self.label_rects:list[pygame.Rect] = self.__get_rects()
        
    def draw(self, screen:pygame.Surface):
        for label, label_rect in zip(self.labels, self.label_rects):
            screen.blit(label, label_rect)
        
        
    def __get_labels(self, text:str)->list[pygame.Surface]:
        words:list[str] = text.split(" ")
        max_char_count = int(config.WIDTH*0.75/self.font_size)
        char_count = 0
        n_text:str = ""
        for word in words:
            char_count += len(word)
            if char_count >= max_char_count:
                n_text += word+" \n"
                char_count = 0
            else:
                n_text += word+" "
            
        n_labels:list[pygame.Surface] = [
            self.font.render(t, True, self.color, self.bg_color)
            for t in n_text.split("\n")]
            
        return n_labels
    
    def __get_rects(self)->list[pygame.Rect]:
        def func(n):
            if n % 2 == 0: 
                return [(x-n/2+.5) for x in range(n)]
            else:
                return [(x -n//2) for x in range(n)]
            
        rects = [label.get_rect() for label in self.labels]
        cx, cy = self.target_center
        multipliers = func(len(rects))
        for rect, m in zip(rects, multipliers):
            rect.center = (cx, cy+(rect.h*m))
        return rects
        
class Image:
    
    def __init__(self, src:str, center:tuple[int,int], size:tuple[int,int]) -> None:
        self.surface = pygame.image.load(src)
        if size:
            self.surface = pygame.transform.scale(self.surface, size)
        self.rect = self.surface.get_rect() 
        self.rect.center = center
    
    @staticmethod
    def download_img(url:str, filename:str)->str:
        path = config.CACHED_IMGS_PATH + filename + ".jpg"
        urllib.request.urlretrieve(url, path)
        return path
    
    def draw(self, screen:pygame.Surface):
        screen.blit(self.surface, self.rect.topleft)
        