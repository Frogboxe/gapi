"""
Created on the 6th of ‎October, ‎2017

[11/10] This is only a differnt module because I initially expected
the implementation to be more difficult.

"""
import pygame

import gapi.gapi as gapi
import gapi.elements as elements
import gapi.containers as containers
import gapi.detection as detection

class dSubScreen(gapi.dScreen):
    """
    Subscreens are screens held within the main screen.
    They hold their own surface, elements, detectors and
    input handling and, as such, act as Screens to Elements,
    meaning that no modification must be made to an Element
    to allow it to belong to a subscreen.

    Do not call run on a subscreen. Just don't.
    """
    screen = gapi.dScreen
    done = bool
    elementsStacks = str, str, ... # inf
    elements = containers.MLS
    detectorStacks = str, str, ... # inf
    detectors = containers.MLS
    detections = detection.dDetections
    surface = pygame.Surface
    size = int, int
    def __init__(self, screen, stack, pos):
        # add this to master's subscreens
        screen.subScreens.append_object(self, stack)
        # setup stuff
        self.screen = screen
        self.pos = pos
        self.done = False
        self.elements = containers.MLS(self.elementsStacks)
        self.detectors = containers.MLS(self.detectorStacks)
        self.surface = pygame.Surface(self.size)
        elements.Background(self, self.size, self.colour)

    def _detect(self):
        for detector, ref, i in self.detectors:
            self.detections.detectFuncs[ref](self, detector)

    def _draw(self):
        for element, stack, i in self.elements:
            element._draw()

    def _update(self):
        self.update()
        for element, stack, i in self.elements:
            element._update()

    # this series of properties exist so that Elements can
    # get data from the main Screen WITHOUT creating data
    # redundancy.

    @property
    def _keysDown(self):
        return self.screen._keysDown

    @property
    def _keys(self):
        return self.screen._keys

    @property
    def _keysUp(self):
        return self.screen._keysUp

    @property
    def _mouseDown(self):
        return self.screen._mouseDown

    @property
    def _mouse(self):
        return self.screen._mouse

    @property
    def _mouseUp(self):
        return self.screen._mouseUp

    @property
    def mousePos(self):
        return self.screen.mousePos






    
