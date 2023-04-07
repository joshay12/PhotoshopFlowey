import pygame

#A spritesheet class dedicated to handling more than one image and spliting them up amongst sprites.
class spritesheet:
    #The constructor needs the path of the image(s), the name of the image(s), and the amount of items to loop through.
    def __init__(self, path: str, name: str, amount: int = 1) -> None:
        #Set up the class with its path, name, and amount properties.
        self.path = path
        self.name = name
        self.amount = amount
        #Prepare to load a mass amount of images.
        self.images = []

        #Loop through the amount.
        for i in range(amount):
            #Append the path, name, and the current loop iteration as an image to the images list.
            self.images.append(pygame.image.load(self.path + "/" + self.name + str(i + 1) + ".bmp"))

    #Pre-make the rotated images for slower loading times, but faster runtime.
    def make_rotated_images(self, degree_increments: int) -> bool:
        #Do not allow anything more or less than 1 image in the spritesheet.
        if len(self.images > 1):
            print("You cannot have more than 1 image in the spritesheet to make rotated images.")
            return False
        elif len(self.images == 0):
            print("You cannot have 0 images in the spritesheet to make rotated images.")
            return False

        rotator = self.images[0]
    
        #Add the rotated images according to the degree_increments provided to the image list of the spritesheet.
        for i in range(int(360 / degree_increments) - 1):
            self.images.append(pygame.transform.rotate(rotator, (i + 1) * degree_increments))
    
        return True

    #Pre-make the rotated images for slower loading times, but faster runtime.
    def make_rotated_images_range(self, degree_increments: int, start: int, end: int) -> bool:
        #Do not allow anything more or less than 1 image in the spritesheet.
        if len(self.images) > 1:
            print("You cannot have more than 1 image in the spritesheet to make rotated images.")
            return False
        elif len(self.images) == 0:
            print("You cannot have 0 images in the spritesheet to make rotated images.")
            return False

        rotator = self.images[0]

        for i in range(int(360 / degree_increments) - 1):
            self.images.append(pygame.transform.rotate(rotator, (i + 1 + start) * degree_increments))

            if (i + 1 + start) * degree_increments >= end:
                break

    #Return a new sprite found at the index of the spritesheet.
    def get_sprite(self, index: int = 0) -> 'sprite':
        return sprite(self.images, index)

    #Resize the image of the sprite found at the index provided to the percentage provided.
    def resize_image(self, index: int, percent: float) -> None:
        image = self.images[index]

        width = image.get_width()
        height = image.get_height()

        self.images[index] = pygame.transform.scale(self.images[index], (width * percent, height * percent))

    #Convert all the images into sprites from the spritesheet and return the result.
    def get_sprites(self) -> list:
        output = []

        for i in range(len(self.images)):
            output.append(self.get_sprite(i))

        return output

    #Resize an entire spritesheet of images according to the tuple provided for size.
    def resize_images(self, size: tuple) -> 'spritesheet':
        for i in range(len(self.images)):
            self.resize_image(i, size)

        return self

#A sprite class for wraping around the pygame image.
#This is used because of spritesheet and makes animations simpler.
class sprite:
    #The constructor needs the spritesheet to retrieve from and the index to get from the images list.
    def __init__(self, images: list, index: int = 0) -> None:
        #Typical class setup.
        self.index = index
        self.image = images[index]
        self.current_brightness = 0
        self.origin_image = images[index].copy()

    #Simply rotates the sprite's image horizontally.
    def flip_horizontal(self) -> 'sprite':
        return sprite([pygame.transform.flip(self.image, True, False)])

    #Simply rotates the sprite's image vertically.
    def flip_vertical(self) -> 'sprite':
        return sprite([pygame.transform.flip(self.image, False, True)])

    #Rotates the sprite's image both horizontally and vertically.
    def flip_both(self) -> 'sprite':
        return sprite([pygame.transform.flip(self.image, True, True)])

    def resize_image(self, percent: float) -> None:
        width = self.image.get_width()
        height = self.image.get_height()

        self.image = pygame.transform.scale(self.image, (width * percent, height * percent))

    def resize_image_set(self, percent: float) -> None:
        width = self.origin_image.get_width()
        height = self.origin_image.get_height()

        self.image = pygame.transform.smoothscale(self.origin_image, (width * percent, height * percent))

    def set_brightness(self, brightness: int) -> None:
        new_image = pygame.Surface(self.origin_image.get_size())

        pixels = pygame.PixelArray(self.origin_image)
        adjusted = pygame.PixelArray(new_image)

        for y in range(new_image.get_height()):
            for x in range(new_image.get_width()):
                color = pixels[x, y]

                r = min(max(int(((color >> 16) & 0xFF) + brightness), 0), 255)
                g = min(max(int(((color >> 8) & 0xFF) + brightness), 0), 255)
                b = min(max(int((color & 0xFF) + brightness), 0), 255)

                adjusted[x, y] = (r << 16) | (g << 8) | b

        del pixels
        del adjusted

        self.image = new_image
    
    #Easy way to get the width of the image.
    def get_width(self) -> int:
        return self.image.get_width()

    #Easy way to get the height of the image.
    def get_height(self) -> int:
        return self.image.get_height()

