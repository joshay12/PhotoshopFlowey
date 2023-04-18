from sprites import animation, predef_spritesheets
from input import keyboard
from pygame import Surface
from random import randint
from sound import effect

class story:
	def __init__(self, spritesheets: predef_spritesheets, keyboard: keyboard) -> None:
		self.undertale = undertale_font(spritesheets)
		self.undertale_yellow = undertale_yellow_font(spritesheets)
		self.keyboard = keyboard
		self.current = 0
		self.skip = False
		self.await_z_press = 0
		self.events = 0
		self.stories_played = 0
		self.play_new_line = False
		self.pre_story_lines = []
		self.current_line = None
		self.story_finished = True

		#There are 60 ticks per second.
		#For instant text, set the Speed to 0.
		#To delay the text, use {d=<TICK_AMOUNT>} ("d" referencing "delay")

		#Parameter usage: Font, Text, X, Y, Sound Effect, Speed, Shake, Delay, Auto Proceed, and Change Event.
		self.pre_story_lines.append(line(self.undertale, "Long ago, two races\nruled over the Earth:\nHUMANS and MONSTERS{d=7}", 100, 100, None, 4, 0, 0, True, False))
		self.pre_story_lines.append(line(self.undertale, "One day, the{d=3}", 100, 100, None, 4, 0, 0, True, False))
		self.pre_story_lines.append(line(self.undertale, "One day, they all\ndisappeared without\na trace.{d=30}", 100, 100, None, 0, 0, 0, True, True))
		self.pre_story_lines.append(clear_line(True))

	def play(self, story: list) -> None:
		self.stories_played += 1
		self.current_story = story
		self.current = 0
		self.events = 0
		self.play_new_line = True
		self.story_finished = False

	def wait_for_z(self) -> None:
		if self.await_z_press == 1 and not self.keyboard.is_z():
			self.await_z_press = 2
		elif self.await_z_press == 2 and self.keyboard.is_z():
			self.await_z_press = 3

	def update(self) -> None:
		if self.current_story != None:
			if self.current >= len(self.current_story):
				self.story_finished = True

				return

			self.current_line = self.current_story[self.current]

			if self.current_line != None:
				self.current_line.update()

			if self.play_new_line:
				if self.current_line.say_line():
					self.events += 1

				self.play_new_line = False

			if self.current_line.font == None:
				if self.current_line.clear:
					self.current += 1

				return

			if not self.current_line.font.complete:
				return

			if self.current_line.auto_proceed:
				self.play_new_line = True
				self.current += 1
				return

			if self.await_z_press == 0 and self.current_line.font.complete:
				self.await_z_press = 1

			self.wait_for_z()

			if self.await_z_press == 0:
				self.play_new_line = True
				self.current += 1
				return

			if self.await_z_press == 3:
				self.await_z_press = 0
				self.play_new_line = True
				self.current += 1

	def render(self, screen: Surface) -> None:
		if self.current_line != None:
			self.current_line.render(screen)

class line:
	def __init__(self, font: 'custom_font', text: str, x: int, y: int, sound: effect = None, speed: int = 3, shake: int = 0, delay: int = 0, auto_proceed: bool = False, change_event: bool = False) -> None:
		self.font = font
		self.text = text
		self.x = x
		self.y = y
		self.sound = sound
		self.speed = speed
		self.shake = shake
		self.delay = delay
		self.auto_proceed = auto_proceed
		self.change_event = change_event
		self.clear = False

	def say_line(self) -> bool:
		self.font.say(self.text, self.x, self.y, self.shake, self.sound, self.speed)

		return self.change_event

	def update(self):
		self.font.update()

	def render(self, screen: Surface):
		self.font.render(screen)

class clear_line(line):
	def __init__(self, change_event: bool = False) -> None:
		super().__init__(None, "{c=True}", 0, 0, change_event = change_event)

		self.clear = True

	def say_line(self) -> bool:
		return self.change_event

	def update(self):
		pass

	def render(self, screen: Surface):
		pass

