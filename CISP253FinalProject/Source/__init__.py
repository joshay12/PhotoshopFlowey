from input import keyboard
from sprites import predef_spritesheets, SPRITESHEETS
from entity import *
from flowey import flowey
from fonts import story, fonts_init
from sound import predef_effects, predef_songs, EFFECTS, SONGS
from story_board import story_board, intro_picture, file_backdrop, file_shattered, flowey_head, flowey_static
from player import character, save_star, soul, soul_npc
from getpass import getuser
from math import sin
import pygame, random

GLOBAL_SCREEN = None
MY_SCREEN = None

class window:
    def __init__(self, title: str) -> None:
        global GLOBAL_SCREEN, MY_SCREEN, SPRITESHEETS, EFFECTS, SONGS

        pygame.init()
        pygame.mixer.init(channels = 16)

        self.title = title
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption(self.title)

        GLOBAL_SCREEN = self.screen
        MY_SCREEN = my_screen()

        entity_init(MY_SCREEN)
        fonts_init(MY_SCREEN)

        SPRITESHEETS = predef_spritesheets(self.screen)
        EFFECTS = predef_effects()
        SONGS = predef_songs()

        self.red = 0
        self.red_increase = True
        self.begin_fight = False
        self.stop_red = False
        self.f4 = False
        self.running = False
        self.keyboard = keyboard()
        self.clock = pygame.time.Clock()
        self.entities = entity_collection()
        self.entities.add(intro_picture(640 / 2, 480 / 3, SPRITESHEETS))
        self.entities.add(file_backdrop(self, 640 / 2, 150, SPRITESHEETS, EFFECTS).hide())
        self.entities.add(character(self, 640 / 2, 480 - 480 / 3, self.screen.get_width(), self.screen.get_height(), self.keyboard, SPRITESHEETS))
        self.entities.add(save_star(640 / 2, -350, self.entities, SPRITESHEETS))
        self.entities.get_items_by_class(character).first().set_save_star(self.entities).set_heal_effect(EFFECTS.HEAL)
        self.flowey = flowey(self, SPRITESHEETS, 0, -475)
        self.board = story_board(story(SPRITESHEETS, EFFECTS, self.keyboard), self.entities, self)

        self.tick = 0

    def run(self) -> None:
        global MY_SCREEN, EFFECTS

        self.running = True

        delta_time = 0.0
        updates_per_second = 60
        tick = 0

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.keyboard.update_keys()

            delta_time += self.clock.tick() / 1000.0

            while delta_time >= 1.0 / updates_per_second:
                self.update(MY_SCREEN)

                delta_time -= 1.0 / updates_per_second

            if not self.board.running and tick == 5:
                SONGS.STORY.play(pitch = 0.9, loops = 0)
                self.board.begin(EFFECTS, 3) #INSERT NUMBER HERE TO SKIP TO CERTAIN PORTION OF STORY.

            tick += 1

            self.render()

        pygame.quit()

    def update(self, my_screen: 'my_screen') -> None:
        #self.entities.update()
        self.board.update()
        self.flowey.update()
        
        my_screen.update()

        if self.keyboard.is_f4() and not self.f4:
            pygame.display.toggle_fullscreen()

            self.f4 = True
        elif self.f4 and not self.keyboard.is_f4():
            self.f4 = False

        if self.begin_fight and not self.stop_red:
            if self.tick > 0:
                self.tick -= 1

                return

            self.red += 8 if self.red_increase else -8

            if self.red_increase and self.red > 100:
                self.red = 100
                self.tick = 20
                self.red_increase = False
            elif not self.red_increase and self.red < 0:
                self.red = 0
                self.red_increase = True
        elif self.red > 0 and self.stop_red:
            self.red -= 8

            if self.red < 0:
                self.red = 0

    def render(self) -> None:
        self.screen.fill((self.red, 0, 0))

        #self.entities.render(self.screen)
        self.board.render(self.screen)
        self.flowey.render(self.screen)

        pygame.display.flip()

    def run_event(self, story_number: int, event_number: int) -> None:
        global SONGS, EFFECTS

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
            elif event_number == 3:
                player = self.entities.get_items_by_class(character).first()

                player.run_controls = False
                player.animation = player.up

                f_back = self.entities.get_items_by_class(file_backdrop).first()

                EFFECTS.EXPLOSION.play()

                self.entities.add(flowey_head(self, 640 / 2, 150, SPRITESHEETS))
                self.entities.add(flowey_static(self.entities.get_items_by_class(flowey_head).first(), EFFECTS, SPRITESHEETS))
                self.entities.add(file_shattered(f_back, 109, 0, 0, SPRITESHEETS))
                self.entities.add(file_shattered(f_back, -106, 0, 1, SPRITESHEETS))
                self.entities.add(file_shattered(f_back, -25, -44, 2, SPRITESHEETS))
                self.entities.add(file_shattered(f_back, -32, 42, 3, SPRITESHEETS))
                self.entities.add(file_shattered(f_back, 62, -43, 4, SPRITESHEETS))
                self.entities.add(file_shattered(f_back, 49, 42, 5, SPRITESHEETS))

                self.entities.remove(f_back)
        elif story_number == 1:
            f_head = self.entities.get_items_by_class(flowey_head).first()
            f_static = self.entities.get_items_by_class(flowey_static).first()
            p_char = self.entities.get_items_by_class(character).first()

            if event_number == 0:
                f_head.hide()
                f_static.force_static(0)
                p_char.move_to_bottom = True
            elif event_number == 1:
                f_static.force_static(0)
                f_static.attempt = True
                f_head.shake = True
                f_head.show()
            elif event_number == 2:
                SONGS.YOU_IDIOT.play()

                self.board.story.play(self.board.story.pre_fight_story_before_first_snicker)
                self.board.running = True
                self.board.pause_loop = False
            elif event_number == 3:
                f_head.animation.set_current(1)
            elif event_number == 4:
                f_head.animation.set_current(0)
            elif event_number == 5:
                f_head.animation.set_current(2)
            elif event_number == 6:
                f_head.animation.set_current(0)
            elif event_number == 7:
                f_head.animation.set_current(3)
            elif event_number == 8:
                f_head.animation.set_current(4)
            elif event_number == 9:
                f_head.animation.set_current(5)
            elif event_number == 10:
                for _ in range(6):
                    if self.entities.has_item_by_class(file_shattered):
                        self.entities.remove(self.entities.get_items_by_class(file_shattered).first())
                    else:
                        break

                f_head.hide()
                f_head.flowey_snicker(False)
                f_static.force_static(1)
                f_static.attempt = False
        elif story_number == 2:
            f_head = self.entities.get_items_by_class(flowey_head).first()
            f_static = self.entities.get_items_by_class(flowey_static).first()

            if event_number == 0:
                EFFECTS.FLOWEY_CREEPY_LAUGH_NORMAL.play()
            elif event_number == 1:
                f_head.animation.set_current(0)
                f_head.show()
                f_static.force_static(1)
                f_static.attempt = True
            elif event_number == 2:
                self.board.story.play(self.board.story.pre_fight_story_before_second_snicker)
                self.board.running = True
                self.board.pause_loop = False
            elif event_number == 3:
                f_head.animation.set_current(2)
            elif event_number == 4:
                f_head.animation.set_current(1)
            elif event_number == 5:
                f_head.animation.set_current(6)
            elif event_number == 6:
                f_head.animation.set_current(1)
            elif event_number == 7:
                f_head.animation.set_current(0)
            elif event_number == 8:
                f_head.animation.set_current(1)
            elif event_number == 9:
                f_head.animation.set_current(7)
            elif event_number == 10:
                f_head.animation.set_current(5)
            elif event_number == 11:
                f_head.animation.set_current(8)
            elif event_number == 12:
                f_head.animation.set_current(9)
            elif event_number == 13:
                f_head.animation.set_current(9)
                f_head.animation.increment = 4
            elif event_number == 14:
                f_head.animation.set_current(19)
                f_head.animation.increment = 0
            elif event_number == 15:
                f_head.hide()
                f_head.flowey_snicker(True)
                f_static.force_static(1)
                f_static.attempt = False
            elif event_number == 16:
                EFFECTS.FLOWEY_CREEPY_LAUGH_SLOW.play()
            elif event_number == 17:
                f_head.animation.set_current(0)
                f_head.show()
                f_static.force_static(1)
                f_static.attempt = True
            elif event_number == 18:
                self.board.story.play(self.board.story.pre_fight_story_before_walk)
                self.board.running = True
                self.board.pause_loop = False
        elif story_number == 3:
            f_head = self.entities.get_items_by_class(flowey_head).first()
            f_static = self.entities.get_items_by_class(flowey_static).first()
            p_char = self.entities.get_items_by_class(character).first()

            if event_number == 0:
                f_head.animation.set_current(7)
            elif event_number == 1:
                f_head.animation.set_current(2)
            elif event_number == 2:
                f_head.animation.set_current(0)
            elif event_number == 3:
                f_head.animation.set_current(1)
            elif event_number == 4:
                f_head.animation.set_current(20)
            elif event_number == 5:
                f_head.animation.set_current(21)
            elif event_number == 6:
                f_head.animation.set_current(22)
            elif event_number == 7:
                p_char.move_up_slightly = True
            elif event_number == 8:
                f_head.animation.set_current(23)
                self.board.story.play(self.board.story.pre_fight_story_before_fight)
                self.board.running = True
                self.board.pause_loop = False
            elif event_number == 9:
                f_head.animation.set_current(24)
            elif event_number == 10:
                f_head.animation.set_current(25)
                f_static.attempt = False
                SONGS.YOU_IDIOT.stop()
            elif event_number == 11:
                skipped = False

                for _ in range(6):
                    if self.entities.has_item_by_class(file_shattered):
                        self.entities.remove(self.entities.get_items_by_class(file_shattered).first())

                        skipped = True
                    else:
                        break

                self.entities.remove(f_head)
                self.entities.remove(f_static)
                self.entities.add(soul(skipped, self, p_char, self.keyboard, EFFECTS, SPRITESHEETS))
        elif story_number == 4:
            if event_number == 0:
                self.entities.remove(self.entities.get_items_by_class(character).first())
            elif event_number == 1:
                x = 640 / 2 - 40
                y = 480 / 2 - 30

                for i in range(6):
                    self.entities.add(soul_npc(self, x, y, i, EFFECTS, SPRITESHEETS))

                    if i == 3:
                        x = 640 / 2 - 40
                        y -= 50
                    elif i == 4:
                        x = 640 / 2 + 40
                    else:
                        alter_x = x - 640 / 2
                        alter_x *= -2

                        x += alter_x

                        if i % 2 == 1:
                            x += sin(y * -5) * 70
                            y -= 50
            elif event_number == 2:
                EFFECTS.SOUL_SEND_TO_BATTLE.play()
            elif event_number == 3:
                for _ in range(6):
                    if self.entities.has_item_by_class(soul_npc):
                        self.entities.remove(self.entities.get_items_by_class(soul_npc).first())
                    else:
                        break

                self.begin_fight = True
                self.flowey.visible = True
                self.flowey.tick = 0
                self.flowey.move_to_0 = True

                SONGS.YOUR_BEST_NIGHTMARE_INTRO.play(loops = 0)
            elif event_number == 4:
                self.stop_red = True
                self.begin_fight = False


class my_screen:
    def __init__(self) -> None:
        self.x = 0.0
        self.y = 0.0
        self.shake_intensity = 0.0
        self.shake_recovery = 0
        self.tick = 0

    def shake_screen(self, intensity: int, speed: int) -> None:
        self.x = float(random.randint(-intensity, intensity))
        self.y = float(random.randint(-intensity, intensity))
        self.shake_intensity = float(intensity)
        self.shake_recovery = speed
        self.tick = 0

    def update(self) -> None:
        if self.shake_intensity >= 1.0:
            if self.tick >= 2:
                self.shake_screen(int(self.shake_intensity / ((abs(self.shake_recovery) / 10) + 1)), self.shake_recovery)
            else:
                self.tick += 1
        else:
            self.shake_intensity = 0
            self.x = 0
            self.y = 0
            self.tick = 0

game = window("Undertale: Omega Flowey")
game.run()