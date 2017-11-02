from functools import lru_cache

import gapi.k as k

class Detectors:
    def box_detector(size):
        mx, my = size
        return {
            lambda x, y: y >= 0,
            lambda x, y: x >= 0,
            lambda x, y: y <= my,
            lambda x, y: x <= mx,
            }
    
    def circle_detector(radius):
        return {
            lambda x, y: x**2 + y**2 <= radius**2,
            }

    def pointy_top_hexagon_detector(dim):
        return {
            lambda x, y: x >= 0,
            lambda x, y: x <= dim,
            lambda x, y: y <= (2*x*dim)-dim,
            }
    
class dDetector:
    expressions = set
    screen = None # dScreen subclass
    pos = int, int
    def __init__(self, screen, layer, owner, pos):
        screen.detectors.append_object(self, layer)
        self.owner = owner
        self.pos = pos
        self.expressions = set()

    def add_expression(self, expression):
        self.expressions.add(expression)

    def set_expressions(self, expressions):
        self.expressions = expressions

    def point_inside(self, point):
        x, y = point[0]-self.owner.pos[0], point[1]-self.owner.pos[1]
        for expression in self.expressions:
            if not expression(x, y):
                return False
        return True


class dDetections:
    detectFuncs = dict
    @staticmethod
    def on_mouse_down(screen, detector):
        if len(screen._mouseDown) > 0: # if a mouse key is down
            if detector.point_inside(screen.mousePos):
                for mKey in screen._mouseDown:
                    detector.owner.on_mouse_down(screen.mousePos, mKey)
                
    @staticmethod
    def on_mouse_up(screen, detector):
        if len(screen._mouseUp) > 0: # if a mouse key is up
            if detector.point_inside(screen.mousePos):
                for mKey in screen._mouseUp:
                    detector.owner.on_mouse_up(screen.mousePos, mKey)

    @staticmethod
    def mouse_hover(screen, detector):
        if detector.point_inside(screen.mousePos):
            detector.owner.mouse_hover(screen.mousePos)

    @staticmethod
    def key_down(screen, detector):
        for key in screen._keysDown:
            detector.owner.key_down(key)

    @staticmethod
    def key_up(screen, detector):
        for key in screen._keysUp:
            detector.owner.key_up(key)

    

dDetections.detectFuncs = {
    "on_mouse_down":dDetections.on_mouse_down,
    "on_mouse_up":dDetections.on_mouse_up,
    "mouse_hover":dDetections.mouse_hover,
    "key_down":dDetections.key_down,
    "key_up":dDetections.key_up,
    }




























