"""
Created on the 4th of October, 2017

This file is a documented use of GAPI on a basic level.
"""
import gapi.gapi as gapi
import gapi.elements as elements
import gapi.k as k
import gapi.subwindow as subwindow
import gapi.detection as detection

class dummy_Screen(gapi.dScreen):
    elementStacks = "bg", "main" # "bg" is an engine requirement, else optional
    subScreenStacks = "main",
    detectorStacks = ()
    size = 800, 600
    flags = 0
    caption = "TEMPLATE"
    fps = 60
    # overload me
    def post_init(self):
        """
        Called after pygame has started up but before
        the event loop. This is the best place for
        spawning in elements.
        """
        subscreen = dummy_SubScreen(self, (0, 0))        
        dummy_Element(subscreen, "main", (0, 0),
                      elements.dElement.create_surf((256, 256), (255, 255, 255)))
        dummy_Text(subscreen, "main", (0, 0), "hello, world!")

    # overload me
    def key_down(self, key):
        """
        Called whenever a key is pressed. This can happen
        multiple times per frame, depending on how many
        keys were pressed at once.

        key:
            keycode of the key pressed
        """
        pass
        
    # overload me
    def key_up(self, key):
        """
        Same as key_down, except on key released instead
        of on key pressed.

        key:
            keycode of the key released
        """
        pass

    # overload me
    def update(self):
        """
        Called once per frame after screen drawing has
        been done but before it has been pushed to the
        screen.
        """
        pass

    # overload me: must return bool
    def exit(self):
        """
        Returns bool, telling engine if it should accept
        the exit request (True to continue to exit).
        """
        return True

    # overload me
    def close(self):
        """
        Called after the screen has closed AND pygame
        is shutting down (after this returns, pygame
        will be unloaded).
        """
        pass

class dummy_SubScreen(subwindow.dSubScreen):
    """
    NOTE: dSubScreen derives dScreen, hence carries
    methods like key_down and the like. All of these
    work properly, with the exception of dScreen methods
    that specifically work with pygame.display, such as
    run, _init and _draw. Do not call these. They are
    overloaded to run assert False for a reason.
    """
    elementsStacks = "bg", "main" # "bg" is engine requirement
    detectorStacks = "on_mouse_down", "on_mouse_up", "key_typed",
    size = 400, 300
    def __init__(self, screen, pos):
        """
        screen:
            dScreen deriv owner of this element.
        pos:
            position on master screen to render
            this subscreen to.
        """
        super().__init__(screen, "main", (0, 0))

    def update(self):
        pass

    
class dummy_Element(elements.dElement):
    def __init__(self, screen, layer, pos, texture):
        """
        screen:
            dScreen deriv owner of this element.
        layer:
            str defining a stack to be pushed to in
            the screen's MLS (look at MLS docs inside
            gapi.containers).
        pos:
            tuple of 2 ints to describe a position on
            the screen.
        texture:
            pygame.Surface that is blitted to the
            screen.
        """
        self.pos = pos
        self.texture = texture
        super().__init__(screen, layer)
        detector = detection.dDetector(self.screen, "on_mouse_down",
                                       self, self.pos)
        detector.set_expressions(detection.Detectors.box_detector(
            self.size))
        detector = detection.dDetector(self.screen, "on_mouse_up",
                                       self, self.pos)
        detector.set_expressions(detection.Detectors.box_detector(
            self.size))
        detector = detection.dDetector(self.screen, "key_typed",
                                       self, self.pos)
        
    # overload me
    def update(self):
        """
        Called every frame by the engine.
        """
        pass

    # overload me: must call super().delete()
    def delete(self):
        """
        Called when engine wants to kill the object.
        If overriden, ensure to call base delete.
        Safe to directly call to delete an object
        (DO THIS BEFORE del <obj> IF YOU FEEL
        ODDLY COMPELLED TO USE del <obj>!).
        """
        super().delete()

    def on_mouse_down(self, mousePos, mouseKey):
        pass

    def on_mouse_up(self, mousePos, mouseKey):
        pass

    def key_typed(self, key):
        print(key)

class dummy_Text(elements.dText):
    fontSize = 34
    fontRoot = "OpenDyslexic.ttf"
    fontAllias = 16
    fontColour = 255, 0, 0
    def __init__(self, screen, layer, pos, text):
        """
        screen:
            dScreen deriv owner of this element.
        layer:
            str defining a stack to be pushed to in
            the screen's MLS (look at MLS docs inside
            gapi.containers).
        pos:
            tuple of 2 ints to describe a position on
            the screen.
        text:
            text to be renderered and blitted to the
            screen each frame.
        """
        self.pos = pos
        self.text = text
        super().__init__(screen, layer)


dummy_Screen().run()





























    
