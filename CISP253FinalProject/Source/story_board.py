from pygame import Surface
from fonts import story

class story_board:
    def __init__(self, story: story, window) -> None:
        self.running = False
        self.pause_loop = False
        self.last_event = 0
        self.story = story
        self.normal_font = story.undertale
        self.yellow_font = story.undertale_yellow
        self.window = window

    def begin(self) -> None:
        self.story.play(self.story.pre_story_lines)
        self.running = True

    def update(self) -> None:
        if self.running and not self.pause_loop:
            self.story.update()
            self.check_events()

    def render(self, screen: Surface) -> None:
        if self.running and not self.pause_loop:
            self.story.render(screen)

    def check_events(self) -> None:
        if self.last_event == self.story.events or self.story.current_story == None:
            return

        self.last_event = self.story.events

        if self.story.current_story == self.story.pre_story_lines:
            if self.last_event == 1:
                self.window.run_event(0, 0)