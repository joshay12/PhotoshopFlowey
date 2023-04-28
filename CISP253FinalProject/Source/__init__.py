from input import keyboard
from sprites import predef_spritesheets, SPRITESHEETS
from entity import *
from flowey import flowey, white_overlay, flowey_face, dark_piece
from fonts import story, fonts_init
from sound import predef_effects, predef_songs, EFFECTS, SONGS
from story_board import story_board, intro_picture, file_backdrop, file_shattered, flowey_head, flowey_static
from player import character, save_star, soul, soul_npc
from getpass import getuser
from math import sin
import pygame, random

#This is the pygame screen stored globally.
GLOBAL_SCREEN = None
#This is the in-game screen stored globally to assist with screen shakes.
MY_SCREEN = None

#The window class is specifically dedicated to running the game window as well as broadcasting events to any entity within the game.
class window:
    def __init__(self, title: str) -> None:
        #Connect global variables to prepare for initialization.
        global GLOBAL_SCREEN, MY_SCREEN, SPRITESHEETS, EFFECTS, SONGS

        #Initialize pygame and start the sound handler with 16 possible channels (a lot, but I kept running out and got tired of it).
        pygame.init()
        pygame.mixer.init(channels = 16)

        #Make the window be 640x480 and set the title to what was provided when calling the window.
        self.title = title
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption(self.title)

        #Initialize this py file's global variables.
        GLOBAL_SCREEN = self.screen
        MY_SCREEN = my_screen()

        #Send the in-game screen global variables to the entities and fonts to assist in screen shaking.
        entity_init(MY_SCREEN)
        fonts_init(MY_SCREEN)

        #Initialize the global variables within other py files.
        SPRITESHEETS = predef_spritesheets(self.screen)
        EFFECTS = predef_effects()
        SONGS = predef_songs()

        #This is used to determine the red color of the filling background of the screen. It ranges from 0 (black) to 100 (dimmed red).
        self.red = 0
        #Whether the red color above is increasing or decreasing.
        self.red_increase = True
        #This variable assists the program in knowing when to flicker the screen red and black (using above variables) when True.
        self.begin_fight = False
        #This variable will force the screen to gradually revert back to black when True.
        self.stop_red = False
        #This variable determines if the F4 key is being held.
        self.f4 = False
        #Whether or not the entire program is running (this is for the game-loop).
        self.running = False
        #Initialize the keyboard, pygame clock, and the overall entities within the screen.
        self.keyboard = keyboard()
        self.clock = pygame.time.Clock()
        self.entities = entity_collection()
        #Add the initial entities to their respective positions, with their visibility, spritesheets, and effects.
        self.entities.add(intro_picture(640 / 2, 480 / 3, SPRITESHEETS))
        self.entities.add(file_backdrop(self, 640 / 2, 150, SPRITESHEETS, EFFECTS).hide())
        self.entities.add(character(self, 640 / 2, 480 - 480 / 3, self.screen.get_width(), self.screen.get_height(), self.keyboard, SPRITESHEETS))
        self.entities.add(save_star(640 / 2, -350, self.entities, SPRITESHEETS))
        #Since the character and save_star both rely on each other, I had the save_star get the character first, then the character get the save_star with this line.
        self.entities.get_items_by_class(character).first().set_save_star(self.entities).set_heal_effect(EFFECTS.HEAL)
        #Start up Flowey (very slow loading time due to approximately 300 MB of RAM to load).
        self.flowey = flowey(self, MY_SCREEN, SPRITESHEETS, 0, -475)
        #Initialize the storyboard of the game.
        self.board = story_board(story(SPRITESHEETS, EFFECTS, self.keyboard), self.entities, self)

        #A general tick for keeping track of time within the game.
        self.tick = 0

    #Run the game.
    def run(self) -> None:
        #Connect the global variables for the in-game screen and sound effects.
        global MY_SCREEN, EFFECTS

        #The game is now running. If this is set to false, the game will exit.
        self.running = True

        #Prepare for the loop.
        delta_time = 0.0
        updates_per_second = 60
        tick = 0

        #As long as the game-loop is running...
        while self.running:
            #Loop through pygame's events...
            for event in pygame.event.get():
                #If the event is exiting the pygame...
                if event.type == pygame.QUIT:
                    #Close the game-loop.
                    self.running = False
            
            #Update the keys in the keyboard class.
            self.keyboard.update_keys()

            #Handle updates always being at 60 UPS. The game could be at 20 FPS or 1,000,000 FPS; however, the UPS should always be 60 to give consistent input and output.
            #Note: This does NOT render to the screen; that is FPS. UPS just handles input and output.
            delta_time += self.clock.tick() / 1000.0

            while delta_time >= 1.0 / updates_per_second:
                #Class the update function.
                self.update(MY_SCREEN)

                delta_time -= 1.0 / updates_per_second

            #If the story has not started and the game is almost done sputtering from loading (tick == 5 helps)...
            if not self.board.running and tick == 5:
                #Start playing the STORY song at a lower pitch and begin the storyboard.
                SONGS.STORY.play(pitch = 0.9, loops = 0)
                self.board.begin(EFFECTS, 0) #INSERT NUMBER HERE TO SKIP TO CERTAIN PORTION OF STORY. 0 = Start; 1 = Character Control; 2 = File Explode; 3 = Pre-flowey Fight

            tick += 1

            #Now while we are not catching up or are ahead of updates, render the screen no matter what.
            self.render()

        #Once the game-loop is done, exit the game.
        pygame.quit()

    def update(self, my_screen: 'my_screen') -> None:
        #Update the in-game screen, storyboard, and flowey.
        self.board.update()
        self.flowey.update()
        
        my_screen.update()

        #If F4 is being pressed...
        if self.keyboard.is_f4() and not self.f4:
            #Toggle the game's fullscreen.
            pygame.display.toggle_fullscreen()

            self.f4 = True
        #Then wait for the F4 key to be released before checking to toggle the fullscreen again.
        elif self.f4 and not self.keyboard.is_f4():
            self.f4 = False

        #If we are revealing flowey and the red is not stopped...
        if self.begin_fight and not self.stop_red:
            #Wait until the tick is 0 (60 ticks = 1 second).
            if self.tick > 0:
                self.tick -= 1

                return

            #If the red is increasing, then increase it by 8; otherwise, do the opposite.
            self.red += 8 if self.red_increase else -8

            #If we've exceeded the maximum red set (100)...
            if self.red_increase and self.red > 100:
                #Then flip the increase to decrease, pause for 20 ticks (1/3 second), and set red to 100 to prevent it from going over the maximum.
                self.red = 100
                self.tick = 20
                self.red_increase = False
            #Otherwise, if we've exceeded the minimum red set (0)...
            elif not self.red_increase and self.red < 0:
                #Then flip the decrease to increase and set red to 0 to prevent it from going under the minimum.
                self.red = 0
                self.red_increase = True
        #Otherwise, if Flowey has been revealed and we need to stop red from flashing...
        elif self.red > 0 and self.stop_red:
            #Then just decrease the red.
            self.red -= 8

            #If it goes beyond 0 (black), then set it back to 0.
            if self.red < 0:
                self.red = 0

    def render(self) -> None:
        #Clear the screen with black (or dimmed red if the red color is changed.)
        self.screen.fill((self.red, 0, 0))

        #Render the storyboard and Flowey, passing in our screen to render to in the functions.
        self.board.render(self.screen)
        self.flowey.render(self.screen)

        #Display the screen pixels.
        pygame.display.flip()

    #This is a semi-complicated function dedicated to handling events throughout the entire game.
    #Since this py file contains the entirety of the project, it was placed within our window class.
    #Documentation will be moderate rather than thorough here as the format somewhat explains itself after some time.
    def run_event(self, story_number: int, event_number: int) -> None:
        #Connect our songs, sound effects, and in-game screen to this function.
        global SONGS, EFFECTS, MY_SCREEN

        #The pattern is if the story is 0 (such as the category for the story; perhaps 0 means: During the opening before the character appears), then check the event.
        #The event is more specific. If a certain event is called within a story, then it will run the contents for that event.
        if story_number == 0:
            #This event is when the game freezes at the start.
            if event_number == 0:
                SONGS.STORY.stop()
                SONGS.STORY_FROZEN.play(pitch = 0.84)

                self.entities.get_items_by_class(intro_picture).first().animation.set_current(1)
            #This event stops the frozen song and makes the character appear and is playable.
            elif event_number == 1:
                SONGS.STORY_FROZEN.stop()

                self.entities.get_items_by_class(character).first().visible = True
            #This event displays the file information of the player.
            elif event_number == 2:
                f_back = self.entities.get_items_by_class(file_backdrop).first()

                f_back.show_generated_font(getuser(), self.board.story.undertale)
                f_back.show()
            #This event blows up the file information.
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
            #Cache our flowey_head, flowey_static, and player_character.
            f_head = self.entities.get_items_by_class(flowey_head).first()
            f_static = self.entities.get_items_by_class(flowey_static).first()
            p_char = self.entities.get_items_by_class(character).first()

            #This event moves Flowey and our character to their appropriate positions.
            if event_number == 0:
                f_head.hide()
                f_static.force_static(0)
                p_char.move_to_bottom = True
            #This event shows Flowey again and makes his head shake.
            elif event_number == 1:
                f_static.force_static(0)
                f_static.attempt = True
                f_head.shake = True
                f_head.show()
            #This event begins the first portion of the story.
            elif event_number == 2:
                SONGS.YOU_IDIOT.play()

                self.board.story.play(self.board.story.pre_fight_story_before_first_snicker)
                self.board.running = True
                self.board.pause_loop = False
            #Events 3-9 set Flowey's faces according to the text of the screen.
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
            #This event makes Flowey snicker and removes our shattered files.
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
            #Cache our Flowey head and Flowey static.
            f_head = self.entities.get_items_by_class(flowey_head).first()
            f_static = self.entities.get_items_by_class(flowey_static).first()

            #This event plays Flowey's creepy laugh.
            if event_number == 0:
                EFFECTS.FLOWEY_CREEPY_LAUGH_NORMAL.play()
            #This event makes flowey appear again.
            elif event_number == 1:
                f_head.animation.set_current(0)
                f_head.show()
                f_static.force_static(1)
                f_static.attempt = True
            #This event runs the second portion of the story.
            elif event_number == 2:
                self.board.story.play(self.board.story.pre_fight_story_before_second_snicker)
                self.board.running = True
                self.board.pause_loop = False
            #Events 3-12 and 14 display Flowey's expressions depending on the text on-screen.
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
            #This event let's Flowey's face have a special animation.
            elif event_number == 13:
                f_head.animation.set_current(9)
                f_head.animation.increment = 4
            elif event_number == 14:
                f_head.animation.set_current(19)
                f_head.animation.increment = 0
            #This event prepares Flowey to snicker again.
            elif event_number == 15:
                f_head.hide()
                f_head.flowey_snicker(True)
                f_static.force_static(1)
                f_static.attempt = False
            #This event plays Flowey laugh in a lower, creepier pitch.
            elif event_number == 16:
                EFFECTS.FLOWEY_CREEPY_LAUGH_SLOW.play()
            #This event shows Flowey again.
            elif event_number == 17:
                f_head.animation.set_current(0)
                f_head.show()
                f_static.force_static(1)
                f_static.attempt = True
            #This event plays the third part of the story.
            elif event_number == 18:
                self.board.story.play(self.board.story.pre_fight_story_before_walk)
                self.board.running = True
                self.board.pause_loop = False
        elif story_number == 3:
            #Cache our Flowey head, Flowey static, and player character.
            f_head = self.entities.get_items_by_class(flowey_head).first()
            f_static = self.entities.get_items_by_class(flowey_static).first()
            p_char = self.entities.get_items_by_class(character).first()

            #Events 0-6 and 9 change Flowey's expressions to the appropriate ones for the in-game text.
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
            #This event moves the player up a few pixels for defying Flowey.
            elif event_number == 7:
                p_char.move_up_slightly = True
            #This evemt plays the fourth portion of the story.
            elif event_number == 8:
                f_head.animation.set_current(23)
                self.board.story.play(self.board.story.pre_fight_story_before_fight)
                self.board.running = True
                self.board.pause_loop = False
            elif event_number == 9:
                f_head.animation.set_current(24)
            #This event stops the music.
            elif event_number == 10:
                f_head.animation.set_current(25)
                f_static.attempt = False
                SONGS.YOU_IDIOT.stop()
            #This event handles if the debugger skipped to the soul portion as well as prepares the human soul for battle.
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
                self.entities.add(soul(MY_SCREEN, skipped, self, p_char, self.keyboard, EFFECTS, SPRITESHEETS))
        elif story_number == 4:
            #This event removes our character and keeps the soul.
            if event_number == 0:
                self.entities.remove(self.entities.get_items_by_class(character).first())
            #This event prepares the other 6 souls Flowey has for battle.
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
            #This event plays a short sound effect to send the souls into battle.
            elif event_number == 2:
                EFFECTS.SOUL_SEND_TO_BATTLE.play()
            #This event removes the Flowey souls, displays the silhouette-d Flowey, and flashes the screen red.
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
            #This event stops the screen from flashing red.
            elif event_number == 4:
                self.stop_red = True
                self.begin_fight = False
            #This event shakes the screen and plays the Omega Laugh.
            elif event_number == 5:
                SONGS.FLOWEY_MEGA_LAUGH.play(loops = 0)

                MY_SCREEN.shake_screen_duration(3, 3, 385)
        elif story_number == 5:
            #This event makes the soul playable and begins the actual fight.
            if event_number == 0:
                SONGS.YOUR_BEST_NIGHTMARE_THEME1.play(loops = 0)

                self.flowey.entities.remove(self.flowey.entities.get_items_by_class(white_overlay).first())
                self.flowey.entities.remove(self.flowey.entities.get_items_by_class(flowey_face).first())

                self.flowey.entities.remove_range(self.flowey.entities.get_items_by_class(dark_piece))

                self.entities.get_items_by_class(soul).first().controls = True

