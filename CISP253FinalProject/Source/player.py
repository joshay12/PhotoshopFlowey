from entity import entity
from sprites import predef_spritesheets
from input import keyboard
from pygame import Surface

class character(entity):
    def __init__(self, x: int, y: int, keyboard: keyboard, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.PLAYER_DOWN_ANIMATION, x, y, False, False)

        self.down = spritesheets.PLAYER_DOWN_ANIMATION
        self.up = spritesheets.PLAYER_UP_ANIMATION
        self.left = spritesheets.PLAYER_LEFT_ANIMATION
        self.right = spritesheets.PLAYER_RIGHT_ANIMATION
        self.keyboard = keyboard

    def update(self) -> None:
        if self.keyboard.is_up():
            self.y -= 2
            self.animation = self.up
        elif self.keyboard.is_down():
            self.y += 2
            self.animation = self.down
        
        if self.keyboard.is_left():
            self.x -= 2
            self.animation = self.left
        elif self.keyboard.is_right():
            self.x += 2
            self.animation = self.right

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())