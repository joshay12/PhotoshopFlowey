from pygame import Surface
from player import save_star
from sprites import predef_spritesheets
from sound import predef_effects
from fonts import story
from entity import entity, entity_collection
from random import randint

#TODO: Add attacks.
#TODO: Add health bar.
#TODO: Add game over.
#TODO: Add different startup screens.

class story_board:
    def __init__(self, story: story, entities: entity_collection, window) -> None:
        self.story = story
        self.entities = entities
        self.window = window
        self.running = False
        self.pause_loop = False
        self.last_event = 0
        self.normal_font = story.undertale
        self.yellow_font = story.undertale_yellow

        #The variables below are to assist in proceeding the story in a flow.
        #It may look like a complicated mess, but there's a method to the madness.

        #Checks if the "Z" key is currently held.
        self.z_held = True
        #Whether or not the game is on the screen to choose "Continue" or "Restart"
        self.continue_or_restart_time = False
        #True if "Continue" is highlighted and False if "Restart" is highlighted.
        self.continue_or_restart = True
        #Verifies the "Z" key is not pressed before checking if the "Z" key is pressed on the "Continue/Restart" screen.
        self.continue_or_restart_prepared = False
        #Checks if the "Right" or "Left" button is currently held on the "Continue/Restart" screen.
        self.continue_or_restart_held = True

    def begin(self, effects: predef_effects, skip: int = 0) -> None:
        self.running = True

        if skip == 0:
            self.story.play(self.story.pre_story_lines)
        elif skip == 1:
            self.pause_loop = True
            self.window.run_event(0, 1)
            self.entities.remove(self.entities.get_items_by_class(intro_picture).first())
        elif skip == 2:
            self.pause_loop = True
            self.window.run_event(0, 1)
            self.window.run_event(0, 2)
            self.window.run_event(0, 3)
            self.entities.remove(self.entities.get_items_by_class(intro_picture).first())
            self.entities.remove(self.entities.get_items_by_class(save_star).first())
        elif skip == 3:
            self.pause_loop = True
            self.window.run_event(0, 1)
            self.window.run_event(0, 2)
            self.window.run_event(0, 3)
            self.entities.remove(self.entities.get_items_by_class(intro_picture).first())
            self.entities.remove(self.entities.get_items_by_class(save_star).first())
            
            effects.EXPLOSION.stop()

            self.window.run_event(3, 11)

    def update(self) -> None:
        self.entities.update()

        if self.running and not self.pause_loop:
            self.story.update()
            self.check_events()

        if self.pause_loop and self.continue_or_restart_time:
            self.select_continue_or_restart()

            self.normal_font.update()
            self.yellow_font.update()

    def render(self, screen: Surface) -> None:
        self.entities.render(screen)

        if self.running and not self.pause_loop:
            self.story.render(screen)

        if self.pause_loop and self.continue_or_restart_time:
            self.normal_font.render(screen)
            self.yellow_font.render(screen)

    def check_events(self) -> None:
        if self.last_event == self.story.events or self.story.current_story == None:
            return

        self.last_event = self.story.events

        if self.story.current_story == self.story.pre_story_lines:
            if self.last_event == 1:
                self.window.run_event(0, 0)
            elif self.last_event == 2:
                self.entities.remove(self.entities.get_items_by_class(intro_picture).first())
                self.continue_or_restart_time = True
                self.pause_loop = True
        elif self.story.current_story == self.story.pre_fight_story_before_first_snicker:
            if self.last_event >= 1 and self.last_event <= 8:
                self.window.run_event(1, self.last_event + 2)
        elif self.story.current_story == self.story.pre_fight_story_before_second_snicker:
            if self.last_event >= 1 and self.last_event <= 13:
                self.window.run_event(2, self.last_event + 2)
        elif self.story.current_story == self.story.pre_fight_story_before_walk:
            if self.last_event >= 1 and self.last_event <= 9:
                self.window.run_event(3, self.last_event - 1)
        elif self.story.current_story == self.story.pre_fight_story_before_fight:
            if self.last_event >= 1 and self.last_event <= 3:
                self.window.run_event(3, self.last_event + 8)

    def select_continue_or_restart(self) -> None:
        self.z_held = self.story.keyboard.is_z()

        if self.continue_or_restart:
            self.normal_font.say("Flowey    LV9999    9999:99\nMy World\n\n                Restart", 100, 170, False, None, 0)
            self.yellow_font.say("   Continue", 100, 284, False, None, 0)
        else:
            self.normal_font.say("Flowey    LV9999    9999:99\nMy World\n\n   Continue", 100, 170, False, None, 0)
            self.yellow_font.say("                Restart", 100, 284, False, None, 0)

        if self.continue_or_restart_held:
            if not self.story.keyboard.is_right() and not self.story.keyboard.is_left():
                self.continue_or_restart_held = False
        elif not self.continue_or_restart_held:
            if self.story.keyboard.is_right() or self.story.keyboard.is_left():
                self.continue_or_restart = not self.continue_or_restart
                self.continue_or_restart_held = True

        if not self.continue_or_restart_prepared:
            if self.z_held:
                return

            self.continue_or_restart_prepared = True

            return

        if self.z_held:
            if not self.continue_or_restart:
                self.continue_or_restart = True
                self.continue_or_restart_prepared = False
            else:
                self.normal_font.clear()
                self.yellow_font.clear()
                self.continue_or_restart_time = False
                self.window.run_event(0, 1)

