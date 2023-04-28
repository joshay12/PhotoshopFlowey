from sprites import *
from entity import *
from math import sin, cos, radians

#This is the global speed of Flowey's stalks on the left and right of his head.
#It affects the entirety of Flowey, including if the other pieces of Flowey move around.
STALK_SPEED = 3
#This is used to change the size of the organs which are further back.
ORGAN_SIZE_OFFSET = 1.0

#This is quite a long and complicated class, so I'll try to help out with understanding as much as possible.
class flowey:
    def __init__(self, window, my_screen, sheets: predef_spritesheets, x: int, y: int) -> None:
        #We need to prepare everything in Flowey, including using the organ's size.
        global ORGAN_SIZE_OFFSET

        self.window = window
        self.my_screen = my_screen
        self.x = x
        self.y = y
        self.origin_x = x
        self.origin_y = y
        #We set the brightness to 0 so Flowey is dark immediately on loading.
        self.brightness = 0
        self.sheets = sheets
        #Flowey must not be rendered immediately.
        self.visible = False
        #Flowey must be off-screen to the top.
        self.move_to_0 = False
        #Flowey will be dark until this is True.
        self.reveal_flowey = False
        #The state of Flowey's massive laugh. 0 is no laugh has been done while higher numbers indicate a further state within the laugh.
        self.laugh = 0

        #Create a personal entity collection for Flowey.
        self.entities = entity_collection()

        #BEGIN CREATING THE AMALGAMATION OF FLOWEY.

        #This creates the stalks for Flowey.
        self.entities.add(stalks(self, 402, 150, False))
        self.entities.add(stalks(self, -52, 152, True))
        
        #These two for loops are to assist in creating the organs at specific places with the specific size offset.
        for i in range(3):
            self.entities.add(organ(self, 438 - i * 20, i * -30, False, i))

        ORGAN_SIZE_OFFSET = 1.0
        
        for i in range(3):
            self.entities.add(organ(self, -25 + i * 44, i * -30, True, i))

        #These 9 items help set up the big chunks and portions of Flowey's body.
        self.entities.add(hand(self, 470, 210, False))
        self.entities.add(hand(self, 0, 210, True))
        self.entities.add(vine_1(self, 400, 225, False))
        self.entities.add(vine_1(self, -55, 225, True))
        self.entities.add(vine_2(self, 400, 215, False))
        self.entities.add(vine_2(self, -55, 215, True))
        self.entities.add(vine_3(self, 400, 205, False))
        self.entities.add(vine_3(self, -55, 205, True))
        self.entities.add(television(self, 242, -30))

        #These 9 items help create a proper Flowey head.
        self.entities.add(head_top(self, 260, 120))
        self.entities.add(head_nostrils(self, 288, 110))
        self.entities.add(head_bottom(self, 290, 142))
        self.entities.add(head_lip(self, 275, 255, False))
        self.entities.add(head_lip(self, 345, 255, True))
        self.entities.add(head_teeth(self, 292, 250, False))
        self.entities.add(head_teeth(self, 329, 250, True))
        self.entities.add(head_dimple(self, 285, 119, False))
        self.entities.add(head_dimple(self, 340, 119, True))

        #These 10 items help create eyes, eye sockets, and pupils for Flowey.
        #Flowey has two eyes on the sides of his head and two eyes above his head next to the TV.
        self.entities.add(eye_socket(self, 230, 118, False))
        self.entities.add(eye_socket(self, 360, 122, True))
        self.entities.add(eye(self, 239, 135, False))
        self.entities.add(eye(self, 371, 135, True))
        self.entities.add(eye_pupil_small(self, 249, 177, False))
        self.entities.add(eye_pupil_small(self, 377, 177, True))
        self.entities.add(eye_top(self, 155, 120, False))
        self.entities.add(eye_top(self, 405, 120, True))
        self.entities.add(eye_pupil_large(self, 193, 136, False))
        self.entities.add(eye_pupil_large(self, 432, 136, True))

        #This creates the background to prevent the organs from peeking through the piping coming up next.
        self.entities.add(background(self, 150, 10))

        #THIS IS THE START OF FLOWEY'S PIPING ON THE SIDES OF HIS HEAD AND TV.
        #Each pipe resembles one of the souls Flowey has.

        #Bottom Right Pipes
        temp_x = 310
        temp_y = 220
        temp_dir = 35

        #For each of these loops, we turn the piping a certain direction and move the x and y in the direction it is facing to assist with placement rather than manual trial-and-error.
        for i in range(15):
            self.entities.add(piping(self, temp_x, temp_y, i, self.current_degree(360 - temp_dir), False))

            temp_x, temp_y, temp_dir = self.move_in_direction(temp_x, temp_y, 14, 14, temp_dir, 16)

        #Middle Right Pipes
        temp_x = 350
        temp_y = 85
        temp_dir = -20

        for i in range(5):
            self.entities.add(piping(self, temp_x, temp_y, i, self.current_degree(360 - temp_dir), False))

            temp_x, temp_y, temp_dir = self.move_in_direction(temp_x, temp_y, 14, 14, temp_dir, -8)

        for i in range(6):
            self.entities.add(piping(self, temp_x, temp_y, i + 6, self.current_degree(360 - temp_dir), False))

            temp_x, temp_y, temp_dir = self.move_in_direction(temp_x, temp_y, 14, 14, temp_dir, -24)

        for i in range(6):
            self.entities.add(piping(self, temp_x, temp_y, i + 11, self.current_degree(360 - temp_dir), False))

            temp_x, temp_y, temp_dir = self.move_in_direction(temp_x, temp_y, 14, 14, temp_dir, -8)

        #Top Right Pipes
        temp_x = 365
        temp_y = 70
        temp_dir = -35

        for i in range(11):
            self.entities.add(piping(self, temp_x, temp_y, i + 5, self.current_degree(360 - temp_dir), False))

            temp_x, temp_y, temp_dir = self.move_in_direction(temp_x, temp_y, 14, 14, temp_dir, 16)

        #Bottom Left Pipes
        temp_x = 240
        temp_y = 220
        temp_dir = -215

        for i in range(15):
            self.entities.add(piping(self, temp_x, temp_y, i, self.current_degree(360 - temp_dir), False))

            temp_x, temp_y, temp_dir = self.move_in_direction(temp_x, temp_y, 14, 14, temp_dir, -16)

        #Middle Left Pipes
        temp_x = 200
        temp_y = 85
        temp_dir = 200

        for i in range(5):
            self.entities.add(piping(self, temp_x, temp_y, i, self.current_degree(360 - temp_dir), False))

            temp_x, temp_y, temp_dir = self.move_in_direction(temp_x, temp_y, 14, 14, temp_dir, 8)

        for i in range(6):
            self.entities.add(piping(self, temp_x, temp_y, i + 6, self.current_degree(360 - temp_dir), False))

            temp_x, temp_y, temp_dir = self.move_in_direction(temp_x, temp_y, 14, 14, temp_dir, 24)

        for i in range(6):
            self.entities.add(piping(self, temp_x, temp_y, i + 11, self.current_degree(360 - temp_dir), False))

            temp_x, temp_y, temp_dir = self.move_in_direction(temp_x, temp_y, 14, 14, temp_dir, 8)

        #Top Left Pipes
        temp_x = 185
        temp_y = 70
        temp_dir = -145

        for i in range(11):
            self.entities.add(piping(self, temp_x, temp_y, i + 5, self.current_degree(360 - temp_dir), False))

            temp_x, temp_y, temp_dir = self.move_in_direction(temp_x, temp_y, 14, 14, temp_dir, -16)

        #THIS IS THE END OF FLOWEY'S PIPING AND AMALGAMATION CREATION.

        #A generic ticking variable for keeping track of time.
        self.tick = 0

        #Set the brightness within all the entities of flowey to the initial value (0 - Black).
        self.set_brightness_all()

    #Provide a degree too high or low and return a degree from 0-360 no matter what.
    def current_degree(self, degree: int) -> int:
        #Until the degree is 360 or lower, lower the degree.
        while degree > 360:
            degree -= 360

        #Until the degree is 0 or higher, raise the degree.
        while degree < 0:
            degree += 360

        #Return the new 0-360 degree.
        return degree

    #Move an entity within a certain direction. This function is made specifically for Flowey's piping.
    def move_in_direction(self, old_x: int, old_y: int, speed_x: int, speed_y: int, degrees: int, degree_increment: int):
        #We alter the x and y values by a formula to determine how to move the entity in the direction it is facing.
        new_x = old_x + int(speed_x * cos(radians(degrees)))
        new_y = old_y + int(speed_y * sin(radians(degrees)))

        #Return the newly made x and y as well as alter the degrees by the degree_increment provided.
        return new_x, new_y, (degrees - degree_increment)

    #Set the brightness of all entities within Flowey to the brightness provided.
    def set_brightness_all(self) -> None:
        for entity in self.entities.entities:
            entity.set_brightness(self.brightness)

    #Readjust the sizes of all entities within Flowey to their default size.
    def readjust_sizes(self) -> None:
        for entity in self.entities.entities:
            entity.readjust_size()

    def update(self) -> None:
        #Connect our stalks to change them.
        global STALK_SPEED

        #Update all Flowey's entities.
        for entity in self.entities.entities:
            entity.update()

        #Increase the tick.
        self.tick += 1

        #If we need to move Flowey to the (0, 0) location and he isn't already there...
        if self.move_to_0 and self.origin_y < 0:
            #Increase Flowey's y-coordinate.
            self.origin_y += 0.6

            #If Flowey is beyong the (0, 0) location...
            if self.origin_y > 0:
                #Stop Flowey from moving and set the location to (0, 0).
                self.origin_y = 0
                self.move_to_0 = False

        #After 960 ticks (the amount of time the intro song approximately takes), as long as we aren't revealing Flowey...
        if self.tick == 960 and self.origin_y == 0 and not self.reveal_flowey:
            #Add the white overlay to Flowey's TV.
            self.entities.add(white_overlay(self.entities.get_items_by_class(television).first(), self.sheets))
        #Otherwise, if we are revealing Flowey and his brightness is not fully there yet...
        elif self.reveal_flowey and self.brightness < 255 and self.laugh == 0:
            #Slow down the stalks and force the Flowey movement to stop.
            STALK_SPEED = 1

            #Increase the brightness quickly to hopefully avoid see graphical issues with the brightness.
            #Brightness was a pain to implement to be honest. Glad I partially got it to work.
            self.brightness += 20

            #If we are above the maximum brightness...
            if self.brightness > 255:
                #Continue to laugh and set the brightness to the maximum.
                self.brightness = 255
                self.laugh = 1
                self.tick = 0

            #Reset the brightness of all entities to the new brightness.
            self.set_brightness_all()
        #Otherwise, if Flowey is laughing...
        elif self.laugh == 1 and self.tick == 60:
            #Prepare in the window.
            self.laugh = 2
            self.window.run_event(4, 5)
        #Otherwise, if Flowey is done laughing...
        elif self.laugh == 2 and self.tick == 450:
            #Continue to wait for the pause after laughing to end.
            self.laugh = 3
        #Finally, if the laughing is fully complete, start the fight.
        elif self.laugh == 3 and self.tick == 510:
            self.window.run_event(5, 0)
            STALK_SPEED = 3

        #Set Flowey's x and y position to the origin, but let it be affected by the screen shaking.
        self.x = self.origin_x + self.my_screen.x
        self.y = self.origin_y + self.my_screen.y

    #Render all the entities within Flowey if Flowey is visible.
    def render(self, screen: Surface) -> None:
        if not self.visible:
            return

        for entity in self.entities.entities:
            entity.render(screen)

