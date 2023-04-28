from pygame import Surface
from player import save_star
from sprites import predef_spritesheets
from sound import predef_effects
from fonts import story
from entity import entity, entity_collection
from random import randint

#These are what I wanted to accomplish before submitting the project; however, I did not have enough time sadly. It is now time to document my code.
#TODO: Add attacks.
#TODO: Add health bar.
#TODO: Add game over.
#TODO: Add different startup screens.

#This class handles the storyboard of the entire project. It takes the story and entities, forcing them to
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

    #Start the storyboard.
    def begin(self, effects: predef_effects, skip: int = 0) -> None:
        #Declare the storyboard as "running".
        self.running = True

        #If we are skipping nothing... (Starts at the Once Upon a Time Music)
        if skip == 0:
            #Start at the beginning.
            self.story.play(self.story.pre_story_lines)
        #Otherwise, if we are skipping 1 section... (Starts at the Character Control)
        elif skip == 1:
            #Pause the storyboard, run the first window event, and remove the introduction picture from the entities.
            self.pause_loop = True
            self.window.run_event(0, 1)
            self.entities.remove(self.entities.get_items_by_class(intro_picture).first())
        #Otherwise, if we are skipping 2 sections... (Starts at the File Exploding)
        elif skip == 2:
            #Pause the storyboard, run 3 consecutive window events, and remove the save star and introduction picture.
            self.pause_loop = True
            self.window.run_event(0, 1)
            self.window.run_event(0, 2)
            self.window.run_event(0, 3)
            self.entities.remove(self.entities.get_items_by_class(intro_picture).first())
            self.entities.remove(self.entities.get_items_by_class(save_star).first())
        #Otherwise, if we are skipping 3 sections... (Starts at the Soul Appearance)
        elif skip == 3:
            #Pause the storyboard, run 3 consecutive window events, and remove the save star and introduction picture.
            self.pause_loop = True
            self.window.run_event(0, 1)
            self.window.run_event(0, 2)
            self.window.run_event(0, 3)
            self.entities.remove(self.entities.get_items_by_class(intro_picture).first())
            self.entities.remove(self.entities.get_items_by_class(save_star).first())
            
            #Stop the sound for the explosion caused by the event (0, 3).
            effects.EXPLOSION.stop()

            #Run the appropriate event in the window.
            self.window.run_event(3, 11)

    def update(self) -> None:
        #Update the storyboard's entities.
        self.entities.update()

        #If the storyboard is running and is not paused...
        if self.running and not self.pause_loop:
            #Update the story and check if there are new events thrown.
            self.story.update()
            self.check_events()

        #If the storyboard is paused and the story reaches the continue-or-restart phase...
        if self.pause_loop and self.continue_or_restart_time:
            #Display and update according to the continue-or-restart phase's requirements.
            self.select_continue_or_restart()

            self.normal_font.update()
            self.yellow_font.update()

    def render(self, screen: Surface) -> None:
        #Render the storyboard's entities.
        self.entities.render(screen)

        #If the storyboard is running and is not paused...
        if self.running and not self.pause_loop:
            #Render the story.
            self.story.render(screen)

        #If the storyboard is paused and the story reaches the continue-or-restart phase...
        if self.pause_loop and self.continue_or_restart_time:
            #Render the text according to the continue-or-restart phase's requirements.
            self.normal_font.render(screen)
            self.yellow_font.render(screen)

    def check_events(self) -> None:
        #If there is no new event, stop here.
        if self.last_event == self.story.events or self.story.current_story == None:
            return

        #Set the last event called to the story's events.
        self.last_event = self.story.events

        #If the current story is the "Long ago..." text...
        if self.story.current_story == self.story.pre_story_lines:
            #If the last event called was 1...
            if self.last_event == 1:
                #Run the window event (0, 0).
                self.window.run_event(0, 0)
            #Events work in a similar way onwards. Documentation in these events will be brief.
            elif self.last_event == 2:
                self.entities.remove(self.entities.get_items_by_class(intro_picture).first())
                self.continue_or_restart_time = True
                self.pause_loop = True
        elif self.story.current_story == self.story.pre_fight_story_before_first_snicker:
            #Automates the next 8 events since they are so similar.
            if self.last_event >= 1 and self.last_event <= 8:
                #Run the event according to my offset specified (2).
                self.window.run_event(1, self.last_event + 2)
        elif self.story.current_story == self.story.pre_fight_story_before_second_snicker:
            if self.last_event >= 1 and self.last_event <= 13:
                #The offset here is also 2.
                self.window.run_event(2, self.last_event + 2)
        elif self.story.current_story == self.story.pre_fight_story_before_walk:
            if self.last_event >= 1 and self.last_event <= 9:
                #The offset here is -1.
                self.window.run_event(3, self.last_event - 1)
        elif self.story.current_story == self.story.pre_fight_story_before_fight:
            if self.last_event >= 1 and self.last_event <= 3:
                #The offset here is 8.
                self.window.run_event(3, self.last_event + 8)

    def select_continue_or_restart(self) -> None:
        #Verify initially if the Z key is being pressed.
        self.z_held = self.story.keyboard.is_z()

        #Display a different result depending on the current "continue_or_restart".
        if self.continue_or_restart:
            #This result means continue is selected and is yellow.
            self.normal_font.say("Flowey    LV9999    9999:99\nMy World\n\n                Restart", 100, 170, False, None, 0)
            self.yellow_font.say("   Continue", 100, 284, False, None, 0)
        else:
            #This result means restart is selected and is yellow.
            self.normal_font.say("Flowey    LV9999    9999:99\nMy World\n\n   Continue", 100, 170, False, None, 0)
            self.yellow_font.say("                Restart", 100, 284, False, None, 0)

        #Check if the left or right key is already held.
        if self.continue_or_restart_held:
            #Wait until the left or right key is not held.
            if not self.story.keyboard.is_right() and not self.story.keyboard.is_left():
                #Prepare for the left or right key to be pressed.
                self.continue_or_restart_held = False
        #Otherwise, if the left or right key is not held...
        elif not self.continue_or_restart_held:
            #If the left or right key is pressed...
            if self.story.keyboard.is_right() or self.story.keyboard.is_left():
                #Change to restart or continue depending on the current position.
                self.continue_or_restart = not self.continue_or_restart
                #State the key is being held.
                self.continue_or_restart_held = True

        #If Z is held prior to the screen appearing...
        if not self.continue_or_restart_prepared:
            #If the Z key is still held...
            if self.z_held:
                #Stop here.
                return

            #Otherwise, allow the Z key to be pressed.
            self.continue_or_restart_prepared = True

            #Stop here.
            return

        #If the Z key is held after verifying it is not held (this helps identify it as a keypress rather than a keydown).
        if self.z_held:
            #If restart is selected...
            if not self.continue_or_restart:
                #Shove the user back to the continue button.
                self.continue_or_restart = True
                #Wait for the user to release Z.
                self.continue_or_restart_prepared = False
            #Otherwise...
            else:
                #Clear the text.
                self.normal_font.clear()
                self.yellow_font.clear()
                #Exit the current screen.
                self.continue_or_restart_time = False
                #Broadcast the window event to allow the character to appear.
                self.window.run_event(0, 1)

