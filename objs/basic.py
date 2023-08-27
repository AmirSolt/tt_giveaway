from PIL import Image, ImageDraw
import pygame
from helper import utils, config
import urllib.request
import os
from pygame import gfxdraw



class Text:
    
    def __init__(self, text:str, center:tuple[int,int], font_size:int=32, color:tuple[int,int,int]=(0,0,0), bg_color:tuple[int,int,int, int]=(255,255,255, 0.1)) -> None:
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
    
    def update(self, text:str, color:tuple[int,int,int]=None, bg_color:tuple[int,int,int, int]=None ):
        self.text:str = text
        if color : self.color = color 
        if bg_color: self.bg_color = bg_color
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
        
        
        
        
        
class Pic:
    
    def __init__(self, src:str, center:tuple[int,int], size:tuple[int,int]) -> None:
        self.surface = pygame.image.load(src)
        self.rounded_border = pygame.image.load(config.PFP_FRAME_PATH)
        

            
        self.rect = self.surface.get_rect() 
        self.rect.center = center
        
        frame_mult = 1.1
        if size:
            self.surface = pygame.transform.smoothscale(self.surface, size)
            self.rounded_border = pygame.transform.smoothscale(self.rounded_border, (size[0]*frame_mult, size[1]*frame_mult))
            
        self.surface_pos = (self.rect.center[0]-(size[0]*0.5), self.rect.center[1]-(size[1]*0.5))
        self.rounded_border_pos = (self.rect.center[0]-(size[0]*frame_mult/2), self.rect.center[1]-(size[1]*frame_mult/2))
    
    @staticmethod
    def download_img(url:str, path:str)->str:
        urllib.request.urlretrieve(url, path)
        return path
    
    @staticmethod
    def make_rounded(path):
        im = Image.open(path)
        rad = min(im.size)//2
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        
        path = os.path.splitext(path)[0] + '.png'
        im.save(path)
        return path

    def draw(self, screen:pygame.Surface):
        screen.blit(self.surface, self.rect.topleft)
    
    def draw_with_circle_border(self, screen:pygame.Surface):
        screen.blit(self.surface, self.surface_pos)
        screen.blit(self.rounded_border, self.rounded_border_pos)

        
        
class Avatar:
    
    def __init__(self, src:str, center:tuple[int,int], size:tuple[int,int]) -> None:
        self.surface = pygame.image.load(src)
        self.rounded_border = pygame.image.load(config.PFP_FRAME_PATH)
        

            
        self.rect = self.surface.get_rect() 
        self.rect.center = center
        
        frame_mult = 1.1
        if size:
            self.surface = pygame.transform.smoothscale(self.surface, size)
            self.rounded_border = pygame.transform.smoothscale(self.rounded_border, (size[0]*frame_mult, size[1]*frame_mult))
            
        self.surface_pos = (self.rect.center[0]-(size[0]*0.5), self.rect.center[1]-(size[1]*0.5))
        self.rounded_border_pos = (self.rect.center[0]-(size[0]*frame_mult/2), self.rect.center[1]-(size[1]*frame_mult/2))
    
    @staticmethod
    def download_img(url:str, path:str)->str:
        urllib.request.urlretrieve(url, path)
        return path
    
    @staticmethod
    def make_rounded(path):
        im = Image.open(path)
        rad = min(im.size)//2
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        
        path = os.path.splitext(path)[0] + '.png'
        im.save(path)
        return path

    def draw(self, screen:pygame.Surface):
        screen.blit(self.surface, self.rect.topleft)
    
    def draw_with_circle_border(self, screen:pygame.Surface):
        screen.blit(self.surface, self.surface_pos)
        screen.blit(self.rounded_border, self.rounded_border_pos)