#This is the overlay on the TV when Flowey is first introduced.
#It allows Flowey's creepy face to appear and laugh at you.
class white_overlay(entity):
    def __init__(self, tv: 'television', spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.TV_OVERLAY_ANIMATION, 0, 0, False, False)

        #We set up the white overlay to be based on the TV provided.
        self.tv = tv

        self.x = self.tv.x + 17
        self.y = self.tv.y + self.tv.height / 2 - self.height / 3 + 3
        #The overlay is not shown at first.
        self.opacity = 0
        self.tick = 0
        #The overlay is on top of everything.
        self.layer = 3000

        #Change the opacity of the overlay.
        self.get_sprite().change_opacity(self.opacity)
        #Add Flowey's face to the overlay.
        self.face = flowey_face(self, spritesheets)
        self.tv.owner.entities.add(self.face)

    #This is to satisfy the flowey class because if an entity does not have a "set_brightness" it will crash the program.
    def set_brightness(self, _: int):
        pass

    def update(self) -> None:
        #If Flowey is moving slow, specifically set the position based off the TV's.
        if STALK_SPEED < 3:
            self.x = self.tv.x + 17
            self.y = self.tv.y + self.tv.height / 2 - self.height / 3 + 3

        #Change the opacity of the sprite.
        self.get_sprite().change_opacity(self.opacity)

        #Increase the sprite's visibility.
        self.opacity += 4

        #If the opacity is greater than the maximum, set it to the maximum.
        if self.opacity > 255:
            self.opacity = 255

    def render(self, screen: Surface) -> None:
        if not self.visible:
            return

        screen.blit(self.get_sprite().image, self.get_data())

