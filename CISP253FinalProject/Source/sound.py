from pygame import mixer

class effect:
    def __init__(self, path: str, name: str, extension: str = ".mp3") -> None:
        self.sound = mixer.Sound(path + name + extension)
        self.channel = mixer.find_channel()

    def play(self, volume_left: float = 1.0, volume_right: float = 1.0) -> None:
        self.channel.set_volume(volume_left, volume_right)
        self.channel.play()

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