#A class used to flip between sprites at a certain increment to assist with animations.
class animation:
    #The constructor requires the list of sprites being used to animation as well as the frequency to swap images (the increment)
    def __init__(self, sprites: list, increment: int) -> None:
        #There cannot be no sprites as the class depends on at least 1 sprite existing.
        if sprites == None or len(sprites) == 0 or sprites[0] == None:
            raise Exception("You must have more than 0 sprites within your animation.")

        #Normal class setup.
        self.index = 0
        self.tick = 0
        self.amount_to_skip = 1
        self.increment = increment
        self.sprites = sprites
        #Initialize the current animation sprite to be the first sprite within the list.
        self.current = self.sprites[0]

    #Updates the animation according to what "forward" is set to.
    #If this function is not called, the animation will not update.
    def update(self, forward: bool = True) -> None:
        #Consistently increase the tick.
        self.tick += 1

        #Checks if the updates (60 per second) have surpassed the provided increment.
        if self.increment > 0 and self.tick % self.increment == 0 and self.amount_to_skip != 0:
            if self.amount_to_skip == 1:
                #If it does, then proceed to the next or previous animation frame depending on the "forward" variable.
                self.next() if forward else self.previous()
            elif self.amount_to_skip != 1:
                #If the amount of images to skip in the animation is more or less than 1, then proceed to skip frames of the animation.
                self.change_animation(self.amount_to_skip)

    #Flips all sprites in the animation horizontally.
    def flip_all_horizontally(self) -> 'animation':
        sprites = []

        for sprite in self.sprites:
            sprites.append(sprite.flip_horizontal())

        return animation(sprites, self.increment)

    #Flips all sprites in the animation vertically.
    def flip_all_vertically(self) -> 'animation':
        sprites = []

        for sprite in self.sprites:
            sprites.append(sprite.flip_vertical())

        return animation(sprites, self.increment)

    #Flips all sprites in the animation both horizontally and vertically.
    def flip_all_both(self) -> 'animation':
        sprites = []

        for sprite in self.sprites:
            sprites.append(sprite.flip_both())

        return animation(sprites, self.increment)

    #Changes the animation frame the amount set within the parameter.
    def change_animation(self, amount: int) -> None:
        #Increases the animation from the amount provided and prevents the index from exceeding the animation limits.
        self.index += amount
        
        if self.index < 0:
            self.index = len(self.sprites) - 1
        elif self.index > len(self.sprites) - 1:
            self.index = 0

        #Update the current sprite to the current index.
        self.current = self.sprites[self.index]

    #Easily skips to the next frame of the animation.
    def next(self) -> None:
        self.change_animation(1)

    #Easily reverts to the previous frame of the animation.
    def previous(self) -> None:
        self.change_animation(-1)

    #Resets everything within the animation.
    def reset(self) -> None:
        self.index = 0
        self.tick = 0
        self.current = self.sprites[0]

    #Sets the current frame of the animation rather than adding or subtracting from it.
    def set_current(self, index: int) -> None:
        self.index = index

        #If the index is beyond what can be handled, handle it appropriately.
        if self.index < 0:
            self.index = len(self.sprites) - 1
        elif self.index > len(self.sprites) - 1:
            self.index = 0

        #Update the current sprite to the current index.
        self.current = self.sprites[self.index]

    #Resize the image of the sprite found at the index provided to the percentage provided.
    def resize_image(self, index: int, percent: float) -> 'sprite':
        self.sprites[index].resize_image(percent)

        return sprite([self.sprites[index].image])
        #width = self.sprites[index].get_width()
        #height = self.sprites[index].get_height()
        #
        #return sprite([pygame.transform.scale(self.sprites[index].image, (width * percent, height * percent))])

    #Resize an entire animation according to the tuple provided for size.
    def resize_images(self, percent: float) -> 'animation':
        sprites = []

        for i in range(len(self.sprites)):
            sprites.append(self.resize_image(i, percent))

        return animation(sprites, self.increment)

    def copy(self) -> 'animation':
        sprites = []

        for i in range(len(self.sprites)):
            sprites.append(sprite([self.sprites[i].image]))

        return animation(sprites, self.increment)

