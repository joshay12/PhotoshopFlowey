from pygame import mixer

EFFECTS = None

class effect:
    def __init__(self, path: str, name: str, extension: str = ".wav") -> None:
        self.sound = mixer.Sound(path + name + extension)
        self.channel = mixer.find_channel()

    def play(self, volume_left: float = 1.0, volume_right: float = 1.0) -> None:
        self.channel.set_volume(volume_left, volume_right)

        if self.is_playing():
            self.channel.stop()

        self.channel.play(self.sound)

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

class predef_effects:
    def __init__(self) -> None:
        location = "Resources/Sounds/"

        self.FLOWEY_TALK_NORMAL = effect(location, "flowey_normal")
        self.FLOWEY_TALK_INTENSE = effect(location, "flowey_intense")