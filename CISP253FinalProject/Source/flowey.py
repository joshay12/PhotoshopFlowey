from pickle import FALSE
from sprites import *
from entity import *
from math import sin, cos, radians

STALK_SPEED = 3
ORGAN_SIZE_OFFSET = 1.0

class flowey:
    def __init__(self, sheets: predef_spritesheets, x: int, y: int) -> None:
        global ORGAN_SIZE_OFFSET

        self.x = x;
        self.y = y;
        self.brightness = 0.0
        self.sheets = sheets

        self.entities = entity_collection()

        self.entities.add(stalks(self, 402, 150, False))
        self.entities.add(stalks(self, -52, 152, True))
        
        for i in range(3):
            self.entities.add(organ(self, 438 - i * 20, i * -30, False, i))

        ORGAN_SIZE_OFFSET = 1.0
        
        for i in range(3):
            self.entities.add(organ(self, -25 + i * 44, i * -30, True, i))

        self.entities.add(hand(self, 470, 210, False))
        self.entities.add(hand(self, 0, 210, True))
        self.entities.add(vine_1(self, 400, 225, False))
        self.entities.add(vine_1(self, -55, 225, True))
        self.entities.add(vine_2(self, 400, 215, False))
        self.entities.add(vine_2(self, -55, 215, True))
        self.entities.add(vine_3(self, 400, 205, False))
        self.entities.add(vine_3(self, -55, 205, True))
        self.entities.add(television(self, 242, -30))

        self.entities.add(head_top(self, 260, 120))
        self.entities.add(head_nostrils(self, 288, 110))
        self.entities.add(head_bottom(self, 290, 142))
        self.entities.add(head_lip(self, 275, 255, False))
        self.entities.add(head_lip(self, 345, 255, True))
        self.entities.add(head_teeth(self, 292, 250, False))
        self.entities.add(head_teeth(self, 329, 250, True))
        self.entities.add(head_dimple(self, 285, 119, False))
        self.entities.add(head_dimple(self, 340, 119, True))

        self.entities.add(eye_socket(self, 230, 118, False))
        self.entities.add(eye_socket(self, 360, 122, True))
        self.entities.add(eye(self, 239, 135, False))
        self.entities.add(eye(self, 371, 135, True))
        self.entities.add(eye_pupil(self, 248, 177, False))
        self.entities.add(eye_pupil(self, 381, 181, True))

        #Bottom Right Pipes
        temp_x = 310
        temp_y = 220
        temp_dir = 35

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

        self.tick = 0

        #self.set_brightness_all()

    def current_degree(self, degree: int) -> int:
        while degree > 360:
            degree -= 360

        while degree < 0:
            degree += 360

        return degree

    def move_in_direction(self, old_x: int, old_y: int, speed_x: int, speed_y: int, degrees: int, degree_increment: int):
        new_x = old_x + int(speed_x * cos(radians(degrees)))
        new_y = old_y + int(speed_y * sin(radians(degrees)))

        return new_x, new_y, (degrees - degree_increment)

    def set_brightness_all(self) -> None:
        for entity in self.entities.entities:
            entity.set_brightness(self.brightness)

    def readjust_sizes(self) -> None:
        for entity in self.entities.entities:
            entity.readjust_size()

    def update(self) -> None:
        for entity in self.entities.entities:
            entity.update()

        #self.tick += 1
        #
        #if self.tick == 5:
        #    self.fully_bright = False
        #    #self.set_brightness_all()
        #elif self.tick > 120 and self.tick % 2 == 0 and self.brightness < 1.0:
        #    self.brightness += 0.1
        #    self.set_brightness_all()
        #elif self.tick > 120 and self.tick % 2 == 0 and not self.fully_bright:
        #    self.brightness = 1.0
        #    self.set_brightness_all()
        #    self.readjust_sizes()
        #    self.fully_bright = True

    def render(self, screen: Surface) -> None:
        for entity in self.entities.entities:
            entity.render(screen)

class flowey_piece(entity):
    def __init__(self, owner: flowey, left_animation: animation, right_animation: animation, x: int, y: int, flip: bool = False, layer: int = 0, force_center: bool = False) -> None:
        super().__init__(left_animation if not flip else right_animation, x + owner.x, y + owner.y, force_center = force_center)

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

    def set_brightness(self, brightness: float) -> None:
        for item in self.animation.sprites:
            item.set_brightness(brightness)

    def readjust_size(self) -> None:
        self.animation.resize_images(1.0)

    def render(self, screen: Surface) -> None:        
        screen.blit(self.get_sprite().image, self.get_data())

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

