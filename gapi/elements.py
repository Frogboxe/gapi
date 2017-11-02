"""
Created on the 2nd of October, 2017

[11/10] A place to put Elements and subclasses thereof. 

"""
import pygame

from functools import lru_cache

class dElement:
    screen = None # dScreen
    pos = int, int
    size = int, int
    render = False
    _texture = pygame.Surface
    def __init__(self, screen, layer):
        self.init(screen, layer)

    def update(self):
        pass

    def init(self, screen, stack, insert=None):
        if insert is None:
            screen.elements.append_object(self, stack)
        else:
            assert isinstance(insert, int)
            screen.elements.insert_object(self, stack, insert)
        self.screen = screen
        return self

    def delete(self):
        self.screen.remove_object(self)

    def _update(self):
        self.update()

    def _draw(self):
        if self.render:
            self.screen.draw(self._texture, self.pos)

    @staticmethod
    @lru_cache(64)
    def create_surf(size, col):
        if len(col) == 3:
            surf = pygame.Surface(size)
            surf.fill(col)
            surf = surf.convert()
        elif len(col) == 4:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill(col)
            surf = surf.convert_alpha()
        return surf

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, texture):
        assert isinstance(texture, pygame.Surface) or texture is None
        self._texture = texture
        self.render = not texture is None
        self.size = self._texture.get_size()


class dText(dElement):
    fontSize = int
    fontRoot = str
    fontAllias = int
    fontColour = int, int, int
    _text = str
    @staticmethod
    @lru_cache(16)
    def get_font(size, font):
        return pygame.font.Font("gapi/fonts/"+font, size)
    
    @staticmethod
    @lru_cache(1024)
    def generate_text(text, size, font, allias, colour):
        font = dText.get_font(size, font)
        return font.render(text, allias, colour)
        
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self.texture = dText.generate_text(text, self.fontSize, self.fontRoot,
                                           self.fontAllias, self.fontColour)
        self._text = text

class Background(dElement):
    pos = 0, 0
    def __init__(self, screen, size, colour):
        self.texture = dElement.create_surf(size, colour)
        self.init(screen, "bg")





        
