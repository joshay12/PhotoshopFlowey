from entity import entity, entity_collection
from sprites import predef_spritesheets
from input import keyboard
from sound import effect, predef_effects
from pygame import Surface

#This entity is the save star found when the character walks up for a brief period of time.
class save_star(entity):
    def __init__(self, x: int, y: int, entities: entity_collection, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.SAVE_STAR_ANIMATION, x, y, True, False)

        #Hook up the character to the entity.
        self.character = entities.get_items_by_class(character).first()
        self.x -= self.width / 2
        self.y -= self.height / 2
        self.origin_y = self.y
        self.layer = 1

    def update(self) -> None:
        self.animation.update()

        #When updating, the y position is dependent on the character's current position with the screen scrolling.
        self.y = self.origin_y - self.character.screen_scroll

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

#This is the character entity that looks like a kid. This is controllable by the user.
class character(entity):
    def __init__(self, window, x: int, y: int, screen_width: int, screen_height: int, keyboard: keyboard, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.PLAYER_DOWN_ANIMATION, x, y, False, False)

        #Initialize the data of the character.
        self.window = window
        #This is the speed of the character.
        self.speed = 3
        #These four animations hold the player's animations for the direction they are facing.
        self.down = spritesheets.PLAYER_DOWN_ANIMATION
        self.up = spritesheets.PLAYER_UP_ANIMATION
        self.left = spritesheets.PLAYER_LEFT_ANIMATION
        self.right = spritesheets.PLAYER_RIGHT_ANIMATION
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.keyboard = keyboard
        #This is used to scroll the screen for the save star.
        self.screen_scroll = 0
        #The character is not visible by default.
        self.visible = False
        #The character can move by default.
        self.run_controls = True
        #If the character is shoved to the bottom of the screen, this is True.
        self.move_to_bottom = False
        #If the character moves up just a smudged, this is True
        self.move_up_slightly = False
        #This is true if the Z key is held.
        self.z_prepared = False
        self.x -= self.width / 2
        self.y -= self.height / 2
        self.origin_x = self.x
        self.origin_y = self.y
        self.layer = 2
        self.ending_discussion_tick = 0

    #Set the character's save star.
    def set_save_star(self, entities: entity_collection) -> 'character':
        self.entities = entities
        self.star = entities.get_items_by_class(save_star).first()

        return self

    #Set the healing sound in the character.
    def set_heal_effect(self, sound: effect) -> 'character':
        self.heal_sound = sound

        return self

    def update(self) -> None:
        #If the player is not visible or the character cannot move...
        if not self.visible or not self.run_controls:
            #Reset the animation.
            self.animation.set_current(0)

            #Affect the character by the screen shaking.
            self.x = self.origin_x + self.my_screen.x
            self.y = self.origin_y + self.my_screen.y

            #If we move the character slightly and we don't meet the y position required...
            if self.move_up_slightly and self.origin_y > 335:
                #Move upwards.
                self.origin_y -= 5
            #Otherwise if we meet the y position required...
            elif self.move_up_slightly and self.origin_y <= 335:
                #Increase the ticks for the ending discussion.
                self.ending_discussion_tick += 1
            #If we move the player to the bottom of the screen and we don't meet the y positions and we aren't moving up...
            elif self.move_to_bottom and self.origin_y < 360 and not self.move_up_slightly:
                #Move downwards.
                self.origin_y += 8

                #Center the player in the x-coordinate.
                if self.origin_x < 640 / 2 - self.width / 2 - 4:
                    self.origin_x += 4
                elif self.origin_x > 640 / 2 - self.width / 2 + 4:
                    self.origin_x -= 4

            #If our ending discussion tick is at 60 (1 second)...
            if self.ending_discussion_tick == 60:
                #Then run the window event.
                self.window.run_event(3, 8)

            #Prevent the character from having controls.
            return

        self.origin_x = self.x
        self.origin_y = self.y

        self.animation.update()

        x = 0
        y = 0

        #If the Z key is pressed and not prepared...
        if not self.z_prepared:
            #If the keyboard is not pressing Z...
            if not self.keyboard.is_z():
                #Then say the Z key is prepared to be pressed.
                self.z_prepared = True
        #Otherwise...
        else:
            #If the keyboard is pressing Z...
            if self.keyboard.is_z():
                #Check if we are an appropriate distance away from the save star...
                if self.distance_from_entity(self.star) <= 55.0:
                    #If we are, then play a sound, delete the star, stop the controls, and broadcast an event in the window.
                    self.heal_sound.play(1.0, 1.0, 1.0, 0)
                    self.entities.remove(self.star)
                    self.window.run_event(0, 2)
                    self.run_controls = False
                #Otherwise...
                else:
                    #Make the Z key to be not prepared.
                    self.z_prepared = False

        #Basic controls.
        if self.keyboard.is_up():
            y = -self.speed
            self.animation = self.up
        elif self.keyboard.is_down():
            y = self.speed
            self.animation = self.down
        
        #Splitting the if statements allows for diagonal movement.
        if self.keyboard.is_left():
            x = -self.speed
            self.animation = self.left
        elif self.keyboard.is_right():
            x = self.speed
            self.animation = self.right

        #If we are not moving...
        if x == 0 and y == 0:
            #Reset the animation.
            self.animation.set_current(0)
            self.animation.increment = 0
        #Otherwise...
        else:
            #Animate at 12 ticks per frame.
            self.animation.increment = 12

        #Adjust the layer of the character according to if it is above or below the save star.
        self.layer = 2 if self.y > self.star.y - 16 else 0
        #Sort the entities by their layers.
        self.entities.sort()
        
        #If we are not moving the y position...
        if y != 0:
            #If we are colliding with the save star...
            if self.x + x > self.star.x - self.width and self.x + x < self.star.x + self.star.width and self.y + y > self.star.y - self.height + 16 and self.y + y < self.star.y:
                #Then stop the character from moving and reset the animation.
                y = 0
                self.animation.set_current(0)

        #This is the same, but on the x position.
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

        #This is a basic collision detector to prevent the player from exiting the screen.
        if self.x > self.screen_width - self.width + 4:
            self.x = self.screen_width - self.width + 4
        elif self.x < 0:
            self.x = 0

        #The if statements are split to allow for both an x and y collision to be detected.
        if self.y > self.screen_height - self.height:
            self.y = self.screen_height - self.height
        elif self.y < 0:
            self.y = 0

        self.origin_x = self.x
        self.origin_y = self.y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