#THis is Flowey's face which goes on top of the white overlay in the TV.
#It laughs at you.
class flowey_face(entity):
    def __init__(self, overlay: 'white_overlay', spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.TV_FACE_ANIMATION, 0, 0, True, False)

        #Everything within this sprite is based off the overlay.
        self.overlay = overlay

        self.x = self.overlay.x + self.overlay.width / 2 - self.width / 2
        self.y = self.overlay.y + self.overlay.height / 2 - 32
        self.y_offset = 0
        self.opacity = self.overlay.opacity
        self.tick = 0
        #Have it be in front of the overlay.
        self.layer = self.overlay.layer + 1
        self.full_smile = False

        #Change the face's opacity.
        self.get_sprite().change_opacity(self.opacity)

    #This is the same case as the white overlay. This is here to appease the flowey class.
    def set_brightness(self, _: int):
        pass

    def update(self) -> None:
        #Get the previous animation frame's height.
        c_height = self.get_sprite().get_height()

        #Update the animation.
        self.animation.update()

        #Get the current animation frame's height.
        n_height = self.get_sprite().get_height()

        #Alter the y offset to the height different, or if Flowey is laughing, then never change the y_offset.
        self.y_offset -= int((n_height - c_height) / 2) if self.animation.index < 11 else 0

        #Set all other elements of the face to the white overlay's.
        self.opacity = self.overlay.opacity
        self.x = self.overlay.x + self.overlay.width / 2 - self.width / 2
        self.y = self.overlay.y + self.overlay.height / 2 - 32 - self.y_offset
        self.get_sprite().change_opacity(self.opacity)

        #If we aren't laughing yet...
        if self.overlay.tv.owner.laugh < 2:
            #If the opacity has reached the maximum...
            if self.opacity >= 255:
                #If the animation is just a smile...
                if self.animation.index < 6:
                    #Start incrementing the animation automatically.
                    self.animation.increment = 5
                #Once the animation has shown a smile...
                elif self.animation.index == 6 and self.tick < 60:
                    #Stop the animation and wait for 1 second (60 ticks).
                    self.animation.increment = 0
                    self.tick += 1
                #Once 60 seconds pass...
                elif self.animation.index == 6:
                    #Reveal the true eyes of the smile by increasing the animation.
                    self.animation.next()
                    self.animation.increment = 5
                    self.tick = 0
                #Once the animation has shown a full smile...
                elif self.animation.index == 10 and self.tick < 60:
                    #Stop the animation and wait for 1 second (60 ticks).
                    self.animation.increment = 0
                    self.tick += 1
                #Once 60 seconds pass...
                elif self.animation.index == 10 and self.tick == 60:
                    #Remove the darkness from Flowey and show the full body.
                    self.overlay.tv.owner.reveal_flowey = True
                    #Run this event in the window.
                    self.overlay.tv.owner.window.run_event(4, 4)
                    self.tick += 1
        #Otherwise, if Flowey is laughing...
        elif self.overlay.tv.owner.laugh == 2:
            #Set the y_offset manually and increase the animation for laughing.
            self.y_offset = -22
            self.animation.increment = 4

            #If the animation is beyond the laughing, bright it back to the laughing beginning.
            if self.animation.index > 13:
                self.animation.set_current(11)
        #Otherwise, if the laughing is done...
        else:
            #Just allow Flowey to smile.
            self.y_offset = -14
            self.animation.increment = 0
            self.animation.set_current(14)

    def render(self, screen: Surface) -> None:
        if not self.visible:
            return

        screen.blit(self.get_sprite().image, self.get_data())

