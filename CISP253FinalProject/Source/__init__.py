from input import keyboard
from sprites import predef_spritesheets, SPRITESHEETS
from entity import *
from flowey import flowey
from fonts import undertale_font
import pygame

GLOBAL_SCREEN = None

class window:
    def __init__(self, title: str) -> None:
        global GLOBAL_SCREEN, SPRITESHEETS

        pygame.init()

        self.title = title
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption(self.title)

        GLOBAL_SCREEN = self.screen
        SPRITESHEETS = predef_spritesheets(self.screen)

        self.running = False
        self.keyboard = keyboard()
        self.clock = pygame.time.Clock()
        self.entities = entity_collection()
        self.flowey = flowey(SPRITESHEETS, 0, 0)
        self.font = undertale_font(SPRITESHEETS.UNDERTALE_FONT_ANIMATION)

    def run(self) -> None:
        self.running = True

        delta_time = 0.0
        updates_per_second = 60

        self.font.say("Hello World!", 30, 300, 15)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.keyboard.update_keys()

            delta_time += self.clock.tick() / 1000.0

            while delta_time >= 1.0 / updates_per_second:
                self.update()

                delta_time -= 1.0 / updates_per_second

            self.render()

        pygame.quit()

    def update(self) -> None:
        self.flowey.update()
        self.entities.update()
        self.font.update()

    def render(self) -> None:
        self.screen.fill((0, 0, 0))

        self.entities.render(self.screen)
        self.flowey.render(self.screen)
        self.font.render(self.screen)

        pygame.display.flip()

game = window("Undertale: Omega Flowey")
game.run()