class intro_picture(entity):
    def __init__(self, x: int, y: int, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.INTRO_SCREEN_ANIMATION, x, y, True, False)

        self.x -= self.width / 2
        self.y -= self.height / 2

    def update(self) -> None:
        pass

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

class file_backdrop(entity):
    def __init__(self, window, x: int, y: int, spritesheets: predef_spritesheets, effects: predef_effects) -> None:
        super().__init__(spritesheets.FILE_BACKDROP_ANIMATION, x, y, True, False)

        self.window = window
        self.spritesheets = spritesheets
        self.effects = effects

        self.font = None

        self.x -= self.width / 2
        self.y -= self.height / 2

        self.origin_x = self.x
        self.origin_y = self.y

        self.layer = 1000
        self.tick = 0
        self.cracks = None

    def hide(self) -> 'file_backdrop':
        self.visible = False

        return self

    def show(self) -> 'file_backdrop':
        self.visible = True

        return self

    def show_generated_font(self, name: str, font) -> None:
        if self.font == None:
            self.font = font

        output = name.lower().split(" ")[0] + "   LV1    409:20\nThe End\n{p=20}   Save      Return"

        self.font.say(output, 133, 110, False, None, 0)

    def update(self) -> None:
        self.x = self.origin_x + self.my_screen.x
        self.y = self.origin_y + self.my_screen.y

        if self.visible:
            self.font.update()
            self.tick += 1

            if self.tick == 180:
                self.cracks = file_cracks(self, self.x, self.y, self.spritesheets, self.effects)
                self.my_screen.shake_screen(50, 4)

            if self.cracks != None:
                self.cracks.update()

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

        if self.visible:
            self.font.render(screen)

            if self.cracks != None:
                self.cracks.render(screen)

class file_cracks(entity):
    def __init__(self, owner: file_backdrop, x: int, y: int, spritesheets: predef_spritesheets, effects: predef_effects) -> None:
        super().__init__(spritesheets.FILE_CRACKS_ANIMATION, x, y, True, False)

        self.owner = owner
        self.effects = effects

        self.x -= self.width / 2
        self.y -= self.height / 2
        self.x += self.owner.width / 2
        self.y += self.owner.height / 2

        self.origin_x = self.x
        self.origin_y = self.y

        self.layer = 1001
        self.tick = 0

        effects.PUNCH.play()

    def hide(self) -> 'file_cracks':
        self.visible = False

        return self

    def show(self) -> 'file_cracks':
        self.visible = True

        return self

    def update(self) -> None:
        self.tick += 1

        if self.tick == 90:
            self.animation.next()
            self.effects.PUNCH_SLOWER.play()
            self.origin_x += 2
            self.owner.font.clear()
            self.owner.animation.next()
            self.my_screen.shake_screen(55, 4)
        elif self.tick == 180:
            self.animation.next()
            self.effects.PUNCH_SLOWEST.play()
            self.origin_x += 28
            self.my_screen.shake_screen(65, 4)
        elif self.tick >= 330:
            self.my_screen.shake_screen(80, 4)
            self.owner.window.run_event(0, 3)

        self.x = self.origin_x + self.my_screen.x
        self.y = self.origin_y + self.my_screen.y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