#This class was made to help make Flowey an easier setup. This handles a lot of functions that would've made this file much larger.
class flowey_piece(entity):
    def __init__(self, owner: flowey, left_animation: animation, right_animation: animation, x: int, y: int, flip: bool = False, layer: int = 0, force_center: bool = False, one_sided: bool = False, force_copy: bool = True, create_dark_piece_automatically: bool = True) -> None:
        super().__init__(left_animation if one_sided else (left_animation if not flip else right_animation), x + owner.x, y + owner.y, force_center = force_center, force_copy = force_copy)

        #Let the owner be able to move all x and y positions of the sprites.
        self.owner = owner
        #Determins how far in front or behind to make the entity for rendering.
        self.layer = layer
        self.tick = 0
        #This is stored to prevent issues when using sin and cos.
        self.origin_x = x
        self.origin_y = y
        self.origin_direction = self.direction
        self.origin_image_direction = self.image_direction
        self.brightness = 255
        self.darkness = None

        #Brightness is an illusion with a dark version over-top the flowey_piece and it changing its opacity.
        if create_dark_piece_automatically:
            self.create_dark_piece(force_center)

    #Once we create the dark piece, we add it to the Flowey entity collection.
    def create_dark_piece(self, force_center: bool, resize: float = 1.0) -> None:
        self.darkness = dark_piece(self, self.animation, force_center, resize)
        self.owner.entities.add(self.darkness)

    #Set the brightness according to the dark piece made.
    def set_brightness(self, brightness: int) -> None:
        self.brightness = brightness

    #Readjust the size of the entity to its default.
    def readjust_size(self) -> None:
        self.animation.resize_images(1.0)

    def render(self, screen: Surface) -> None:
        if not self.visible:
            return

        screen.blit(self.get_sprite().image, self.get_data())

