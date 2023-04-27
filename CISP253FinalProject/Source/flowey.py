from sprites import *
from entity import *
from math import sin, cos, radians

STALK_SPEED = 3
ORGAN_SIZE_OFFSET = 1.0

class flowey:
    def __init__(self, window, my_screen, sheets: predef_spritesheets, x: int, y: int) -> None:
        global ORGAN_SIZE_OFFSET

        self.window = window
        self.my_screen = my_screen
        self.x = x
        self.y = y
        self.origin_x = x
        self.origin_y = y
        self.brightness = 0
        self.sheets = sheets
        self.visible = False
        self.move_to_0 = False
        self.reveal_flowey = False
        self.laugh = 0

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
        self.entities.add(eye_pupil_small(self, 249, 177, False))
        self.entities.add(eye_pupil_small(self, 377, 177, True))
        self.entities.add(eye_top(self, 155, 120, False))
        self.entities.add(eye_top(self, 405, 120, True))
        self.entities.add(eye_pupil_large(self, 193, 136, False))
        self.entities.add(eye_pupil_large(self, 432, 136, True))

        self.entities.add(background(self, 150, 10))

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

        self.tick = 0

        self.set_brightness_all()

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
        global STALK_SPEED

        for entity in self.entities.entities:
            entity.update()

        self.tick += 1

        if self.move_to_0 and self.origin_y < 0:
            self.origin_y += 0.6

            if self.origin_y > 0:
                self.origin_y = 0
                self.move_to_0 = False

        if self.tick == 960 and self.origin_y == 0 and not self.reveal_flowey:
            self.entities.add(white_overlay(self.entities.get_items_by_class(television).first(), self.sheets))
        elif self.reveal_flowey and self.brightness < 255 and self.laugh == 0:
            STALK_SPEED = 1

            self.brightness += 20

            if self.brightness > 255:
                self.brightness = 255
                self.laugh = 1
                self.tick = 0

            self.set_brightness_all()
        elif self.laugh == 1 and self.tick == 60:
            self.laugh = 2
            self.window.run_event(4, 5)
        elif self.laugh == 2 and self.tick == 450:
            self.laugh = 3
        elif self.laugh == 3 and self.tick == 510:
            self.window.run_event(5, 0)
            STALK_SPEED = 3

        self.x = self.origin_x + self.my_screen.x
        self.y = self.origin_y + self.my_screen.y

    def render(self, screen: Surface) -> None:
        if not self.visible:
            return

        for entity in self.entities.entities:
            entity.render(screen)

class white_overlay(entity):
    def __init__(self, tv: 'television', spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.TV_OVERLAY_ANIMATION, 0, 0, False, False)

        self.tv = tv

        self.x = self.tv.x + 17
        self.y = self.tv.y + self.tv.height / 2 - self.height / 3 + 3
        self.opacity = 0
        self.tick = 0
        self.layer = 3000

        self.get_sprite().change_opacity(self.opacity)
        self.face = flowey_face(self, spritesheets)
        self.tv.owner.entities.add(self.face)

    def set_brightness(self, _: int):
        pass

    def update(self) -> None:
        if STALK_SPEED < 3:
            self.x = self.tv.x + 17
            self.y = self.tv.y + self.tv.height / 2 - self.height / 3 + 3

        self.get_sprite().change_opacity(self.opacity)

        self.opacity += 4

        if self.opacity > 255:
            self.opacity = 255

    def render(self, screen: Surface) -> None:
        if not self.visible:
            return

        screen.blit(self.get_sprite().image, self.get_data())

class flowey_face(entity):
    def __init__(self, overlay: 'white_overlay', spritesheets: predef_spritesheets) -> None:
        super().__init__(spritesheets.TV_FACE_ANIMATION, 0, 0, True, False)

        self.overlay = overlay

        self.x = self.overlay.x + self.overlay.width / 2 - self.width / 2
        self.y = self.overlay.y + self.overlay.height / 2 - 32
        self.y_offset = 0
        self.opacity = self.overlay.opacity
        self.tick = 0
        self.layer = self.overlay.layer + 1
        self.full_smile = False

        self.get_sprite().change_opacity(self.opacity)

    def set_brightness(self, _: int):
        pass

    def update(self) -> None:
        c_height = self.get_sprite().get_height()

        self.animation.update()

        n_height = self.get_sprite().get_height()

        self.y_offset -= int((n_height - c_height) / 2) if self.animation.index < 11 else 0

        self.opacity = self.overlay.opacity
        self.x = self.overlay.x + self.overlay.width / 2 - self.width / 2
        self.y = self.overlay.y + self.overlay.height / 2 - 32 - self.y_offset
        self.get_sprite().change_opacity(self.opacity)

        if self.overlay.tv.owner.laugh < 2:
            if self.opacity >= 255:
                if self.animation.index < 6:
                    self.animation.increment = 5
                elif self.animation.index == 6 and self.tick < 60:
                    self.animation.increment = 0
                    self.tick += 1
                elif self.animation.index == 6:
                    self.animation.next()
                    self.animation.increment = 5
                    self.tick = 0
                elif self.animation.index == 10 and self.tick < 60:
                    self.animation.increment = 0
                    self.tick += 1
                elif self.animation.index == 10 and self.tick == 60:
                    self.overlay.tv.owner.reveal_flowey = True
                    self.overlay.tv.owner.window.run_event(4, 4)
                    self.tick += 1
        elif self.overlay.tv.owner.laugh == 2:
            self.y_offset = -22
            self.animation.increment = 4

            if self.animation.index > 13:
                self.animation.set_current(11)
        else:
            self.y_offset = -14
            self.animation.increment = 0
            self.animation.set_current(14)

    def render(self, screen: Surface) -> None:
        if not self.visible:
            return

        screen.blit(self.get_sprite().image, self.get_data())

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

        if create_dark_piece_automatically:
            self.create_dark_piece(force_center)

    def create_dark_piece(self, force_center: bool, resize: float = 1.0) -> None:
        self.darkness = dark_piece(self, self.animation, force_center, resize)
        self.owner.entities.add(self.darkness)

    def set_brightness(self, brightness: int) -> None:
        self.brightness = brightness

    def readjust_size(self) -> None:
        self.animation.resize_images(1.0)

    def render(self, screen: Surface) -> None:
        if not self.visible:
            return

        screen.blit(self.get_sprite().image, self.get_data())

class dark_piece(flowey_piece):
    def __init__(self, owner: flowey_piece, animation: animation, force_center: bool = False, resize: float = 1.0) -> None:
        super().__init__(owner, animation, animation, owner.x, owner.y, False, 0, force_center, False, True, False)

        if resize != 1.0:
            self.animation.resize_images_set_defaults(resize)

        self.owner = owner
        self.animation.make_silhouette()
        self.brightness = self.owner.brightness
        self.visible = True
        self.layer = self.owner.layer + 1000

    def update(self) -> None:
        self.brightness = self.owner.brightness

        self.x = self.owner.x
        self.y = self.owner.y
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

class extender(flowey_piece):
    def __init__(self, owner: background) -> None:
        super().__init__(owner, owner.owner.sheets.EXTENDER_ANIMATION, None, 0, 0, False, 249, False, False, True, False)

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