FLOWEY_PATH = "Resources/Images/Omega Flowey/"

#STALKS ANIMATION
STALKS_SPRITESHEET = spritesheet(FLOWEY_PATH + "Stalks", "Stalk", 62).resize_images(0.4)
STALKS_ANIMATION_LEFT = animation(STALKS_SPRITESHEET.get_sprites(), 1)
STALKS_ANIMATION_RIGHT = STALKS_ANIMATION_LEFT.flip_all_horizontally()

#ORGANS ANIMATION
ORGANS_SPRITESHEET = spritesheet(FLOWEY_PATH + "Misc", "Organs", 1).resize_images(0.6)
ORGANS_ANIMATION_LEFT = animation(ORGANS_SPRITESHEET.get_sprites(), 0)
ORGANS_ANIMATION_RIGHT = ORGANS_ANIMATION_LEFT.flip_all_horizontally()

#HANDS ANIMATION
HANDS_SPRITESHEET = spritesheet(FLOWEY_PATH + "Hands", "Hand", 1).resize_images(0.5)
HANDS_ANIMATION_LEFT = animation(HANDS_SPRITESHEET.get_sprites(), 0)
HANDS_ANIMATION_RIGHT = HANDS_ANIMATION_LEFT.flip_all_horizontally()

#VINES ANIMATION
VINES_1_SPRITESHEET = spritesheet(FLOWEY_PATH + "Misc", "Vine1-", 1).resize_images(0.5)
VINES_1_ANIMATION_LEFT = animation(VINES_1_SPRITESHEET.get_sprites(), 0)
VINES_1_ANIMATION_RIGHT = VINES_1_ANIMATION_LEFT.flip_all_horizontally()
VINES_2_SPRITESHEET = spritesheet(FLOWEY_PATH + "Misc", "Vine2-", 1).resize_images(0.5)
VINES_2_ANIMATION_LEFT = animation(VINES_2_SPRITESHEET.get_sprites(), 0)
VINES_2_ANIMATION_RIGHT = VINES_2_ANIMATION_LEFT.flip_all_horizontally()
VINES_3_SPRITESHEET = spritesheet(FLOWEY_PATH + "Misc", "Vine3-", 1).resize_images(0.5)
VINES_3_ANIMATION_LEFT = animation(VINES_3_SPRITESHEET.get_sprites(), 0)
VINES_3_ANIMATION_RIGHT = VINES_3_ANIMATION_LEFT.flip_all_horizontally()

#TV ANIMATION
TV_SPRITESHEET = spritesheet(FLOWEY_PATH + "TV", "TV", 3).resize_images(0.5)
TV_ANIMATION = animation(TV_SPRITESHEET.get_sprites(), 0)

#FULL HEAD ANIMATION
HEAD_SPRITESHEET = spritesheet(FLOWEY_PATH + "Head", "Head", 10).resize_images(0.5)
HEAD_ANIMATION = animation(HEAD_SPRITESHEET.get_sprites(), 0)

#EYE SOCKET ANIMATION
EYE_SOCKET_SPRITESHEET_LEFT = spritesheet(FLOWEY_PATH + "Eyes", "EyeSocketLeft", 1).resize_images(0.5)
EYE_SOCKET_SPRITESHEET_RIGHT = spritesheet(FLOWEY_PATH + "Eyes", "EyeSocketRight", 1).resize_images(0.5)
EYE_SOCKET_ANIMATION_LEFT = animation(EYE_SOCKET_SPRITESHEET_LEFT.get_sprites(), 0)
EYE_SOCKET_ANIMATION_RIGHT = animation(EYE_SOCKET_SPRITESHEET_RIGHT.get_sprites(), 0)