#This dark piece assists in the illusion of brightness at the cost of memory (RAM) and halves the FPS.
#These are immediately deleted once they fade away to preserve resources.
class dark_piece(flowey_piece):
    def __init__(self, owner: flowey_piece, animation: animation, force_center: bool = False, resize: float = 1.0) -> None:
        super().__init__(owner, animation, animation, owner.x, owner.y, False, 0, force_center, False, True, False)

        #If the resize is not 1, then resize the animation.
        if resize != 1.0:
            self.animation.resize_images_set_defaults(resize)
           
        self.owner = owner
        #Turn the animation into a silhouette.
        self.animation.make_silhouette()
        #Set the brightness to the owner's (flowey_piece).
        self.brightness = self.owner.brightness
        self.visible = True
        #Put the darkness in front of all things besides the white overlay.
        self.layer = self.owner.layer + 1000

    def update(self) -> None:
        self.brightness = self.owner.brightness

        self.x = self.owner.x
        self.y = self.owner.y
        #Change the opacity based on the current brightness.
        self.animation.change_opacity_all(255 - self.brightness)
        self.animation.set_current(self.owner.animation.index)

    def render(self, screen: Surface) -> None:
        if not self.visible:
            return

        screen.blit(self.get_sprite().image, self.get_data())

#There is a backdrop for Flowey. This is behind Flowey's piping, head, and TV to prevent the stalks and organs from peeking through
class background(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int) -> None:
        super().__init__(owner, owner.sheets.BACKGROUND_ANIMATION, None, x, y, False, 100, False, True, False)

        self.extender = extender(self)
        self.owner.entities.add(self.extender)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.2

        #Handles the movement of the background to be natural.
        bobbing_y = sin(self.tick / 2) * 4

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y + bobbing_y

        if self.darkness != None:
            self.darkness.update()

#In Flowey's jaws, there is an extender to assist in hiding from the flashing red background. This is the sole purpose for this class.
class extender(flowey_piece):
    def __init__(self, owner: background) -> None:
        super().__init__(owner, owner.owner.sheets.EXTENDER_ANIMATION, None, 0, 0, False, 249, False, False, True, False)

        #This is set to be just below the background of Flowey.
        self.owner = owner
        self.x = self.owner.origin_x + self.owner.owner.x + self.owner.width / 2 - self.width / 2 - 2
        self.y = self.owner.origin_y + self.owner.owner.y + self.owner.height - self.height / 2 - 24

    def update(self) -> None:
        self.x = self.owner.origin_x + self.owner.owner.x + self.owner.width / 2 - self.width / 2 - 2
        self.y = self.owner.origin_y + self.owner.owner.y + self.owner.height - self.height / 2 - 24

#These are the green stalks with thorns on them on the left and right side of Flowey.
class stalks(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool = False) -> None:
        super().__init__(owner, owner.sheets.STALKS_ANIMATION_LEFT, owner.sheets.STALKS_ANIMATION_RIGHT, x, y, flip, 7)

    def update(self) -> None:
        self.tick += 1

        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y

        #Update the animation 30 times per second.
        if self.tick % 2 == 0:
            self.animation.update()
            self.animation.amount_to_skip = STALK_SPEED

        if self.darkness != None:
            self.darkness.update()