#There are 6 organs for Flowey. They are the objects in the top-left and top-right corners which look like pipes.
class organ(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool, layer_offset: int) -> None:
        super().__init__(owner, owner.sheets.ORGANS_ANIMATION_LEFT, owner.sheets.ORGANS_ANIMATION_RIGHT, x, y, flip, 6 - layer_offset)

        global ORGAN_SIZE_OFFSET

        #Do not re-size the organs if it is the original.
        if ORGAN_SIZE_OFFSET < 1.0:
            self.animation = self.animation.resize_images(ORGAN_SIZE_OFFSET)

        #Lessen the organ size by 10% next iteration.
        ORGAN_SIZE_OFFSET -= 0.1

        if ORGAN_SIZE_OFFSET > 0.69 and ORGAN_SIZE_OFFSET < 0.71 and flip:
            self.x += 16
            self.origin_x += 16

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.04

        #Handles the movement of the organs to be natural.
        inverse_tick = self.tick if self.origin_x > 200 else -self.tick
        bobbing_x = sin(inverse_tick) * (self.animation.current.get_width() / 100)
        bobbing_y = sin(self.tick) * (self.animation.current.get_height() / 75)

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        self.get_sprite().resize_image_set(1 + (sin(self.tick) * 1.5 / 100.0))

#There are 2 hands for Flowey. They are the objects in the bottom-left and bottom-right corners which look like hands (... obviously).
class hand(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.HANDS_ANIMATION_LEFT, owner.sheets.HANDS_ANIMATION_RIGHT, x, y, flip, 0)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.16

        #Handles the movement of the hands to be natural.
        inverse_tick = self.tick if self.origin_x > 200 else -self.tick
        bobbing_x = sin(inverse_tick) * 5
        bobbing_y = cos(self.tick) * 5

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        self.get_sprite().resize_image_set(1 + (sin(self.tick / 2) * 1.8 / 100.0))

#There are 6 vines for Flowey. They are the objects in between the stalks and the hands. They are difficult to notice unless you pay extra attention to them.
#This is the first iteration of the vines.
class vine_1(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.VINES_1_ANIMATION_LEFT, owner.sheets.VINES_1_ANIMATION_RIGHT, x, y, flip, 3)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.06

        #Handles the movement of the vines to be natural.
        inverse_tick = self.tick if self.origin_x > 200 else -self.tick
        bobbing_x = sin(inverse_tick) * 4
        bobbing_y = cos(self.tick * 1.8) * 4

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        self.get_sprite().resize_image_set(1 + (sin(-self.tick) / 100.0))

#This is the second iteration of the vines.
class vine_2(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.VINES_2_ANIMATION_LEFT, owner.sheets.VINES_2_ANIMATION_RIGHT, x, y, flip, 2)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.06

        #Handles the movement of the vines to be natural.
        inverse_tick = self.tick if self.origin_x > 200 else -self.tick
        bobbing_x = sin(inverse_tick)
        bobbing_y = cos(self.tick) * 4

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        self.get_sprite().resize_image_set(1 + (sin(-self.tick) / 100.0))

#This is the third and final iteration of the vines.
class vine_3(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.VINES_3_ANIMATION_LEFT, owner.sheets.VINES_3_ANIMATION_RIGHT, x, y, flip, 1)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.06

        #Handles the movement of the vines to be natural.
        inverse_tick = self.tick if self.origin_x > 200 else -self.tick
        bobbing_x = sin(inverse_tick / 1.8)
        bobbing_y = cos(self.tick / 1.8) * 4

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        self.get_sprite().resize_image_set(1 + (sin(self.tick / 1.8) * -1 / 100.0))

#This is the TV atop Flowey's head.
class television(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int) -> None:
        super().__init__(owner, owner.sheets.TV_ANIMATION, owner.sheets.TV_ANIMATION, x, y, False, 500)

        self.animation.set_current(1)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.16

        #Handles the movement of the TV to be natural.
        bobbing_y = sin(self.tick) * 2

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y + bobbing_y

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

#These are the nostrils inside of the top head.
class head_nostrils(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int) -> None:
        super().__init__(owner, owner.sheets.HEAD_ANIMATION.copy(), owner.sheets.HEAD_ANIMATION.copy(), x, y, False, 252)

        self.animation.sprites[8].resize_image(1.1)
        self.animation.sprites[9].resize_image(1.1)
        self.animation.set_current(8)
        self.nostril_tick = 0.0

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

#This is the bottom of the head, right in between the lips.
class head_bottom(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int) -> None:
        super().__init__(owner, owner.sheets.HEAD_ANIMATION.copy(), owner.sheets.HEAD_ANIMATION.copy(), x, y, False, 250)

        self.animation.sprites[3].resize_image(1.3)
        self.animation.set_current(3)

    def update(self) -> None:
        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y

