from pygame import mixer, sndarray
from numpy import interp, arange

SONGS = None
EFFECTS = None

class song:
    def __init__(self, path: str, name: str, extension: str = ".wav") -> None:
        self.sound = mixer.Sound(path + name + extension)
        self.channel = mixer.find_channel()

    def play(self, volume: float = 1.0, pitch: float = 1.0, loops: int = -1) -> None:
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
    def __init__(self, path: str, name: str, extension: str = ".wav") -> None:
        self.sound = mixer.Sound(path + name + extension)
        self.channel = mixer.find_channel()

    def play(self, volume_left: float = 1.0, volume_right: float = 1.0, pitch: float = 1.0, loops: int = 0) -> None:
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

class predef_effects:
    def __init__(self) -> None:
        location = "Resources/Sounds/Effects/"

        self.FLOWEY_TALK_NORMAL = effect(location, "flowey_normal")
        self.FLOWEY_TALK_INTENSE = effect(location, "flowey_intense")