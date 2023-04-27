from pygame import mixer, sndarray
from numpy import interp, arange

SONGS = None
EFFECTS = None

class song:
    def __init__(self, path: str, name: str, extension: str = ".ogg") -> None:
        self.sound = mixer.Sound(path + name + extension)
        self.channel = mixer.find_channel()

    def play(self, volume: float = 1.0, pitch: float = 1.0, loops: int = -1) -> None:
        self.channel = mixer.find_channel()

        if pitch != 1.0:
            self.change_pitch(pitch)

        self.channel.set_volume(volume, volume)

        if self.is_playing():
            self.channel.stop()

        self.channel.play(self.sound, loops)

    def is_playing(self) -> bool:
        return self.channel.get_busy()

    def pause(self) -> None:
        self.channel.pause()

    def resume(self) -> None:
        self.channel.unpause()
        
    def stop(self) -> None:
        self.channel.stop()

    def set_volume(self, volume: float) -> None:
        self.channel.set_volume(volume, volume)

    def change_pitch(self, pitch: float) -> 'effect':
        sound_array = sndarray.samples(self.sound).ravel()
        
        resampled_array = interp(arange(0, len(sound_array), pitch), arange(0, len(sound_array)), sound_array).astype(sound_array.dtype)

        self.sound = mixer.Sound(buffer = resampled_array)

        return self

class effect:
    def __init__(self, path: str, name: str, extension: str = ".ogg") -> None:
        self.sound = mixer.Sound(path + name + extension)
        self.channel = mixer.find_channel()

    def play(self, volume_left: float = 1.0, volume_right: float = 1.0, pitch: float = 1.0, loops: int = 0) -> None:
        self.channel = mixer.find_channel()

        if pitch != 1.0:
            self.change_pitch(pitch)

        self.channel.set_volume(volume_left, volume_right)

        if self.is_playing():
            self.channel.stop()
            
        self.channel.play(self.sound, loops)

    def is_playing(self) -> bool:
        return self.channel.get_busy()

    def pause(self) -> None:
        self.channel.pause()

    def resume(self) -> None:
        self.channel.unpause()
        
    def stop(self) -> None:
        self.channel.stop()

    def change_pan(self, volume_left: float, volume_right: float) -> None:
        self.channel.set_volume(volume_left, volume_right)

    def set_volume(self, volume: float) -> None:
        self.channel.set_volume(volume, volume)

    def change_pitch(self, pitch: float) -> 'effect':
        sound_array = sndarray.samples(self.sound).ravel()
        
        resampled_array = interp(arange(0, len(sound_array), pitch), arange(0, len(sound_array)), sound_array).astype(sound_array.dtype)

        self.sound = mixer.Sound(buffer = resampled_array)

        return self

class predef_songs:
    def __init__(self) -> None:
        location = "Resources/Sounds/Songs/"

        self.STORY = song(location, "story")
        self.STORY_FROZEN = song(location, "frozen_story")
        self.YOU_IDIOT = song(location, "you_idiot")
        self.FLOWEY_MEGA_LAUGH = song(location, "mega_laugh")
        self.YOUR_BEST_NIGHTMARE_INTRO = song(location, "your_best_nightmare_intro")
        self.YOUR_BEST_NIGHTMARE_THEME1 = song(location, "your_best_nightmare_theme1")

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