#These are the lips just below the head.
class head_lip(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.HEAD_ANIMATION.copy(), owner.sheets.HEAD_ANIMATION.copy(), x, y, flip, 253)

        self.animation.set_current(4 if not flip else 5)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.16

        #Handles the movement of the vines to be natural.
        inverse_tick = self.tick if self.origin_x > 300 else -self.tick
        bobbing_x = sin(inverse_tick * 2) * 4
        bobbing_y = sin(self.tick * 0.75) * 5

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        self.get_sprite().resize_image_set(1 + (sin(self.tick * 0.75) * 4 / 100.0))

#These are the teeth attached to the lips.
class head_teeth(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.HEAD_ANIMATION.copy(), owner.sheets.HEAD_ANIMATION.copy(), x, y, flip, 254)

        self.animation.set_current(6 if not flip else 7)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.16

        #Handles the movement of the vines to be natural.
        inverse_tick = self.tick if self.origin_x > 300 else -self.tick
        bobbing_x = sin(inverse_tick * 2) * 4
        bobbing_y = sin(self.tick * 0.75) * 5

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        self.get_sprite().resize_image_set(1 + (sin(self.tick * 0.75) * 4 / 100.0))

#These are the dimples which go above the lips/teeth.
class head_dimple(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.HEAD_ANIMATION.copy(), owner.sheets.HEAD_ANIMATION.copy(), x, y, flip, 255)

        self.animation.sprites[1].resize_image(1.15)
        self.animation.sprites[2].resize_image(1.15)
        self.animation.set_current(1 if not flip else 2)

    def update(self) -> None:
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.16

        #Handles the movement of the vines to be natural.
        inverse_tick = self.tick if self.origin_x > 300 else -self.tick
        bobbing_x = sin(inverse_tick * 2) * 4
        bobbing_y = sin(self.tick * 0.5)

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x + bobbing_x
        self.y = self.origin_y + self.owner.y + bobbing_y
        self.get_sprite().resize_image_set(1 + (sin(self.tick * 0.5) * 2 / 100.0))

#These are the eye-sockets which go to the outer rim of the lips.
class eye_socket(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.EYE_SOCKET_ANIMATION_LEFT, owner.sheets.EYE_SOCKET_ANIMATION_RIGHT, x, y, flip, 256)

        self.get_sprite().resize_image(0.8)

    def update(self) -> None:
        self.animation.update()
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.24

        #Handles the movement of the vines to be natural.
        bobbing_y = sin(self.tick) * 2

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y + bobbing_y

#These are the eyes which go in the eye sockets.
class eye(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.EYE_ANIMATION_LEFT, owner.sheets.EYE_ANIMATION_RIGHT, x, y, flip, 257)

        self.get_sprite().resize_image(0.75)

    def update(self) -> None:
        self.animation.update()
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.2

        #Handles the movement of the vines to be natural.
        bobbing_y = sin(self.tick) * 1.5

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y + bobbing_y

#These are the pupils which go in the eyes.
class eye_pupil(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.PUPIL_ANIMATION, owner.sheets.PUPIL_ANIMATION, x, y, flip, 258, force_center = True)

        self.get_sprite().resize_image(0.5)

    def update(self) -> None:
        self.animation.update()
        #If the stalks are moving at a certain pace, then increase the bobbing ticks.
        if STALK_SPEED > 1:
            self.tick += 0.2

        #Handles the movement of the vines to be natural.
        bobbing_y = sin(self.tick) * 1.6

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        self.x = self.origin_x + self.owner.x
        self.y = self.origin_y + self.owner.y + bobbing_y
        self.get_sprite().resize_image_set(0.5 + (sin(self.tick * 1.15) * 15 / 100.0))

#These are the six circles of piping coming out of Flowey's face and TV.
class piping(flowey_piece):
    def __init__(self, owner: flowey, x: int, y: int, index: int, direction: int, flip: bool) -> None:
        super().__init__(owner, owner.sheets.PIPE_ANIMATION.copy(), owner.sheets.PIPE_ANIMATION.copy(), x, y, flip, 249 - index, force_center = True)

        self.animation.set_current(int(direction / 2))

        self.get_sprite().resize_image(0.5)
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

        if self.delay_tick < self.my_delay:
            self.delay_tick += 1
        elif not self.grow:
            self.grow_tick += 1
            
            if self.grow_tick % self.pause == 0:
                self.grow = True
                self.size_velocity = 0.0075
        elif self.grow:
            self.size += self.size_velocity
            self.size_velocity -= 0.0004
            
            if self.size < 0.5:
                self.size = 0.5
                self.size_velocity = 0
                self.grow = False

            self.get_sprite().resize_image_set(self.size)


        #Handles the movement of the vines to be natural.
        #bobbing_y = sin(self.tick) * 1.6

        #Allows the owner (Flowey) to affect the x and y positioning of the organs.
        #self.x = self.origin_x + self.owner.x
        #self.y = self.origin_y + self.owner.y + bobbing_y
        #self.get_sprite().resize_image_set(0.5 + (sin(self.tick * 1.15) * 15 / 100.0))