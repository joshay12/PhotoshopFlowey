from entity import entity
from sprites import predef_spritesheets
from input import keyboard
from pygame import Surface

class character(entity):
    def __init__(self, x: int, y: int, keyboard: keyboard, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.PLAYER_DOWN_ANIMATION, x, y, False, False)

        self.speed = 3
        self.down = spritesheets.PLAYER_DOWN_ANIMATION
        self.up = spritesheets.PLAYER_UP_ANIMATION
        self.left = spritesheets.PLAYER_LEFT_ANIMATION
        self.right = spritesheets.PLAYER_RIGHT_ANIMATION
        self.keyboard = keyboard
        self.visible = False

    def update(self) -> None:
        if not self.visible:
            return

        self.animation.update()

        x = 0
        y = 0

        if self.keyboard.is_up():
            y = -self.speed
            self.animation = self.up
        elif self.keyboard.is_down():
            y = self.speed
            self.animation = self.down
        
        if self.keyboard.is_left():
            x = -self.speed
            self.animation = self.left
        elif self.keyboard.is_right():
            x = self.speed
            self.animation = self.right

        if x == 0 and y == 0:
            self.animation.set_current(0)
            self.animation.increment = 0
        else:
            self.animation.increment = 12

        self.x += x
        self.y += y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())