class file_shattered(entity):
    def __init__(self, owner: file_backdrop, x: int, y: int, shatter_number: int, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.FILE_SHATTERED_ANIMATION, x, y, True, True)

        self.animation = self.animation.clear_all_but(shatter_number)

        self.x += owner.x + owner.width / 2 - self.width / 2
        self.y += owner.y + owner.height / 2 - self.height / 2

        self.origin_x = self.x
        self.origin_y = self.y

        self.center_x = owner.x + owner.width / 2
        self.center_y = owner.y
        self.speed_x = -((640 / 2 - self.width / 2 - self.origin_x) / 12) + randint(-2, 2)
        self.velocity_y = -((480 / 4 - self.height / 2 - self.origin_y) / 16) + randint(-3, 1)

        self.layer = 1002

    def hide(self) -> 'file_cracks':
        self.visible = False

        return self

    def show(self) -> 'file_cracks':
        self.visible = True

        return self

    def update(self) -> None:
        self.velocity_y += 0.5

        self.origin_x += self.speed_x
        self.origin_y += self.velocity_y

        self.x = self.origin_x + self.my_screen.x
        self.y = self.origin_y + self.my_screen.y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

class flowey_head(entity):
    def __init__(self, window, x: int, y: int, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.FLOWEY_ANIMATION, x, y, True, False)

        self.window = window
        self.x -= self.width / 2
        self.y -= self.height / 2
        self.rand_x = 0
        self.rand_y = 0
        self.origin_x = self.x
        self.origin_y = self.y
        self.shake = False
        self.visible = True
        self.move_to_top = False
        self.snicker = False
        self.slow = False
        self.layer = 998
        self.tick = 0
        self.tick_rand = 0

    def hide(self) -> 'flowey_head':
        self.visible = False

        return self

    def show(self) -> 'flowey_head':
        self.visible = True

        return self

    def flowey_snicker(self, slow: bool = False) -> None:
        self.snicker = True
        self.slow = slow
        self.tick = 265 if slow else 215

    def update(self) -> None:
        if self.animation.increment > 0:
            self.animation.update()

            if self.animation.index > 18:
                self.animation.set_current(9)

        if self.tick < 225 and not self.snicker:
            self.tick += 1

            if self.tick == 150:
                self.window.run_event(1, 0)
            elif self.tick == 165:
                self.move_to_top = True
            elif self.tick == 185:
                self.window.run_event(1, 1)
        elif self.tick == 225 and not self.snicker:
            self.tick += 1
            self.window.run_event(1, 2)

        if self.tick > 0 and self.snicker:
            self.tick -= 1

            if self.tick == (250 if self.slow else 200):
                self.window.run_event(2, 16 if self.slow else 0)
            elif self.tick == 15:
                self.window.run_event(2, 17 if self.slow else 1)
        elif self.tick == 0 and self.snicker:
            self.tick = 226
            self.window.run_event(2, 18 if self.slow else 2)
            self.snicker = False

        if self.move_to_top and self.y > 60:
            self.origin_y -= 5

        self.tick_rand += 1

        if self.tick_rand % 3 == 0:
            self.rand_x = randint(-1, 1) if self.shake else 0
            self.rand_y = randint(-1, 1) if self.shake else 0

        self.x = self.origin_x + self.rand_x
        self.y = self.origin_y + self.rand_y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

class flowey_static(entity):
    def __init__(self, owner: flowey_head, effects: predef_effects, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.STATIC_ANIMATION, 0, 0, False, False)

        self.owner = owner
        self.effects = effects
        self.x = self.owner.origin_x
        self.y = self.owner.origin_y
        self.force = False
        self.force_ticks = 0
        self.visible = False
        self.attempt = False
        self.chance = 800
        self.tick = 0
        self.layer = 999

    def hide(self) -> 'flowey_static':
        self.visible = False

        return self

    def show(self) -> 'flowey_static':
        self.visible = True

        return self

    def force_static(self, amount: int) -> None:
        self.force = True
        self.animation.reset()

        if amount == 0:
            self.force_ticks = 12
            self.effects.SHORT_STATIC.play()
        elif amount == 1:
            self.force_ticks = 25
            self.effects.SHORT_MEDIUM_STATIC.play()
        elif amount == 2:
            self.force_ticks = 40
            self.effects.MEDIUM_STATIC.play()
        elif amount == 3:
            self.force_ticks = 76
            self.effects.STATIC.play()


    def update(self) -> None:
        self.x = self.owner.origin_x - self.width / 2 + self.owner.width / 2
        self.y = self.owner.origin_y - self.height / 2 + self.owner.height / 2

        if self.force:
            self.show()
            self.animation.update()
            self.force_ticks -= 1

            if self.force_ticks <= 0:
                self.force = False
                self.force_ticks = 0
                self.hide()
        else:
            if not self.attempt:
                self.hide()

                return

            if not self.visible and randint(0, self.chance) == self.chance - 1:
                self.show()
                self.tick = 0
                self.animation.reset()
                self.effects.SHORT_STATIC.play()
            elif self.visible and self.tick < 15:
                self.animation.update()
                self.tick += 1
            elif self.visible and self.tick >= 15:
                self.hide()

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())