#The sole purpose of this class is to show the introduction picture in the "Long ago..." story.
class intro_picture(entity):
    def __init__(self, x: int, y: int, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.INTRO_SCREEN_ANIMATION, x, y, True, False)

        #The x and y are already center-screen; however, to center the actual image based on its center, we need to subtract half the width and height of the picture from the x and y respectively.
        self.x -= self.width / 2
        self.y -= self.height / 2

    #Nothing to update here.
    def update(self) -> None:
        pass

    #Normal render.
    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

#This class shows the background of the file which says your name, location, save, return, etc.
class file_backdrop(entity):
    def __init__(self, window, x: int, y: int, spritesheets: predef_spritesheets, effects: predef_effects) -> None:
        super().__init__(spritesheets.FILE_BACKDROP_ANIMATION, x, y, True, False)

        #Typical initialization data.
        self.window = window
        self.spritesheets = spritesheets
        self.effects = effects

        self.font = None

        self.x -= self.width / 2
        self.y -= self.height / 2

        self.origin_x = self.x
        self.origin_y = self.y

        #Make sure it is in front of everything.
        self.layer = 1000
        self.tick = 0
        #The cracks for the "File Erased" portion.
        self.cracks = None

    #Hides the file.
    def hide(self) -> 'file_backdrop':
        self.visible = False

        return self

    #Shows the file.
    def show(self) -> 'file_backdrop':
        self.visible = True

        return self

    #Shows the text on the file.
    def show_generated_font(self, name: str, font) -> None:
        #If there is no font in the class, use the font provided in the parameter.
        if self.font == None:
            self.font = font

        #Lowers the name, splits it by a string, and gets the first result. Ex: "My Bob Billy Jeff" -> "my bob billy jeff" -> [ "my", "bob", "billy", "jeff" ] -> "my"
        #After retrieving the name, the other generic text is added to the file.
        output = name.lower().split(" ")[0] + "   LV1    409:20\nThe End\n{p=20}   Save      Return"
        
        #Say the output determined instantaneously.
        self.font.say(output, 133, 110, False, None, 0)

    def update(self) -> None:
        #Set the x and y of the text to the origin and the screen shaking.
        self.x = self.origin_x + self.my_screen.x
        self.y = self.origin_y + self.my_screen.y

        #If the file backdrop is visible...
        if self.visible:
            #Update the font.
            self.font.update()
            #Increase the generic tick.
            self.tick += 1

            #If the tick is 180 (3 seconds)...
            if self.tick == 180:
                #Create cracks and shake the screen with an intensity of 50 and a recovery of 4.
                self.cracks = file_cracks(self, self.x, self.y, self.spritesheets, self.effects)
                self.my_screen.shake_screen(50, 4)

            #If the cracks exist...
            if self.cracks != None:
                #Update the cracks.
                self.cracks.update()

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

        #If the backdrop is visible...
        if self.visible:
            #Render the font.
            self.font.render(screen)

            #If the cracks exist...
            if self.cracks != None:
                #Render the cracks.
                self.cracks.render(screen)

