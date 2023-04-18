from input import keyboard
from sprites import predef_spritesheets, SPRITESHEETS
from entity import *
from flowey import flowey
from fonts import story
from sound import predef_effects, predef_songs, EFFECTS, SONGS
from story_board import story_board
from player import character
import pygame

GLOBAL_SCREEN = None

class window:
    def __init__(self, title: str) -> None:
        global GLOBAL_SCREEN, SPRITESHEETS, EFFECTS, SONGS

        pygame.init()
        pygame.mixer.init(channels = 4)

        self.title = title
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption(self.title)

        GLOBAL_SCREEN = self.screen
        SPRITESHEETS = predef_spritesheets(self.screen)
        EFFECTS = predef_effects()
        SONGS = predef_songs()

        self.running = False
        self.keyboard = keyboard()
        self.clock = pygame.time.Clock()
        self.entities = entity_collection()
        self.flowey = flowey(SPRITESHEETS, 0, 0)
        self.character = character(640 // 2, 480 // 2, self.keyboard, SPRITESHEETS)
        self.board = story_board(story(SPRITESHEETS, self.keyboard), self)

        self.flowey.visible = False

    def run(self) -> None:
        global EFFECTS

        self.running = True

        delta_time = 0.0
        updates_per_second = 60
        tick = 0

        SONGS.STORY.play(pitch = 0.9, loops = 0)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.keyboard.update_keys()

            delta_time += self.clock.tick() / 1000.0

            while delta_time >= 1.0 / updates_per_second:
                self.update()

                delta_time -= 1.0 / updates_per_second

            if not self.board.running:
                self.board.begin(1)

            tick += 1

            self.render()

        pygame.quit()

    def update(self) -> None:
        self.flowey.update()
        self.entities.update()
        self.board.update()
        self.character.update()

    def render(self) -> None:
        self.screen.fill((0, 0, 0))

        self.entities.render(self.screen)
        self.flowey.render(self.screen)
        self.board.render(self.screen)
        self.character.render(self.screen)

        pygame.display.flip()

    def run_event(self, story_number: int, event_number: int) -> None:
        global SONGS

        if story_number == 0:
            if event_number == 0:
                SONGS.STORY.stop()
                SONGS.STORY_FROZEN.play(pitch = 0.84)
            elif event_number == 1:
                SONGS.STORY_FROZEN.stop()

game = window("Undertale: Omega Flowey")
game.run()