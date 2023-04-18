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

        #The variables below are to assist in proceeding the story in a flow.
        #It may look like a complicated mess, but there's a method to the madness.

        #Whether or not the game is on the screen to choose "Continue" or "Restart"
        self.continue_or_restart_time = False
        #True if "Continue" is highlighted and False if "Restart" is highlighted.
        self.continue_or_restart = True
        #Checks if the "Right" or "Left" button is currently held on the "Continue/Restart" screen.
        self.continue_or_restart_held = True

    def begin(self) -> None:
        self.story.play(self.story.pre_story_lines)
        self.running = True

    def update(self) -> None:
        if self.running and not self.pause_loop:
            self.story.update()
            self.check_events()

        if self.pause_loop and self.continue_or_restart_time:
            self.select_continue_or_restart()

            self.normal_font.update()
            self.yellow_font.update()

    def render(self, screen: Surface) -> None:
        if self.running and not self.pause_loop:
            self.story.render(screen)

        if self.pause_loop and self.continue_or_restart_time:
            self.normal_font.render(screen)
            self.yellow_font.render(screen)

    def check_events(self) -> None:
        if self.last_event == self.story.events or self.story.current_story == None:
            return

        self.last_event = self.story.events

        if self.story.current_story == self.story.pre_story_lines:
            if self.last_event == 1:
                self.window.run_event(0, 0)
            elif self.last_event == 2:
                self.continue_or_restart_time = True
                self.pause_loop = True

    def select_continue_or_restart(self) -> None:
        if self.continue_or_restart:
            self.normal_font.say("Flowey    LV9999    9999:99\nMy World\n\n                Restart", 100, 170, False, None, 0)
            self.yellow_font.say("   Continue", 100, 284, False, None, 0)
        else:
            self.normal_font.say("Flowey    LV9999    9999:99\nMy World\n\n   Continue", 100, 170, False, None, 0)
            self.yellow_font.say("                Restart", 100, 284, False, None, 0)

        if self.continue_or_restart_held:
            if not self.story.keyboard.is_right() and not self.story.keyboard.is_left():
                self.continue_or_restart_held = False
        elif not self.continue_or_restart_held:
            if self.story.keyboard.is_right() or self.story.keyboard.is_left():
                self.continue_or_restart = not self.continue_or_restart
                self.continue_or_restart_held = True