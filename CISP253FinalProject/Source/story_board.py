from pygame import Surface
from sprites import predef_spritesheets
from sound import predef_effects
from fonts import story
from entity import entity, entity_collection

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

    def begin(self, skip: int = 0) -> None:
        self.running = True

        if skip == 0:
            self.story.play(self.story.pre_story_lines)
        elif skip == 1:
            self.pause_loop = True
            self.window.run_event(0, 1)
            self.entities.remove(self.entities.get_items_by_class(intro_picture).first())

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
    def __init__(self, x: int, y: int, spritesheets: predef_spritesheets, effects: predef_effects) -> None:
        super().__init__(spritesheets.FILE_BACKDROP_ANIMATION, x, y, True, False)

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
            self.owner.font.say("{c=True}", 0, 0, speed = 0)
            self.owner.animation.next()
            self.my_screen.shake_screen(55, 4)
        elif self.tick == 180:
            self.animation.next()
            self.effects.PUNCH_SLOWEST.play()
            self.origin_x += 28
            self.my_screen.shake_screen(65, 4)

        self.x = self.origin_x + self.my_screen.x
        self.y = self.origin_y + self.my_screen.y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())