#There are 6 organs for Flowey. They are the objects in the top-left and top-right corners which look like pipes.
class organ(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool, layer_offset: int) -> None:
        super().__init__(owner, owner.sheets.ORGANS_ANIMATION_LEFT, owner.sheets.ORGANS_ANIMATION_RIGHT, x, y, flip, 6 - layer_offset, create_dark_piece_automatically = False)

        global ORGAN_SIZE_OFFSET

        #Do not re-size the organs if it is the original.
        if ORGAN_SIZE_OFFSET < 1.0:
            self.animation = self.animation.resize_images_set_defaults(ORGAN_SIZE_OFFSET)

        self.create_dark_piece(False)

        #Lessen the organ size by 10% next iteration.
        ORGAN_SIZE_OFFSET -= 0.1

        if ORGAN_SIZE_OFFSET > 0.69 and ORGAN_SIZE_OFFSET < 0.71 and flip:
            self.x += 16
            self.origin_x += 16

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.04
        else:
            self.tick = 0

        #Handles the movement of the organs to be natural.
        inverse_tick = self.tick if self.origin_x > 200 else -self.tick
        bobbing_x = sin(inverse_tick) * (self.animation.current.get_width() / 100)
        bobbing_y = sin(self.tick) * (self.animation.current.get_height() / 75)

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y

        if self.brightness >= 255:
            self.get_sprite().resize_image_set(1 + (sin(self.tick) * 1.5 / 100.0))
        else:
            self.get_sprite().resize_image_set(1.0)

        if self.darkness != None:
            self.darkness.update()

#There are 2 hands for Flowey. They are the objects in the bottom-left and bottom-right corners which look like hands (... obviously).
class hand(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.HANDS_ANIMATION_LEFT, owner.sheets.HANDS_ANIMATION_RIGHT, x, y, flip, 0)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.16
        else:
            self.tick = 0

        #Handles the movement of the hands to be natural.
        inverse_tick = self.tick if self.origin_x > 200 else -self.tick
        bobbing_x = sin(inverse_tick) * 5
        bobbing_y = cos(self.tick) * 5

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y

        if self.brightness >= 255:
            self.get_sprite().resize_image_set(1 + (sin(self.tick / 2) * 1.8 / 100.0))
        else:
            self.get_sprite().resize_image_set(1.0)

        if self.darkness != None:
            self.darkness.update()

#There are 6 vines for Flowey. They are the objects in between the stalks and the hands. They are difficult to notice unless you pay extra attention to them.
#This is the first iteration of the vines.
class vine_1(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.VINES_1_ANIMATION_LEFT, owner.sheets.VINES_1_ANIMATION_RIGHT, x, y, flip, 3)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.06
        else:
            self.tick = 0

        #Handles the movement of the vines to be natural.
        inverse_tick = self.tick if self.origin_x > 200 else -self.tick
        bobbing_x = sin(inverse_tick) * 4
        bobbing_y = cos(self.tick * 1.8) * 4

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        
        if self.brightness >= 255:
            self.get_sprite().resize_image_set(1 + (sin(-self.tick) / 100.0))
        else:
            self.get_sprite().resize_image_set(1.0)

        if self.darkness != None:
            self.darkness.update()

#This is the second iteration of the vines.
class vine_2(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.VINES_2_ANIMATION_LEFT, owner.sheets.VINES_2_ANIMATION_RIGHT, x, y, flip, 2)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.06
        else:
            self.tick = 0

        #Handles the movement of the vines to be natural.
        inverse_tick = self.tick if self.origin_x > 200 else -self.tick
        bobbing_x = sin(inverse_tick)
        bobbing_y = cos(self.tick) * 4

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        
        if self.brightness >= 255:
            self.get_sprite().resize_image_set(1 + (sin(-self.tick) / 100.0))
        else:
            self.get_sprite().resize_image_set(1.0)

        if self.darkness != None:
            self.darkness.update()

#This is the third and final iteration of the vines.
class vine_3(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.VINES_3_ANIMATION_LEFT, owner.sheets.VINES_3_ANIMATION_RIGHT, x, y, flip, 1)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.06
        else:
            self.tick = 0

        #Handles the movement of the vines to be natural.
        inverse_tick = self.tick if self.origin_x > 200 else -self.tick
        bobbing_x = sin(inverse_tick / 1.8)
        bobbing_y = cos(self.tick / 1.8) * 4

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        
        if self.brightness >= 255:
            self.get_sprite().resize_image_set(1 + (sin(self.tick / 1.8) * -1 / 100.0))
        else:
            self.get_sprite().resize_image_set(1.0)

        if self.darkness != None:
            self.darkness.update()

#This is the TV atop Flowey's head.
class television(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int) -> None:
        super().__init__(owner, owner.sheets.TV_ANIMATION, owner.sheets.TV_ANIMATION, x, y, False, 500)

        self.animation.set_current(1)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.16
        else:
            self.tick = 0

        #Handles the movement of the TV to be natural.
        bobbing_y = sin(self.tick) * 2

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y + bobbing_y

        if self.darkness != None:
            self.darkness.update()