#This class shows the cracks of the file background and expands over time.
class file_cracks(entity):
    def __init__(self, owner: file_backdrop, x: int, y: int, spritesheets: predef_spritesheets, effects: predef_effects) -> None:
        super().__init__(spritesheets.FILE_CRACKS_ANIMATION, x, y, True, False)

        #Typical class initialization.
        self.owner = owner
        self.effects = effects

        #Adjust the x and y to be the center of the file backdrop.
        self.x -= self.width / 2
        self.y -= self.height / 2
        self.x += self.owner.width / 2
        self.y += self.owner.height / 2

        self.origin_x = self.x
        self.origin_y = self.y

        #Show the cracks in front of the file backdrop.
        self.layer = 1001
        self.tick = 0

        #The moment the class is intialized, play the punch sound effect.
        effects.PUNCH.play()

    #Hides the cracks.
    def hide(self) -> 'file_cracks':
        self.visible = False

        return self

    #Shows the cracks.
    def show(self) -> 'file_cracks':
        self.visible = True

        return self

    def update(self) -> None:
        #Increase the general ticks.
        self.tick += 1

        #If the ticks reach 90 (1.5 seconds)...
        if self.tick == 90:
            #Go to the next animation and play the slower punch effect.
            self.animation.next()
            self.effects.PUNCH_SLOWER.play()
            #Alter the x by 2 to remain in the center of the file background (for some reason it shoves it over 2).
            self.origin_x += 2
            #Clear the text from the file background.
            self.owner.font.clear()
            #Show "File Erased" on the file background.
            self.owner.animation.next()
            #Shake the screen with an intensity of 55 and a recovery of 4.
            self.my_screen.shake_screen(55, 4)
        #If the ticks reach 180 (another 1.5 seconds after the 90)...
        elif self.tick == 180:
            #Go to the next crack and repeat the above.
            self.animation.next()
            self.effects.PUNCH_SLOWEST.play()
            self.origin_x += 28
            self.my_screen.shake_screen(65, 4)
        #If the ticks reach 330 (5.5 seconds [2.5 seconds after the previous 180])...
        elif self.tick >= 330:
            #Shake the screen.
            self.my_screen.shake_screen(80, 4)
            #Run the explosion event in the window.
            self.owner.window.run_event(0, 3)

        #Shake the file's cracks according to the screen shaking.
        self.x = self.origin_x + self.my_screen.x
        self.y = self.origin_y + self.my_screen.y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

