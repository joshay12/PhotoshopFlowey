from pygame import mixer, sndarray
from numpy import interp, arange

#These help the init py file to retrieved pre-loaded songs and sound effects.
SONGS = None
EFFECTS = None

#This class is dedicated to songs. That's all there is to it.
class song:
    def __init__(self, path: str, name: str, extension: str = ".ogg") -> None:
        #We create the sound and try to find an available channel for the sound.
        self.sound = mixer.Sound(path + name + extension)
        self.channel = mixer.find_channel()

    #This plays the song according to the specified data.
    def play(self, volume: float = 1.0, pitch: float = 1.0, loops: int = -1) -> None:
        #We find a new channel that is available to play from.
        self.channel = mixer.find_channel()

        #If the pitch is different, change the pitch of the song.
        if pitch != 1.0:
            self.change_pitch(pitch)

        #Set the volume of the song.
        self.channel.set_volume(volume, volume)

        #If this song is already playing, then stop it from playing.
        if self.is_playing():
            self.channel.stop()

        #Play the song.
        self.channel.play(self.sound, loops)

    #Check whether or not the song is playing or not.
    def is_playing(self) -> bool:
        return self.channel.get_busy()

    #Pause the song.
    def pause(self) -> None:
        self.channel.pause()

    #Resume playing the song.
    def resume(self) -> None:
        self.channel.unpause()
        
    #Stop the song from playing.
    def stop(self) -> None:
        self.channel.stop()

    #Adjust the volume of the song.
    def set_volume(self, volume: float) -> None:
        self.channel.set_volume(volume, volume)

    #Change the pitch of the song.
    #To be honest, I have no idea how this function works. This is a product of ChatGPT, so I used it.
    def change_pitch(self, pitch: float) -> 'effect':
        sound_array = sndarray.samples(self.sound).ravel()
        
        resampled_array = interp(arange(0, len(sound_array), pitch), arange(0, len(sound_array)), sound_array).astype(sound_array.dtype)

        self.sound = mixer.Sound(buffer = resampled_array)

        return self

#This class is dedicated to sound effects. That's all there is to it.
class effect:
    #There are only miniscule differences between this class and the song class; therefore, I will only go over what is different.
    def __init__(self, path: str, name: str, extension: str = ".ogg") -> None:
        self.sound = mixer.Sound(path + name + extension)
        self.channel = mixer.find_channel()

    def play(self, volume_left: float = 1.0, volume_right: float = 1.0, pitch: float = 1.0, loops: int = 0) -> None:
        self.channel = mixer.find_channel()

        if pitch != 1.0:
            self.change_pitch(pitch)

        #Allow panning to word with volume_left and volume_right.
        self.channel.set_volume(volume_left, volume_right)

        if self.is_playing():
            self.channel.stop()
            
        #Loop 0 times rather than infinite times by default (can still be changed).
        self.channel.play(self.sound, loops)

    def is_playing(self) -> bool:
        return self.channel.get_busy()

    def pause(self) -> None:
        self.channel.pause()

    def resume(self) -> None:
        self.channel.unpause()
        
    def stop(self) -> None:
        self.channel.stop()

    #This changes the volume, but with specifically the left and right provided.
    def change_pan(self, volume_left: float, volume_right: float) -> None:
        self.channel.set_volume(volume_left, volume_right)

    def set_volume(self, volume: float) -> None:
        self.channel.set_volume(volume, volume)

    def change_pitch(self, pitch: float) -> 'effect':
        sound_array = sndarray.samples(self.sound).ravel()
        
        resampled_array = interp(arange(0, len(sound_array), pitch), arange(0, len(sound_array)), sound_array).astype(sound_array.dtype)

        self.sound = mixer.Sound(buffer = resampled_array)

        return self

#This is a pre-loaded class with songs loaded on it.
class predef_songs:
    def __init__(self) -> None:
        location = "Resources/Sounds/Songs/"

        self.STORY = song(location, "story")
        self.STORY_FROZEN = song(location, "frozen_story")
        self.YOU_IDIOT = song(location, "you_idiot")
        self.FLOWEY_MEGA_LAUGH = song(location, "mega_laugh")
        self.YOUR_BEST_NIGHTMARE_INTRO = song(location, "your_best_nightmare_intro")
        self.YOUR_BEST_NIGHTMARE_THEME1 = song(location, "your_best_nightmare_theme1")

#This is a pre-loaded class with sound effects loaded on it.
class predef_effects:
    def __init__(self) -> None:
        location = "Resources/Sounds/Effects/"

        self.FLOWEY_TALK_NORMAL = effect(location, "flowey_normal")
        self.FLOWEY_TALK_INTENSE = effect(location, "flowey_intense")
        self.HEAL = effect(location, "heal")
        self.PUNCH = effect(location, "punch")
        self.PUNCH_SLOWER = effect(location, "punch_slower")
        self.PUNCH_SLOWEST = effect(location, "punch_slowest")
        self.EXPLOSION = effect(location, "explosion")
        self.SHORT_STATIC = effect(location, "short_static")
        self.SHORT_MEDIUM_STATIC = effect(location, "short_medium_static")
        self.MEDIUM_STATIC = effect(location, "medium_static")
        self.STATIC = effect(location, "static")
        self.FLOWEY_CREEPY_LAUGH_NORMAL = effect(location, "flowey_creepy_laugh")
        self.FLOWEY_CREEPY_LAUGH_SLOW = effect(location, "flowey_creepy_laugh_slow")
        self.SOUL_PREPARE = effect(location, "prepare_for_battle")
        self.SOUL_SEND_TO_BATTLE = effect(location, "send_to_battle")
        self.SOUL_HURT = effect(location, "hurt")