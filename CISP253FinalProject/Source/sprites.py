from PIL import Image, ImageEnhance
import pygame

SPRITESHEETS = None

#A spritesheet class dedicated to handling more than one image and spliting them up amongst sprites.
class spritesheet:
    #The constructor needs the path of the image(s), the name of the image(s), and the amount of items to loop through.
    def __init__(self, screen: pygame.Surface, path: str, name: str, amount: int = 1, extension: str = ".bmp") -> None:
        #Set up the class with its path, name, and amount properties.
        self.path = path
        self.name = name
        self.amount = amount
        #Prepare to load a mass amount of images.
        self.images = []

        #Loop through the amount.
        for i in range(amount):
            #Append the path, name, and the current loop iteration as an image to the images list.
            self.images.append(pygame.image.load(self.path + "/" + self.name + str(i + 1) + extension).convert_alpha(screen))

    #Pre-make the rotated images for slower loading times, but faster runtime.
    def make_rotated_images(self, degree_increments: int) -> bool:
        #Do not allow anything more or less than 1 image in the spritesheet.
        if len(self.images) > 1:
            print("You cannot have more than 1 image in the spritesheet to make rotated images.")
            return False
        elif len(self.images) == 0:
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
        self.origin_image_string = pygame.image.tostring(self.origin_image, "RGBA")
        self.size = 1.0

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
        self.size = percent

    def set_brightness(self, brightness: float) -> None:
        image = Image.frombuffer("RGBA", self.origin_image.get_size(), self.origin_image_string, "raw", "RGBA", 0, 1)
        enhancer = ImageEnhance.Brightness(image)
        new_image = enhancer.enhance(brightness)

        self.image = pygame.image.fromstring(new_image.tobytes(), new_image.size, new_image.mode)
        #self.resize_image_set(1.0)
    
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

    def clear_all_but(self, index: int) -> 'animation':
        #return self
        return animation([self.sprites[index - 1]], self.increment)

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