#This class appears once the file background explodes into shattered pieces.
class file_shattered(entity):
    def __init__(self, owner: file_backdrop, x: int, y: int, shatter_number: int, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.FILE_SHATTERED_ANIMATION, x, y, True, True)

        #Clear the animation of unnecessary shattered pieces to save on processing and memory (RAM).
        self.animation = self.animation.clear_all_but(shatter_number)

        #Position the shattered pieces according to the backdrop.
        self.x += owner.x + owner.width / 2 - self.width / 2
        self.y += owner.y + owner.height / 2 - self.height / 2

        self.origin_x = self.x
        self.origin_y = self.y

        self.center_x = owner.x + owner.width / 2
        self.center_y = owner.y
        #Sets the speed and velocity of it flying away according to where it is located on the screen along with a pinch of randomness.
        self.speed_x = -((640 / 2 - self.width / 2 - self.origin_x) / 12) + randint(-2, 2)
        self.velocity_y = -((480 / 4 - self.height / 2 - self.origin_y) / 16) + randint(-3, 1)

        #Place this in front of the backdrop and cracks.
        self.layer = 1002

    #Hide the shatter.
    def hide(self) -> 'file_shattered':
        self.visible = False

        return self

    #Show the shatter.
    def show(self) -> 'file_shattered':
        self.visible = True

        return self

    def update(self) -> None:
        #Change the y velocity by half a pixel every 1 UPS (this allows the y position to change faster over the course of time giving a "falling" sense).
        self.velocity_y += 0.5

        #Change the location of the shatter by the speed and velocity provided.
        self.origin_x += self.speed_x
        self.origin_y += self.velocity_y

        #Depend on the shaking of the screen to set the x and y coordinates.
        self.x = self.origin_x + self.my_screen.x
        self.y = self.origin_y + self.my_screen.y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

#This class is for the Flowey head which appears behind the exploded file background.
class flowey_head(entity):
    def __init__(self, window, x: int, y: int, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.FLOWEY_ANIMATION, x, y, True, False)

        #Typical class initialization.
        self.window = window
        self.x -= self.width / 2
        self.y -= self.height / 2
        self.rand_x = 0
        self.rand_y = 0
        self.origin_x = self.x
        self.origin_y = self.y
        #If this is true, Flowey will shake in a harsh manny, yet very little.
        self.shake = False
        #Flowey is not visible by default.
        self.visible = True
        #Moves Flowey to the top of the screen if this is True.
        self.move_to_top = False
        #Hides Flowey and plays a snicker sound effect if this is True.
        self.snicker = False
        #This determines if this is the slow or normal Flowey snicker.
        self.slow = False
        #Put Flowey behind the file background and the static.
        self.layer = 998
        self.tick = 0
        self.tick_rand = 0

    #Hide Flowey.
    def hide(self) -> 'flowey_head':
        self.visible = False

        return self

    #Show Flowey.
    def show(self) -> 'flowey_head':
        self.visible = True

        return self

    #Allows Flowey to snicker.
    def flowey_snicker(self, slow: bool = False) -> None:
        self.snicker = True
        self.slow = slow
        #If the snicker is slow, make the tick higher than normal so Flowey shows at a proper time again.
        self.tick = 265 if slow else 215

    def update(self) -> None:
        #If there is an increment for the animation...
        if self.animation.increment > 0:
            #Update the animation.
            self.animation.update()

            #If the animation is at the end of this hard-defined loop...
            if self.animation.index > 18:
                #Then set the animation back to the beginning of the hard-defined loop.
                self.animation.set_current(9)

        #If the generic tick is less than 225 and Flowey is not snickering...
        if self.tick < 225 and not self.snicker:
            #Increase the generic tick.
            self.tick += 1

            #If the generic tick is 150 (2.5 seconds)...
            if self.tick == 150:
                #Broadcast the window event.
                self.window.run_event(1, 0)
            #Otherwise, if the generic tick is 165 (1/4th second after 150)...
            elif self.tick == 165:
                #Move Flowey to the top of the screen.
                self.move_to_top = True
            #Otherwise, if the generic tick is 185 (1/3rd second after 165)...
            elif self.tick == 185:
                #Broadcast the window event.
                self.window.run_event(1, 1)
        #Otherwise, if the generic tick reaches the full 225 (3.75 seconds) and Flowey is not snickering...
        elif self.tick == 225 and not self.snicker:
            #Increase the generic tick.
            self.tick += 1
            #Broadcast the window event.
            self.window.run_event(1, 2)

        #If the generic tick is more than 0 and Flowey is snickering...
        if self.tick > 0 and self.snicker:
            #Decrease the generic tick.
            self.tick -= 1

            #If the tick passes by the respected 250 or 200 depending on if it is a slow snicker...
            if self.tick == (250 if self.slow else 200):
                #Run the specific window event depending on if the snicker is slow.
                self.window.run_event(2, 16 if self.slow else 0)
            #Otherwise, if the tick is 15 (1/4th second away from 0 [tick is decreasing])...
            elif self.tick == 15:
                #Run the specific window event depending on if the snicker is slow.
                self.window.run_event(2, 17 if self.slow else 1)
        #Otherwise, if the generic tick has hit 0 and Flowey is still snickering...
        elif self.tick == 0 and self.snicker:
            #Set the tick back to 226.
            self.tick = 226
            #Run the specific window event depending on if the snicker is slow.
            self.window.run_event(2, 18 if self.slow else 2)
            #Stop Flowey from snickering.
            self.snicker = False

        #If Flowey is being moved to the top and the y position is not appropriate...
        if self.move_to_top and self.y > 60:
            #Move upwards.
            self.origin_y -= 5

        #Increase the random tick.
        self.tick_rand += 1

        #If the random tick is an increment of 3...
        if self.tick_rand % 3 == 0:
            #Shake Flowey's head between -1 and 1 on both the x and y axis.
            #If Flowey is not yet shaking, set the random x and y to 0.
            self.rand_x = randint(-1, 1) if self.shake else 0
            self.rand_y = randint(-1, 1) if self.shake else 0

        #Adjust Flowey's head to the random x and y provided.
        self.x = self.origin_x + self.rand_x
        self.y = self.origin_y + self.rand_y

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())

