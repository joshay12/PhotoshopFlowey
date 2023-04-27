from entity import entity, entity_collection
from sprites import predef_spritesheets
from input import keyboard
from sound import effect, predef_effects
from pygame import Surface

class save_star(entity):
    def __init__(self, x: int, y: int, entities: entity_collection, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.SAVE_STAR_ANIMATION, x, y, True, False)

        self.character = entities.get_items_by_class(character).first()
        self.x -= self.width / 2
        self.y -= self.height / 2
        self.origin_y = self.y
        self.layer = 1

    def update(self) -> None:
        self.animation.update()

        self.y = self.origin_y - self.character.screen_scroll

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

class character(entity):
    def __init__(self, window, x: int, y: int, screen_width: int, screen_height: int, keyboard: keyboard, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.PLAYER_DOWN_ANIMATION, x, y, False, False)

        self.window = window
        self.speed = 3
        self.down = spritesheets.PLAYER_DOWN_ANIMATION
        self.up = spritesheets.PLAYER_UP_ANIMATION
        self.left = spritesheets.PLAYER_LEFT_ANIMATION
        self.right = spritesheets.PLAYER_RIGHT_ANIMATION
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.keyboard = keyboard
        self.screen_scroll = 0
        self.visible = False
        self.run_controls = True
        self.move_to_bottom = False
        self.move_up_slightly = False
        self.z_prepared = False
        self.x -= self.width / 2
        self.y -= self.height / 2
        self.origin_x = self.x
        self.origin_y = self.y
        self.layer = 2
        self.ending_discussion_tick = 0

    def set_save_star(self, entities: entity_collection) -> 'character':
        self.entities = entities
        self.star = entities.get_items_by_class(save_star).first()

        return self

    def set_heal_effect(self, sound: effect) -> 'character':
        self.heal_sound = sound

        return self

    def update(self) -> None:
        if not self.visible or not self.run_controls:
            self.animation.set_current(0)

            self.x = self.origin_x + self.my_screen.x
            self.y = self.origin_y + self.my_screen.y

            if self.move_up_slightly and self.origin_y > 335:
                self.origin_y -= 5
            elif self.move_up_slightly and self.origin_y <= 335:
                self.ending_discussion_tick += 1
            elif self.move_to_bottom and self.origin_y < 360 and not self.move_up_slightly:
                self.origin_y += 8

                if self.origin_x < 640 / 2 - self.width / 2 - 4:
                    self.origin_x += 4
                elif self.origin_x > 640 / 2 - self.width / 2 + 4:
                    self.origin_x -= 4

            if self.ending_discussion_tick == 60:
                self.window.run_event(3, 8)

            return

        self.origin_x = self.x
        self.origin_y = self.y

        self.animation.update()

        x = 0
        y = 0

        if not self.z_prepared:
            if not self.keyboard.is_z():
                self.z_prepared = True
        else:
            if self.keyboard.is_z():
                if self.distance_from_entity(self.star) <= 55.0:
                    self.heal_sound.play(1.0, 1.0, 1.0, 0)
                    self.entities.remove(self.star)
                    self.window.run_event(0, 2)
                    self.run_controls = False
                else:
                    self.z_prepared = False

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

        self.layer = 2 if self.y > self.star.y - 16 else 0
        self.entities.sort()
        
        if y != 0:
            if self.x + x > self.star.x - self.width and self.x + x < self.star.x + self.star.width and self.y + y > self.star.y - self.height + 16 and self.y + y < self.star.y:
                y = 0
                self.animation.set_current(0)

        if x != 0:
            if self.x + x > self.star.x - self.width and self.x + x < self.star.x + self.star.width and self.y + y > self.star.y - self.height + 16 and self.y + y < self.star.y:
                x = 0
                self.animation.set_current(0)

        self.x += x

        #This is my elaborate solution for screen scrolling.
        #If the character is at the bottom of the scrolling screen...
        if self.screen_scroll >= 0:
            #And the player is still going down...
            if y > 0:
                #Increase the actual y of the player.
                self.y += y
            #Otherwise, if the player is going up...
            elif y < 0:
                #And the player is at half the height of the screen...
                if self.y < self.screen_height / 2 - self.height / 2:
                    #Increase the screen scroll accordingly.
                    self.screen_scroll += y
                #Otherwise...
                else:
                    #Increase the y position accordingly.
                    self.y += y
        #This elif performs the same operations as the previous if, except it does the operations for exceeding the top of the screen rather than the bottom.
        elif self.screen_scroll <= -700:
            if y < 0:
                self.y += y
            elif y > 0:
                if self.y > self.screen_height / 2 - self.height / 2:
                    self.screen_scroll += y
                else:
                    self.y += y
        #Otherwise, if we are between the top and bottom, just affect the screen scroll.
        else:
            self.screen_scroll += y

        if self.x > self.screen_width - self.width + 4:
            self.x = self.screen_width - self.width + 4
        elif self.x < 0:
            self.x = 0

        if self.y > self.screen_height - self.height:
            self.y = self.screen_height - self.height
        elif self.y < 0:
            self.y = 0

        self.origin_x = self.x
        self.origin_y = self.y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