#This is the top of the head just below the TV.
class head_top(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int) -> None:
        super().__init__(owner, owner.sheets.HEAD_ANIMATION, owner.sheets.HEAD_ANIMATION, x, y, False, 251)

        self.animation.set_current(0)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks from normal.
        self.tick += 0.3 if STALK_SPEED > 1 else 0.08

        #Handles the movement of the TV to be natural.
        bobbing_y = sin(self.tick) * 4

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y + bobbing_y

        if self.darkness != None:
            self.darkness.update()

#These are the nostrils inside of the top head.
class head_nostrils(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int) -> None:
        super().__init__(owner, owner.sheets.HEAD_ANIMATION, owner.sheets.HEAD_ANIMATION, x, y, False, 252, False, True, True, False)

        self.animation.sprites[8].resize_image_set_default(1.1)
        self.animation.sprites[9].resize_image_set_default(1.1)
        self.animation.set_current(8)
        self.nostril_tick = 0.0

        self.create_dark_piece(False)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing and nostril ticks from normal.
        if STALK_SPEED > 1:
            self.nostril_tick += 1.0
            self.tick += 0.24
        else:
            self.nostril_tick += 0.25
            self.tick += 0.08

        #Flare the nostrils either 3 times per second or almost 1 time per second.
        if self.nostril_tick % 20 == 0:
            self.animation.set_current(9 if self.animation.index == 8 else 8)

        #Handles the movement of the TV to be natural.
        bobbing_y = sin(self.tick) * 6

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y + bobbing_y

        if self.darkness != None:
            self.darkness.update()

#This is the bottom of the head, right in between the lips.
class head_bottom(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int) -> None:
        super().__init__(owner, owner.sheets.HEAD_ANIMATION, owner.sheets.HEAD_ANIMATION, x, y, False, 250, False, True, True, False)

        self.animation.sprites[3].resize_image_set_default(1.3)
        self.animation.set_current(3)

        self.create_dark_piece(False)

    def update(self) -> None:
        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y

        if self.darkness != None:
            self.darkness.update()

#These are the lips just below the head.
class head_lip(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.HEAD_ANIMATION, owner.sheets.HEAD_ANIMATION, x, y, flip, 253, False, True)

        self.animation.set_current(4 if not flip else 5)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.16
        else:
            self.tick = 0

        #Handles the movement of the vines to be natural.
        inverse_tick = self.tick if self.origin_x > 300 else -self.tick
        bobbing_x = sin(inverse_tick * 2) * 4
        bobbing_y = sin(self.tick * 0.75) * 5

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        
        if self.brightness >= 255:
            self.get_sprite().resize_image_set(1 + (sin(self.tick * 0.75) * 4 / 100.0))
        else:
            self.get_sprite().resize_image_set(1.0)

        if self.darkness != None:
            self.darkness.update()

#These are the teeth attached to the lips.
class head_teeth(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.HEAD_ANIMATION, owner.sheets.HEAD_ANIMATION, x, y, flip, 254, False, True)

        self.animation.set_current(6 if not flip else 7)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.16
        else:
            self.tick = 0

        #Handles the movement of the vines to be natural.
        inverse_tick = self.tick if self.origin_x > 300 else -self.tick
        bobbing_x = sin(inverse_tick * 2) * 4
        bobbing_y = sin(self.tick * 0.75) * 5

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        
        if self.brightness >= 255:
            self.get_sprite().resize_image_set(1 + (sin(self.tick * 0.75) * 4 / 100.0))
        else:
            self.get_sprite().resize_image_set(1.0)

        if self.darkness != None:
            self.darkness.update()

#These are the dimples which go above the lips/teeth.
class head_dimple(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.HEAD_ANIMATION, owner.sheets.HEAD_ANIMATION, x, y, flip, 255, False, True, True, False)

        self.animation.sprites[1].resize_image_set_default(1.15)
        self.animation.sprites[2].resize_image_set_default(1.15)
        self.animation.set_current(1 if not flip else 2)

        self.create_dark_piece(False)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.16
        else:
            self.tick = 0

        #Handles the movement of the vines to be natural.
        inverse_tick = self.tick if self.origin_x > 300 else -self.tick
        bobbing_x = sin(inverse_tick * 2) * 4
        bobbing_y = sin(self.tick * 0.5)

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        
        if self.brightness >= 255:
            self.get_sprite().resize_image_set(1 + (sin(self.tick * 0.5) * 2 / 100.0))
        else:
            self.get_sprite().resize_image_set(1.0)

        if self.darkness != None:
            self.darkness.update()

