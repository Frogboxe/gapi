"""
Created on the 29th of September, 2017

[11/10] This is the main part of GAPI.
"""

import pygame

import gapi.k as k
import gapi.containers as containers
import gapi.elements as elements
import gapi.detection as detection
import gapi.exceptions as exceptions

class dScreen:
    """
    Screens and subscreens should derive from this class. This handles
    the event loop, OS event pulling, detection, drawing to screen and
    frame logic calls.

    NOTE: documentation on public methods (things that the user can
    override using inheritance) is contained inside template.py
    """
    done = bool
    elementStacks = str, str, ... # inf
    elements = containers.MLS
    subScreenStacks = str, str, ... # inf
    subScreens = containers.MLS
    detectorStacks = str, str, ... # inf
    detectors = containers.MLS
    detections = detection.dDetections
    surface = pygame.Surface
    colour = 0, 0, 0
    size = int, int
    flags = int
    caption = str
    fps = int
    exitInfo = str
    mousePos = int, int
    _keysDown = set
    _keys = set
    _keysUp = set
    _mouseDown = set
    _mouse = set
    _mouseUp = set
    def __init__(self):
        self.done = False
        self.exitInfo = "INIT_FAILURE"

    def close(self):
        pass

    def post_init(self):
        pass

    def key_down(self, key):
        pass

    def key_up(self, key):
        pass

    def mouse_down(self, key):
        pass

    def mouse_up(self, key):
        pass

    def update(self):
        pass

    def draw(self, texture, pos):
        self.surface.blit(texture, pos)

    def exit(self):
        return True # if not overriden, always allow exit

    def soft_exit(self):
        self.exitInfo = "GAPI_SOFT_EXIT"
        self.done = True

    def hard_exit(self):
        raise exceptions.GapiHardExit("HARD_EXIT")

    def run(self):
        """
        Main loop start. Call on instance of dScreen or dScreen subclass.
        Note that this should not be called on subscreens and will result
        in an assertion error (subwindow overrides run with assert False).
        """
        try:
            self.exitInfo = "INITIALISATION_ERROR"
            self._init()
            clock = pygame.time.Clock()
            self._keys = set()
            self._mouse = set()
            self.post_init()
            size = self.size
            elements.Background(screen=self, size=size, colour=self.colour)
            self.exitInfo = "GAPI_RUNTIME_ERROR"
            while not self.done:
                clock.tick(self.fps)
                self._keysDown = set()
                self._keysUp = set()
                self._mouseDown = set()
                self._mouseUp = set()
                self.mousePos = pygame.mouse.get_pos()
                for event in pygame.event.get(): # pygame OS events loop
                    if event.type == pygame.MOUSEMOTION:
                        ... # unimplemented behaviour
                    elif event.type == pygame.KEYDOWN:
                        self._key_down(event.key)
                    elif event.type == pygame.KEYUP:
                        self._key_up(event.key)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self._mouse_down(event.button)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self._mouse_up(event.button)
                    elif event.type == pygame.QUIT:
                        self.exitInfo = "OS_QUIT"
                        self.done = self._exit()
                self._detect() 
                self._update()
                self._draw() # draw everything to the screen surface
                pygame.display.flip() # push everything from the screen
                                      # surface to the actual screen
            self.exitInfo = "GAPI_SOFT_EXIT"
            
        except exceptions.GapiHardExit as e:
            self.exitInfo = "GAPI_HARD_EXIT"
            raise e
        except exceptions.GapiException as e:
            self.exitInfo = "GAPI_INTERNAL_ERROR"
            raise e
        except Exception as e:
            self.exitInfo = "PROGRAM_ERROR"
            raise e
        finally:
            print(self.exitInfo)
            self._close()

    def _init(self):
        """
        Called by run to initialise pygame stuff as well as
        set up the screen. This CAN be called to reset the screen.
        SHOULD however, is a completely different matter.
        """
        pygame.font.init()
        pygame.display.set_mode(self.size, self.flags)
        pygame.display.set_caption(self.caption)
        self.surface = pygame.display.get_surface()
        self.elements = containers.MLS(self.elementStacks)
        self.subScreens = containers.MLS(self.subScreenStacks)
        self.detectors = containers.MLS(self.detectorStacks)            

    def _key_down(self, key):
        self._keysDown.add(key)
        self._keys.add(key)
        self.key_down(key)
        for subscreen, stack, i in self.subScreens:
            subscreen.key_down(key)

    def _key_up(self, key):
        self._keysUp.add(key)
        self._keys.remove(key)
        self.key_up(key)
        for subscreen, stack, i in self.subScreens:
            subscreen.key_up(key)

    def _mouse_down(self, key):
        self._mouseDown.add(key)
        self._mouse.add(key)
        self.mouse_down(key)
        for subscreen, stack, i in self.subScreens:
            subscreen.mouse_down(key)

    def _mouse_up(self, key):
        self._mouseUp.add(key)
        self._mouse.remove(key)
        self.mouse_up(key)
        for subscreen, stack, i in self.subScreens:
            subscreen.mouse_up(key)

    def _detect(self):
        """
        notes: detections is a CLASS that is pointed to from
        an instance of a screen. This is done to allow modification
        via inheritance and allow different subscreens to have different
        detector behaviours. (default of detections is
        detections.detections).

        Further, <ref> from self.detectors is ALSO the name of the
        function that should be called to ask whether a detector
        should be t r i g g e r e d or not.
        """
        for detector, ref, i in self.detectors:
            self.detections.detectFuncs[ref](self, detector)
        for subscreen, stack, i in self.subScreens:
            subscreen._detect()

    def _update(self):
        self.update()
        for subscreen, stack, i in self.subScreens:
            subscreen._update()

    def _draw(self):
        for element, stack, i in self.elements:
            element._draw()
        for subscreen, stack, i in self.subScreens:
            subscreen._draw()
            self.draw(subscreen.surface, subscreen.pos)

    def _exit(self):
        if self.done:
            raise exceptions.GapiHardExit("ENGINE_HARD_EXIT")
        return self.exit()

    def _close(self):
        self.close()
        pygame.quit()












    