#This is the soul of the character and is the actual player. This is what will be affected during the fight.
class soul(entity):
    def __init__(self, my_screen, skipped: bool, window, owner: character, keyboard: keyboard, effects: predef_effects, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.PLAYER_SOUL_ANIMATION, owner.x, owner.y, True, False)

        #Typical class setup.
        self.my_screen = my_screen
        self.window = window
        self.owner = owner
        self.keyboard = keyboard
        self.effects = effects

        self.x -= self.width / 2 - self.owner.width / 2 + 1
        self.y -= self.height / 2 - self.owner.height / 2 - 14

        self.origin_x = self.x
        self.origin_y = self.y

        #The speed of the soul is 3.
        self.speed = 3
        #Our generic tick is dependent on if we skipped to the portion when the soul appears or not.
        self.tick = 0 if not skipped else -60
        #Start the soul without allowing the user to control it.
        self.controls = False
        #If the soul has been sent to its proper location, this will be True.
        self.prepare = True
        #If the soul is needs to be sent to its proper location, this will be True.
        self.send = False
        #If the soul is moving to its proper location, this will be True.
        self.move_to_position = False
        #The soul is not visible initially.
        self.visible = False
        #The soul is in front of the character.
        self.layer = 3

    def update(self) -> None:
        #If we can't control the player...
        if not self.controls:
            #If we are still preparing the player...
            if self.prepare:
                #Increase our generic tick by 1.
                self.tick += 1

                #If we are under 0, stop there.
                if self.tick < 0:
                    return

                #This is used to determine how many ticks should it take to flicker.
                increment = 8

                #If the soul has not flickered yet...
                if not self.send:
                    #If the generic tick is an increment of our increment (8)...
                    if self.tick % increment == 0:
                        #Then hide it.
                        self.visible = False
                    #Otherwise, if the generic tick is an increment of our increment divided by 2 (8 -> 4)...
                    elif self.tick % increment == int(increment / 2):
                        #Then show it and play the prepare sound.
                        self.visible = True
                        self.effects.SOUL_PREPARE.play()

                    #If the tick is beyond triple our increment (24)...
                    if self.tick >= increment * 3:
                        #Then prepare to send the player and show it.
                        self.send = True
                        self.visible = True
                #Otherwise, if the generic tick is an increment of half of our increment (8 -> 4) and is not moving to position yet...
                elif self.tick % increment == 3 and not self.move_to_position:
                    #Play the sending to battle sound, broadcast an event, and move the player.
                    self.effects.SOUL_SEND_TO_BATTLE.play()
                    self.move_to_position = True
                    self.window.run_event(4, 0)
                #Otherwise, if we need to move the player and it isn't at the proper position...
                elif self.move_to_position and self.origin_y < 400:
                    #Move downwards.
                    self.origin_y += 1.75
                    self.tick = 0
                #Otherwise, if we are at the proper location...
                elif self.origin_y >= 400:
                    #If our generic tick count reaches 60 (1 second).
                    if self.tick == 60:
                        #Then finish preparation and broadcast an event.
                        self.window.run_event(4, 1)
                        self.prepare = False

            #Make the x and y of the player dependent on the screen shaking.
            self.x = self.origin_x + self.my_screen.x
            self.y = self.origin_y + self.my_screen.y

            return

        x = 0
        y = 0

        #This adds a basic control to the player.
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

        #This adds a basic collision to be within the embrace of Flowey.
        if self.origin_x < 640 / 2 - 200 - self.width:
            self.origin_x = 640 / 2 - 200 - self.width
        elif self.origin_x > 640 / 2 + 200:
            self.origin_x = 640 / 2 + 200

        if self.origin_y < 480 / 2 + 20:
            self.origin_y = 480 / 2 + 20
        elif self.origin_y > 480 - self.height:
            self.origin_y = 480 - self.height

        #Make the x and y of the player dependent on the screen shaking.
        self.x = self.origin_x + self.my_screen.x
        self.y = self.origin_y + self.my_screen.y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