class soul(entity):
    def __init__(self, skipped: bool, window, owner: character, keyboard: keyboard, effects: predef_effects, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.PLAYER_SOUL_ANIMATION, owner.x, owner.y, True, False)

        self.window = window
        self.owner = owner
        self.keyboard = keyboard
        self.effects = effects

        self.x -= self.width / 2 - self.owner.width / 2 + 1
        self.y -= self.height / 2 - self.owner.height / 2 - 14

        self.origin_x = self.x
        self.origin_y = self.y

        self.speed = 4
        self.tick = 0 if not skipped else -60
        self.controls = False
        self.prepare = True
        self.send = False
        self.move_to_position = False
        self.visible = False
        self.layer = 3

    def update(self) -> None:
        if not self.controls:
            if self.prepare:
                self.tick += 1

                if self.tick < 0:
                    return

                increment = 8

                if not self.send:
                    if self.tick % increment == 0:
                        self.visible = False
                    elif self.tick % increment == int(increment / 2):
                        self.visible = True
                        self.effects.SOUL_PREPARE.play()

                    if self.tick >= increment * 3:
                        self.send = True
                        self.visible = True
                elif self.tick % increment == 3 and not self.move_to_position:
                    self.effects.SOUL_SEND_TO_BATTLE.play()
                    self.move_to_position = True
                    self.window.run_event(4, 0)
                elif self.move_to_position and self.origin_y < 400:
                    self.origin_y += 1.75
                    self.tick = 0
                elif self.origin_y >= 400:
                    if self.tick == 60:
                        self.window.run_event(4, 1)
                        self.prepare = False

                self.x = self.origin_x
                self.y = self.origin_y

            return

        x = 0
        y = 0

        if self.keyboard.is_up():
            y = -self.speed
        elif self.keyboard.is_down():
            y = self.speed
        
        if self.keyboard.is_left():
            x = -self.speed
        elif self.keyboard.is_right():
            x = self.speed

        self.origin_x += x
        self.origin_y += y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

class soul_npc(entity):
    def __init__(self, window, x: int, y: int, soul_number: int, effects: predef_effects, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.NPC_SOULS_ANIMATION, x, y, True, True)

        self.animation.set_current(soul_number)

        self.window = window
        self.effects = effects
        self.soul_number = soul_number

        self.x -= self.width / 2
        self.y -= self.height / 2

        self.origin_x = self.x
        self.origin_y = self.y

        self.speed = 2
        self.tick = self.soul_number * -16
        self.send = False
        self.ready = False
        self.fade = False
        self.finished = False
        self.opacity = 255
        self.visible = False
        self.layer = 3

    def update(self) -> None:
        if self.tick < 0:
            self.tick += 1
            return

        increment = 8

        if not self.ready:
            self.tick += 1

            if self.tick % increment == 0:
                self.visible = False
            elif self.tick % increment == int(increment / 2):
                self.visible = True
                self.effects.SOUL_PREPARE.play()

            if self.tick >= increment * 3:
                self.visible = True
                self.ready = True
                self.tick = (80 - self.soul_number * 16) + 25
        elif not self.send:
            self.tick -= 1

            if self.tick == 0:
                if self.soul_number == 0:
                    self.window.run_event(4, 2)
                
                self.send = True
        elif self.send and not self.fade:
            self.tick += 1

            if self.tick < 20:
                self.origin_x += -self.speed if self.origin_x < 640 / 2 else self.speed
                self.origin_y += (-self.speed if self.origin_y < 150 else 0) if self.origin_y < 154 else self.speed
            elif self.tick == 20:
                self.fade = True
        elif self.fade and not self.finished:
            self.opacity -= 12

            if self.opacity < 0:
                self.opacity = 0
                self.visible = False
                self.finished = True
                self.tick = 0

            self.get_sprite().change_opacity(self.opacity)
        elif self.finished and self.soul_number == 0:
            self.tick += 1

            if self.tick == 60:
                self.window.run_event(4, 3)

        self.x = self.origin_x
        self.y = self.origin_y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())