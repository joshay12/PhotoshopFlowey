from input import keyboard
from sprites import predef_spritesheets, SPRITESHEETS
from entity import *
from flowey import flowey
from fonts import story
from sound import predef_effects, predef_songs, EFFECTS, SONGS
from story_board import story_board
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

        self.last_event = 0
        #Whether or not the game is on the screen to choose "Continue" or "Restart"
        self.choose_cont_rest = False
        #True if "Continue" is highlighted and False if "Restart" is highlighted.
        self.cont_or_rest = True
        #Checks if the "Right" or "Left" button is currently held on the "Continue/Restart" screen.
        self.cont_or_rest_held = True
        self.running = False
        self.keyboard = keyboard()
        self.clock = pygame.time.Clock()
        self.entities = entity_collection()
        self.flowey = flowey(SPRITESHEETS, 0, 0)
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
                self.board.begin()

            tick += 1

            self.render()

        pygame.quit()

    def update(self) -> None:
        self.flowey.update()
        self.entities.update()
        self.board.update()

        #if self.choose_cont_rest:
        #    if self.cont_or_rest:
        #        self.undertale.say("Flowey    LV9999    9999:99\nMy World\n\n                Restart", 100, 170, False, None, 0)
        #        self.undertale_yellow.say("   Continue", 100, 284, False, None, 0)
        #    else:
        #        self.undertale.say("Flowey    LV9999    9999:99\nMy World\n\n   Continue", 100, 170, False, None, 0)
        #        self.undertale_yellow.say("                Restart", 100, 284, False, None, 0)
        #
        #    if self.cont_or_rest_held:
        #        if not self.keyboard.is_right() and not self.keyboard.is_left():
        #            self.cont_or_rest_held = False
        #    elif not self.cont_or_rest_held:
        #        if self.keyboard.is_right() or self.keyboard.is_left():
        #            self.cont_or_rest = not self.cont_or_rest
        #            self.cont_or_rest_held = True
        #
        #    self.undertale.update()
        #    self.undertale_yellow.update()
        #elif self.story.stories_played > 0:
        #    self.story.update()
        #    self.check_for_event()

    def render(self) -> None:
        self.screen.fill((0, 0, 0))

        self.entities.render(self.screen)
        self.flowey.render(self.screen)
        self.board.render(self.screen)

        #if self.choose_cont_rest:
        #    self.undertale.render(self.screen)
        #    self.undertale_yellow.render(self.screen)
        #elif self.story.stories_played > 0:
        #    self.story.render(self.screen)

        pygame.display.flip()

    def run_event(self, story_number: int, event_number: int) -> None:
        if story_number == 0:
            if event_number == 0:
                global SONGS

                SONGS.STORY.stop()
                SONGS.STORY_FROZEN.play(pitch = 0.84)

    #def check_for_event(self) -> None:
    #    if self.last_event == self.story.events or self.story.current_story == None:
    #        return
    #
    #    if self.story.current_story == self.story.pre_story_lines:
    #        if self.story.events == 1:
    #            global SONGS
    #
    #            SONGS.STORY.stop()
    #            SONGS.STORY_FROZEN.play(pitch = 0.84)
    #        elif self.story.events == 2:
    #            self.choose_cont_rest = True
    #
    #    self.last_event = self.story.events

game = window("Undertale: Omega Flowey")
game.run()