#This classes sole purpose is the shake the in-game camera.
class my_screen:
    def __init__(self) -> None:
        #Initialize everything to 0 to prevent any offsets.
        self.x = 0.0
        self.y = 0.0
        self.shake_intensity = 0.0
        self.shake_recovery = 0
        self.duration = 0
        self.tick = 0

    #Shakes the screen at the intensity specified and recovers at the speed specified.
    def shake_screen(self, intensity: int, speed: int) -> None:
        #Set the x and y offsets to be random integers from the negative to positive intensity.
        self.x = float(random.randint(-intensity, intensity))
        self.y = float(random.randint(-intensity, intensity))
        #Stores the intensity and recovery for later.
        self.shake_intensity = float(intensity)
        self.shake_recovery = speed
        #Resets the tick.
        self.tick = 0

    #Shakes the screen not only at an intensity and recovery speed, but for a duration in ticks.
    def shake_screen_duration(self, intensity: int, speed: int, duration: int) -> None:
        self.shake_screen(intensity, speed)
        #The duration is divided by 3 as we only change the screen shake once every 3 ticks.
        self.duration = int(duration / 3)

    def update(self) -> None:
        #As long as the intensity is at least 1 (shows an actual effect on-screen since 1 would mean 1 pixel)...
        if self.shake_intensity >= 1.0:
            #And the tick is at least 2 (every 3 ticks)...
            if self.tick >= 2:
                #If there is a duration remaining...
                if self.duration > 0:
                    #Continue shaking the screen until the duration is down to 0.
                    self.shake_screen(self.shake_intensity, self.shake_recovery)
                    self.duration -= 1
                #Otherwise, reduce the intensity by the recovery.
                else:
                    self.shake_screen(int(self.shake_intensity / ((abs(self.shake_recovery) / 10) + 1)), self.shake_recovery)
            #Otherwise, increase the tick until it reaches at least 2.
            else:
                self.tick += 1
        #Otherwise, reset the shaking as there is no more noticable shakes.
        else:
            self.shake_intensity = 0
            self.x = 0
            self.y = 0
            self.tick = 0

#Initialize the game and run it.
game = window("Undertale: Omega Flowey")
game.run()

#Cumulative lines: 522 (__init__.py) + 185 (entity.py) + 1,059 (flowey.py) + 491 (fonts.py) + 44 (input.py) + 484 (player.py) + 147 (sound.py) + 461 (sprites.py) + 566 (story_board.py)
#Total lines: 3,959