#These are the 6 Flowey souls.
class soul_npc(entity):
    def __init__(self, window, x: int, y: int, soul_number: int, effects: predef_effects, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.NPC_SOULS_ANIMATION, x, y, True, True)

        #We set up the soul depending on the soul_number provided.
        self.animation.set_current(soul_number)

        self.window = window
        self.effects = effects
        self.soul_number = soul_number

        self.x -= self.width / 2
        self.y -= self.height / 2

        self.origin_x = self.x
        self.origin_y = self.y

        self.speed = 2
        #We allow the souls to appear at different times (one after another).
        self.tick = self.soul_number * -16
        #Whether or not the souls are heading to their locations.
        self.send = False
        #Whether or not the souls are ready to head to their locations.
        self.ready = False
        #If the souls are fading, this will be true.
        self.fade = False
        #If the souls are completely faded and hidden, this will be true.
        self.finished = False
        #Initially make the souls show fully.
        self.opacity = 255
        #Initially hide the souls.
        self.visible = False
        self.layer = 3

    def update(self) -> None:
        #Wait until the general tick is 0 or higher to continue.
        if self.tick < 0:
            self.tick += 1
            return

        #This is the flicker increment (the same as the player's soul).
        increment = 8

        #If the soul is not ready to be sent...
        if not self.ready:
            #Increase the generic tick.
            self.tick += 1

            #This is the same as the player's soul. Review the player soul's documentation to understand further.
            if self.tick % increment == 0:
                self.visible = False
            elif self.tick % increment == int(increment / 2):
                self.visible = True
                self.effects.SOUL_PREPARE.play()

            if self.tick >= increment * 3:
                self.visible = True
                self.ready = True
                #We set the tick according to the soul number so they send at the same time.
                self.tick = (80 - self.soul_number * 16) + 25
        #Otherwise, if the soul is not sent yet...
        elif not self.send:
            #Decrease the generic tick.
            self.tick -= 1

            #Once the tick hits 0...
            if self.tick == 0:
                #If the soul is the first one...
                if self.soul_number == 0:
                    #Broadcast an event to the window.
                    self.window.run_event(4, 2)
                
                #Send the souls.
                self.send = True
        #Otherwise, if the soul is not fading yet...
        elif self.send and not self.fade:
            #Increase the generic tick.
            self.tick += 1

            #If the tick amount is less than 20...
            if self.tick < 20:
                #Change the position of the soul based on where it is located.
                self.origin_x += -self.speed if self.origin_x < 640 / 2 else self.speed
                self.origin_y += (-self.speed if self.origin_y < 150 else 0) if self.origin_y < 154 else self.speed
            #Otherwise, if the tick is 20...
            elif self.tick == 20:
                #Then begin to fade.
                self.fade = True
        #Otherwise, if the soul is not finished fading...
        elif self.fade and not self.finished:
            #Lessen the transparency.
            self.opacity -= 12

            #If the opacity is less than the minimum.
            if self.opacity < 0:
                #Finish the soul up.
                self.opacity = 0
                self.visible = False
                self.finished = True
                self.tick = 0

            #Change the opacity of the sprite.
            self.get_sprite().change_opacity(self.opacity)
        #Otherwise, if the soul is finished and is the first one...
        elif self.finished and self.soul_number == 0:
            #Increase the generic tick.
            self.tick += 1

            #When 60 ticks pass (1 second)...
            if self.tick == 60:
                #Broadcast the event to the window.
                self.window.run_event(4, 3)

        self.x = self.origin_x
        self.y = self.origin_y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())