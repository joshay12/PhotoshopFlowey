#Specifically import these items rather than the entirety of pygame.
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_z, K_ESCAPE, key as k

#A class which makes input much simpler and easier to handle and understand.
class keyboard:
    #The constructor doesn't need anything but to set up its dictionary of keys.
    def __init__(self) -> None:
        self.keys = k.get_pressed()

    #This function updates what is pressed and released on the keyboard.
    def update_keys(self) -> None:
        self.keys = k.get_pressed()

    #Retrieve a specific key not listed below this function and check whether or not it is pressed.
    def get_key(self, key: int) -> bool:
        return self.keys[key]

    #Check if the UP arrow is pressed.
    def is_up(self) -> bool:
        return self.keys[K_UP]

    #Check if the DOWN arrow is pressed.
    def is_down(self) -> bool:
        return self.keys[K_DOWN]

    #Check if the LEFT arrow is pressed.
    def is_left(self) -> bool:
        return self.keys[K_LEFT]

    #Check if the RIGHT arrow is pressed.
    def is_right(self) -> bool:
        return self.keys[K_RIGHT]

    #Check if the Z key is pressed.
    def is_z(self) -> bool:
        return self.keys[K_z]

    #Check if the ESCAPE key is pressed.
    def is_esc(self) -> bool:
        return self.keys[K_ESCAPE]