#These are the eye-sockets which go to the outer rim of the lips.
class eye_socket(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.EYE_SOCKET_ANIMATION_LEFT, owner.sheets.EYE_SOCKET_ANIMATION_RIGHT, x, y, flip, 256, create_dark_piece_automatically = False)

        self.get_sprite().resize_image_set_default(0.8)

        self.create_dark_piece(False)

    def update(self) -> None:
        self.animation.update()
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.24
        else:
            self.tick = 0

        #Handles the movement of the vines to be natural.
        bobbing_y = sin(self.tick) * 2

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y + bobbing_y

        if self.darkness != None:
            self.darkness.update()

#These are the eyes which go in the eye sockets.
class eye(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.EYE_ANIMATION_LEFT, owner.sheets.EYE_ANIMATION_RIGHT, x, y, flip, 257, create_dark_piece_automatically = False)

        self.get_sprite().resize_image_set_default(0.75)

        self.create_dark_piece(False)

    def update(self) -> None:
        self.animation.update()
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.2
        else:
            self.tick = 0

        #Handles the movement of the vines to be natural.
        bobbing_y = sin(self.tick) * 1.5

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y + bobbing_y

        if self.darkness != None:
            self.darkness.update()

#These are the pupils which go in the side eyes.
class eye_pupil_small(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.PUPIL_ANIMATION, owner.sheets.PUPIL_ANIMATION, x, y, flip, 258, True, True, True, False)

        self.get_sprite().resize_image_set_default(0.5)

        self.create_dark_piece(True)

    def update(self) -> None:
        self.animation.update()
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.2
        else:
            self.tick = 0

        #Handles the movement of the vines to be natural.
        bobbing_y = sin(self.tick) * 1.6

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y + bobbing_y
        
        if self.brightness >= 255:
            self.get_sprite().resize_image_set(1 + (sin(self.tick * 1.15) * 15 / 100.0))
        else:
            self.get_sprite().resize_image_set(1.0)

        if self.darkness != None:
            self.darkness.update()

#These are the eyes which go to the left and right of the TV above the head.
class eye_top(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.EYE_TOP_ANIMATION_LEFT, owner.sheets.EYE_TOP_ANIMATION_RIGHT, x, y, flip, 259)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.2
        else:
            self.tick = 0

        #Handles the movement of the vines to be natural.
        inverse_tick = -self.tick if self.origin_x > 300 else self.tick
        bobbing_x = sin(inverse_tick) * 3
        bobbing_y = cos(self.tick) * 3

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y

        if self.darkness != None:
            self.darkness.update()

#These are the pupils which go in the top eyes.
class eye_pupil_large(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.PUPIL_ANIMATION, owner.sheets.PUPIL_ANIMATION, x, y, flip, 260, True, True)

    def update(self) -> None:
        self.animation.update()
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.2
        else:
            self.tick = 0

        #Handles the movement of the vines to be natural.
        inverse_tick = -self.tick if self.origin_x > 300 else self.tick
        bobbing_x = sin(inverse_tick) * 5.5
        bobbing_y = cos(self.tick) * 3

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        
        if self.brightness >= 255:
            self.get_sprite().resize_image_set(1 + (sin(self.tick * 1.25) * 20 / 100.0))
        else:
            self.get_sprite().resize_image_set(1.0)

        if self.darkness != None:
            self.darkness.update()

#These are the six circles of piping coming out of Flowey's face and TV.
class piping(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, index: int, direction: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.PIPE_ANIMATION, None, x, y, flip, 249 - index, True, True, True, False)

        self.animation.set_current(int(direction / 2))
        self.animation = animation([self.get_sprite()], 0)

        self.create_dark_piece(True, 0.5)

        self.my_delay = index * 4
        self.pause = 40
        self.delay_tick = 0
        self.grow = False
        self.grow_tick = self.pause - 1
        self.size = 0.5
        self.size_velocity = 0.0

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.2
        else:
            self.tick = 0

        if self.delay_tick < self.my_delay:
            self.delay_tick += 1
        elif not self.grow:
            self.grow_tick += 1
            
            if self.grow_tick % self.pause == 0:
                self.grow = True
                self.size_velocity = 0.008
        elif self.grow:
            self.size += self.size_velocity
            self.size_velocity -= 0.0004
            
            if self.size < 0.5:
                self.size = 0.5
                self.size_velocity = 0
                self.grow = False

            if self.brightness >= 255:
                self.get_sprite().resize_image_set(self.size)
            else:
                self.get_sprite().resize_image_set(0.5)

        #Handles the movement of the vines to be natural.
        bobbing_y = sin(self.tick / 2) * 4

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y + bobbing_y

        if self.darkness != None:
            self.darkness.update()