class custom_font:
	def __init__(self, animation: animation, allowed_characters: str) -> None:
		self.animation = animation
		self.allowed = allowed_characters
		self.origin_x = 0
		self.x = 0
		self.y = 0
		self.text = ""
		self.shake = False
		self.speed = 0
		self.extra_delay = 0
		self.extra_tick = 0
		self.current = 0
		self.tick = 0
		self.shake_tick = 0
		self.letters = []
		self.voice = None
		self.complete = False

	def say(self, text: str, x: int, y: int, shake: bool = False, voice: effect = None, speed: int = 5) -> None:
		if text != "{c=True}":
			self.origin_x = x
			self.x = x
			self.y = y
			self.text = text
			self.shake = shake
			self.speed = speed
			self.extra_delay = 0
			self.extra_tick = 0
			self.voice = voice
			self.current = 0
			self.tick = 0
			self.shake_tick = 0
			self.letters = []
			self.complete = False
		else:
			self.origin_x = 0
			self.x = 0
			self.y = 0
			self.text = ""
			self.shake = False
			self.speed = 0
			self.extra_delay = 0
			self.extra_tick = 0
			self.current = 0
			self.tick = 0
			self.shake_tick = 0
			self.letters = []
			self.voice = None
			self.complete = False
	
	def update(self) -> None:
		if self.current < len(self.text) or self.extra_delay > 0:
			self.complete = False

			if self.extra_delay > 0:
				self.extra_tick += 1

				if self.extra_tick >= self.extra_delay:
					self.extra_delay = 0
			else:
				self.tick += 1

				if self.speed > 0 and self.tick % self.speed == 0:
					char = self.text[self.current]
					index = self.allowed.find(char)

					if self.check_special_instructions(char):
						return

					if index > -1:
						self.letters.append(letter(self.animation.sprites[index].image, self.x, self.y, self.is_high(char), self.get_y_offset(char)))

						if self.voice != None:
							self.voice.play()

					self.x += 17

					if char == '\n':
						self.x = self.origin_x
						self.y += 38
						self.extra_delay = 0
					elif char == ',' or char == ':' or char == ';':
						self.extra_delay = 10
						self.extra_tick = 0
					elif char == '.' or char == '!' or char == '?':
						self.extra_delay = 15
						self.extra_tick = 0
					else:
						self.extra_delay = 0

					self.current += 1
				elif self.speed <= 0:
					for char in self.text:
						index = self.allowed.find(char)

						if self.check_special_instructions(char):
							return

						if index > -1:
							self.letters.append(letter(self.animation.sprites[index].image, self.x, self.y, self.is_high(char), self.get_y_offset(char)))

						self.x += 17

						if char == '\n':
							self.x = self.origin_x
							self.y += 38

						self.current += 1
		else:
			self.complete = True

		if self.shake:
			self.shake_tick += 1

			if self.shake_tick % 3 == 0:
				for item in self.letters:
					item.random_shake()

	def check_special_instructions(self, char: str) -> bool:
		if char == '{':
			statement = ""

			for i in range(len(self.text) - self.current):
				statement += self.text[self.current + i]

				if self.text[self.current + i] == '}':
					self.current += i + 1
					statement = statement[1:-1]

					break

			if statement.startswith("d="):
				statement = int(statement[2:])

				self.extra_delay = statement

			return True

		return False

	def clear(self) -> None:
		self.images = []

	def render(self, screen: Surface):
		for item in self.letters:
			screen.blit(item.image, item.image_rect)

	def is_high(self, char: str) -> bool:
		return self.get_y_offset(char) != 0

	def get_y_offset(self, char: str) -> int:
		if char == "'":
			return -10
		elif char == 'Q':
			return 4
		elif char == ',':
			return 5
		elif char == 'g' or char == 'p' or char == 'q' or char == 'y':
			return 6
		elif char == 'j':
			return 7

		return 0

class undertale_font(custom_font):
	def __init__(self, all_spritesheets: predef_spritesheets) -> None:
		super().__init__(all_spritesheets.UNDERTALE_FONT_ANIMATION, """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':,!_.?";#$%&()@[]^-`{}~+=*/\\><|""")

class undertale_yellow_font(custom_font):
	def __init__(self, all_spritesheets: predef_spritesheets) -> None:
		super().__init__(all_spritesheets.UNDERTALE_YELLOW_FONT_ANIMATION, "ACDEFILORSVaeinorstu3")

class letter:
	def __init__(self, image: Surface, x: int, y: int, top_only: bool = False, y_offset: int = 0) -> None:
		self.image = image
		self.x = x
		self.y = y
		self.y_offset = y_offset
		self.top_only = top_only
		self.image_rect = self.image.get_rect()
		self.image_rect.left = x

		if self.top_only:
			self.image_rect.top = y - self.image.get_height() + self.y_offset
		else:
			self.image_rect.bottom = y

	def random_shake(self, x_limit: int = 1, y_limit: int = 1) -> None:
		x_rand = randint(-x_limit, x_limit)
		y_rand = randint(-y_limit, y_limit)

		self.image_rect.left = self.x + x_rand

		if self.top_only:
			self.image_rect.top = self.y + y_rand - self.image.get_height() + self.y_offset
		else:
			self.image_rect.bottom = self.y + y_rand