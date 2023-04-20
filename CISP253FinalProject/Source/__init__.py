from input import keyboard
from sprites import predef_spritesheets, SPRITESHEETS
from entity import *
from flowey import flowey
from fonts import story
from sound import predef_effects, predef_songs, EFFECTS, SONGS
from story_board import story_board, intro_picture, file_backdrop
from player import character, save_star
from getpass import getuser
import pygame

GLOBAL_SCREEN = None

class window:
    def __init__(self, title: str) -> None:
        global GLOBAL_SCREEN, SPRITESHEETS, EFFECTS, SONGS

        pygame.init()
        pygame.mixer.init(channels = 8)

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
        self.entities.add(intro_picture(640 / 2, 480 / 3, SPRITESHEETS))
        self.entities.add(file_backdrop(640 / 2, 150, SPRITESHEETS).hide())
        self.entities.add(character(self, 640 / 2, 480 - 480 / 3, self.screen.get_width(), self.screen.get_height(), self.keyboard, SPRITESHEETS))
        self.entities.add(save_star(640 / 2, -350, self.entities, SPRITESHEETS))
        self.entities.get_items_by_class(character).first().set_save_star(self.entities).set_heal_effect(EFFECTS.HEAL)
        self.flowey = flowey(SPRITESHEETS, 0, 0)
        self.board = story_board(story(SPRITESHEETS, EFFECTS, self.keyboard), self.entities, self)

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
                self.board.begin(1) #INSERT NUMBER HERE TO SKIP TO CERTAIN PORTION OF STORY.

            tick += 1

            self.render()

        pygame.quit()

    def update(self) -> None:
        #self.entities.update()
        self.board.update()
        self.flowey.update()

    def render(self) -> None:
        self.screen.fill((0, 0, 0))

        #self.entities.render(self.screen)
        self.board.render(self.screen)
        self.flowey.render(self.screen)

        pygame.display.flip()

    def run_event(self, story_number: int, event_number: int) -> None:
        global SONGS

        if story_number == 0:
            if event_number == 0:
                SONGS.STORY.stop()
                SONGS.STORY_FROZEN.play(pitch = 0.84)

                self.entities.get_items_by_class(intro_picture).first().animation.set_current(1)
            elif event_number == 1:
                SONGS.STORY_FROZEN.stop()

                self.entities.get_items_by_class(character).first().visible = True
            elif event_number == 2:
                f_back = self.entities.get_items_by_class(file_backdrop).first()

                f_back.show_generated_font(getuser(), self.board.story.undertale)
                f_back.show()

game = window("Undertale: Omega Flowey")
game.run()