class predef_spritesheets:
    def __init__(self, screen: pygame.Surface) -> None:
        #Introduction Screen Animation
        self.INTRO_SCREEN_SPRITESHEET = spritesheet(screen, "Resources/Images/Intro Screen", "image", 2, ".png")
        self.INTRO_SCREEN_ANIMATION = animation(self.INTRO_SCREEN_SPRITESHEET.get_sprites(), 0)

        #File Backdrop Animations
        self.FILE_BACKDROP_PATH = "Resources/Images/File Backdrop/"

        self.FILE_BACKDROP_SPRITESHEET = spritesheet(screen, self.FILE_BACKDROP_PATH, "file", 2, ".png")
        self.FILE_BACKDROP_ANIMATION = animation(self.FILE_BACKDROP_SPRITESHEET.get_sprites(), 0)

        self.FILE_CRACKS_SPRITESHEET = spritesheet(screen, self.FILE_BACKDROP_PATH, "cracks", 3, ".png")
        self.FILE_CRACKS_ANIMATION = animation(self.FILE_CRACKS_SPRITESHEET.get_sprites(), 0)

        self.FILE_SHATTERED_SPRITESHEET = spritesheet(screen, self.FILE_BACKDROP_PATH, "erased_shatter", 6, ".png")
        self.FILE_SHATTERED_ANIMATION = animation(self.FILE_SHATTERED_SPRITESHEET.get_sprites(), 0)

        #Player Animations
        self.PLAYER_PATH = "Resources/Images/Player/"

        self.PLAYER_DOWN_SPRITESHEET = spritesheet(screen, self.PLAYER_PATH + "Character", "player_down", 4, ".png")
        self.PLAYER_UP_SPRITESHEET = spritesheet(screen, self.PLAYER_PATH + "Character", "player_up", 4, ".png")
        self.PLAYER_LEFT_SPRITESHEET = spritesheet(screen, self.PLAYER_PATH + "Character", "player_left", 2, ".png")
        self.PLAYER_RIGHT_SPRITESHEET = spritesheet(screen, self.PLAYER_PATH + "Character", "player_right", 2, ".png")
        self.PLAYER_DOWN_ANIMATION = animation(self.PLAYER_DOWN_SPRITESHEET.get_sprites(), 0)
        self.PLAYER_UP_ANIMATION = animation(self.PLAYER_UP_SPRITESHEET.get_sprites(), 0)
        self.PLAYER_LEFT_ANIMATION = animation(self.PLAYER_LEFT_SPRITESHEET.get_sprites(), 0)
        self.PLAYER_RIGHT_ANIMATION = animation(self.PLAYER_RIGHT_SPRITESHEET.get_sprites(), 0)

        #Save Star Animation
        self.SAVE_STAR_SPRITESHEET = spritesheet(screen, "Resources/Images/Save Star", "save", 2, ".png")
        self.SAVE_STAR_ANIMATION = animation(self.SAVE_STAR_SPRITESHEET.get_sprites(), 10)

        #Font Animations
        self.UNDERTALE_FONT_SPRITESHEET = spritesheet(screen, "Resources/Images/Fonts/Undertale/", "", 94, ".png").resize_images(0.5)
        self.UNDERTALE_FONT_ANIMATION = animation(self.UNDERTALE_FONT_SPRITESHEET.get_sprites(), 0)

        self.UNDERTALE_YELLOW_FONT_SPRITESHEET = spritesheet(screen, "Resources/Images/Fonts/UndertaleYellow/", "", 21, ".png").resize_images(0.5)
        self.UNDERTALE_YELLOW_FONT_ANIMATION = animation(self.UNDERTALE_YELLOW_FONT_SPRITESHEET.get_sprites(), 0)

        self.FLOWEY_PATH = "Resources/Images/Omega Flowey/"

        #SCREEN ANIMATION
        self.SCREEN_SPRITESHEET = spritesheet(screen, "Resources/Images/Filters/", "screen", 1)
        self.SCREEN_ANIMATION = animation(self.SCREEN_SPRITESHEET.get_sprites(), 0)

        #BACKGROUND ANIMATION
        self.BACKGROUND_SPRITESHEET = spritesheet(screen, self.FLOWEY_PATH + "Misc", "Backdrop", 1)
        self.BACKGROUND_ANIMATION = animation(self.BACKGROUND_SPRITESHEET.get_sprites(), 0)

        #STALKS ANIMATION
        self.STALKS_SPRITESHEET = spritesheet(screen, self.FLOWEY_PATH + "Stalks", "Stalk", 62).resize_images(0.4)
        self.STALKS_ANIMATION_LEFT = animation(self.STALKS_SPRITESHEET.get_sprites(), 1)
        self.STALKS_ANIMATION_RIGHT = self.STALKS_ANIMATION_LEFT.flip_all_horizontally()

        #ORGANS ANIMATION
        self.ORGANS_SPRITESHEET = spritesheet(screen, self.FLOWEY_PATH + "Misc", "Organs", 1).resize_images(0.6)
        self.ORGANS_ANIMATION_LEFT = animation(self.ORGANS_SPRITESHEET.get_sprites(), 0)
        self.ORGANS_ANIMATION_RIGHT = self.ORGANS_ANIMATION_LEFT.flip_all_horizontally()

        #HANDS ANIMATION
        self.HANDS_SPRITESHEET = spritesheet(screen, self.FLOWEY_PATH + "Hands", "Hand", 1).resize_images(0.5)
        self.HANDS_ANIMATION_LEFT = animation(self.HANDS_SPRITESHEET.get_sprites(), 0)
        self.HANDS_ANIMATION_RIGHT = self.HANDS_ANIMATION_LEFT.flip_all_horizontally()

        #VINES ANIMATION
        self.VINES_1_SPRITESHEET = spritesheet(screen, self.FLOWEY_PATH + "Misc", "Vine1-", 1).resize_images(0.5)
        self.VINES_1_ANIMATION_LEFT = animation(self.VINES_1_SPRITESHEET.get_sprites(), 0)
        self.VINES_1_ANIMATION_RIGHT = self.VINES_1_ANIMATION_LEFT.flip_all_horizontally()
        self.VINES_2_SPRITESHEET = spritesheet(screen, self.FLOWEY_PATH + "Misc", "Vine2-", 1).resize_images(0.5)
        self.VINES_2_ANIMATION_LEFT = animation(self.VINES_2_SPRITESHEET.get_sprites(), 0)
        self.VINES_2_ANIMATION_RIGHT = self.VINES_2_ANIMATION_LEFT.flip_all_horizontally()
        self.VINES_3_SPRITESHEET = spritesheet(screen, self.FLOWEY_PATH + "Misc", "Vine3-", 1).resize_images(0.5)
        self.VINES_3_ANIMATION_LEFT = animation(self.VINES_3_SPRITESHEET.get_sprites(), 0)
        self.VINES_3_ANIMATION_RIGHT = self.VINES_3_ANIMATION_LEFT.flip_all_horizontally()

        #TV ANIMATION
        self.TV_SPRITESHEET = spritesheet(screen, self.FLOWEY_PATH + "TV", "TV", 3).resize_images(0.5)
        self.TV_ANIMATION = animation(self.TV_SPRITESHEET.get_sprites(), 0)

        #FULL HEAD ANIMATION
        self.HEAD_SPRITESHEET = spritesheet(screen, self.FLOWEY_PATH + "Head", "Head", 10).resize_images(0.5)
        self.HEAD_ANIMATION = animation(self.HEAD_SPRITESHEET.get_sprites(), 0)

        #EYE SOCKET ANIMATION
        self.EYE_SOCKET_SPRITESHEET_LEFT = spritesheet(screen, self.FLOWEY_PATH + "Eyes", "EyeSocketLeft", 1).resize_images(0.5)
        self.EYE_SOCKET_SPRITESHEET_RIGHT = spritesheet(screen, self.FLOWEY_PATH + "Eyes", "EyeSocketRight", 1).resize_images(0.5)
        self.EYE_SOCKET_ANIMATION_LEFT = animation(self.EYE_SOCKET_SPRITESHEET_LEFT.get_sprites(), 0)
        self.EYE_SOCKET_ANIMATION_RIGHT = animation(self.EYE_SOCKET_SPRITESHEET_RIGHT.get_sprites(), 0)

        #SIDE EYE ANIMATION
        self.EYE_SPRITESHEET_LEFT = spritesheet(screen, self.FLOWEY_PATH + "Eyes", "EyeLeft", 1).resize_images(0.5)
        self.EYE_SPRITESHEET_RIGHT = spritesheet(screen, self.FLOWEY_PATH + "Eyes", "EyeRight", 1).resize_images(0.5)
        self.EYE_ANIMATION_LEFT = animation(self.EYE_SPRITESHEET_LEFT.get_sprites(), 0)
        self.EYE_ANIMATION_RIGHT = animation(self.EYE_SPRITESHEET_RIGHT.get_sprites(), 0)

        #PUPIL ANIMATION
        self.PUPIL_SPRITESHEET = spritesheet(screen, self.FLOWEY_PATH + "Eyes", "Pupil", 2)
        self.PUPIL_ANIMATION = animation(self.PUPIL_SPRITESHEET.get_sprites(), 0)

        #PIPE ANIMATION
        self.PIPE_SPRITESHEET = spritesheet(screen, self.FLOWEY_PATH + "Misc", "Pipe", 1)
        self.PIPE_SPRITESHEET.make_rotated_images(2)
        self.PIPE_ANIMATION = animation(self.PIPE_SPRITESHEET.get_sprites(), 0)

        #TOP EYE ANIMATION
        self.EYE_TOP_SPRITESHEET_LEFT = spritesheet(screen, self.FLOWEY_PATH + "Eyes", "EyeTopLeft", 1).resize_images(0.5)
        self.EYE_TOP_SPRITESHEET_RIGHT = spritesheet(screen, self.FLOWEY_PATH + "Eyes", "EyeTopRight", 1).resize_images(0.5)
        self.EYE_TOP_ANIMATION_LEFT = animation(self.EYE_TOP_SPRITESHEET_LEFT.get_sprites(), 0)
        self.EYE_TOP_ANIMATION_RIGHT = animation(self.EYE_TOP_SPRITESHEET_RIGHT.get_sprites(), 0)