#This class is for the static which goes in front of Flowey from time-to-time.
class flowey_static(entity):
    def __init__(self, owner: flowey_head, effects: predef_effects, spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.STATIC_ANIMATION, 0, 0, False, False)

        #Typical class initialization.
        self.owner = owner
        self.effects = effects
        self.x = self.owner.origin_x
        self.y = self.owner.origin_y
        #If this is true, it will force the static to appear.
        self.force = False
        #This is how long the statifc is forced to show.
        self.force_ticks = 0
        #The static is hidden by default.
        self.visible = False
        #If this is true, the static is allowed to attempt to take a random chance to show.
        self.attempt = False
        #There is a 1 in 800 chance of the static randomly appearing in each update (UPS).
        #Statistically, there should be static every 13.3 seconds.
        self.chance = 800
        self.tick = 0
        #Put the static in front of the Flowey head, but behind the file backdrop, cracks, and shatter.
        self.layer = 999

    #Hide the static.
    def hide(self) -> 'flowey_static':
        self.visible = False

        return self

    #Show the static.
    def show(self) -> 'flowey_static':
        self.visible = True

        return self

    #Force the static to appear for the "amount" of time provided (preset values, not ticks).
    def force_static(self, amount: int) -> None:
        #Force the static to appear.
        self.force = True
        #Reset the animation.
        self.animation.reset()

        #If the amount is 0, force the static to play for 12 ticks and play the SHORT_STATIC sound effect.
        if amount == 0:
            self.force_ticks = 12
            self.effects.SHORT_STATIC.play()
        #The following work in similar ways to the above. The tick amount is the length of time in ticks the sound effect is.
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
        #Set the x and y position according to the location of Flowey's head.
        self.x = self.owner.origin_x - self.width / 2 + self.owner.width / 2
        self.y = self.owner.origin_y - self.height / 2 + self.owner.height / 2

        #If the static is forced...
        if self.force:
            #Show the static and update the animation.
            self.show()
            self.animation.update()
            #Decrease the forced static ticks.
            self.force_ticks -= 1

            #If the ticks reach the end...
            if self.force_ticks <= 0:
                #Stop forcing the static and hide it.
                self.force = False
                self.force_ticks = 0
                self.hide()
        #Otherwise...
        else:
            #If the static is not allowed to attempt to show...
            if not self.attempt:
                #Then hide it.
                self.hide()

                #And stop here.
                return

            #If the static is not visible and the random chance is true...
            if not self.visible and randint(0, self.chance) == self.chance - 1:
                #Show the static and play it for only a short bout of time.
                self.show()
                self.tick = 0
                self.animation.reset()
                self.effects.SHORT_STATIC.play()
            #Otherwise, if the static is visible and the generic tick is less than 15 (1/4th second)...
            elif self.visible and self.tick < 15:
                #Update the animation and increase the generic ticks.
                self.animation.update()
                self.tick += 1
            #Otherwise, if the generic ticks exceed 15...
            elif self.visible and self.tick >= 15:
                #Hide the static.
                self.hide()

    def render(self, screen: Surface) -> None:
        screen.blit(self.get_sprite().image, self.get_data())