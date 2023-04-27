from sprites import animation, predef_spritesheets
from sound import predef_effects
from input import keyboard
from pygame import Surface
from random import randint
from sound import effect

MY_SCREEN = None

class fonts_init:
	def __init__(self, my_screen) -> None:
		global MY_SCREEN

		MY_SCREEN = my_screen

class story:
	def __init__(self, spritesheets: predef_spritesheets, effects: predef_effects, keyboard: keyboard) -> None:
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
		self.pre_fight_story_before_first_snicker = []
		self.pre_fight_story_before_second_snicker = []
		self.pre_fight_story_before_walk = []
		self.pre_fight_story_before_fight = []
		self.current_line = None
		self.story_finished = True

		#There are 60 ticks per second.
		#For instant text, set the Speed to 0.
		#To delay the text, use {d=<TICK_AMOUNT>} ("d" referencing "delay")
		#To move the text up or down, use {p=<Y_POSITION_TO_MOVE>}

		#Parameter usage: Font, Text, X, Y, Sound Effect, Speed, Shake, Delay, Auto Proceed, and Change Event.
		self.pre_story_lines.append(line(self.undertale, "Long ago, two races\nruled over the Earth:\nHUMANS and MONSTERS{d=75}", 120, 325, None, 4, 0, 0, True, False))
		self.pre_story_lines.append(line(self.undertale, "One day, the{d=30}", 120, 325, None, 5, 0, 0, True, False))
		self.pre_story_lines.append(line(self.undertale, "One day, they all\ndisappeared without\na trace.{d=300}", 120, 325, None, 0, 0, 0, True, True))
		self.pre_story_lines.append(clear_line(True))

		pre_fight_y_location = 275
		pre_fight_speed = 0

		self.pre_fight_story_before_first_snicker.append(line(self.undertale, "Howdy!", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, False))
		self.pre_fight_story_before_first_snicker.append(line(self.undertale, "It's me, FLOWEY.", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, False))
		self.pre_fight_story_before_first_snicker.append(line(self.undertale, "FLOWEY the FLOWER!", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_first_snicker.append(line(self.undertale, "I owe you a HUGE thanks.", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_first_snicker.append(line(self.undertale, "You really did a number\non that old fool.", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_first_snicker.append(line(self.undertale, "Without you, I NEVER could\nhave gotten past him.", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_first_snicker.append(line(self.undertale, "But now, with YOUR help...", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_first_snicker.append(line(self.undertale, "He's DEAD.", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, True))
		self.pre_fight_story_before_first_snicker.append(line(self.undertale, "And I'VE got the human\nSOULS!", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, True))
		self.pre_fight_story_before_first_snicker.append(clear_line(True))

		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "Boy!", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, False))
		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "I've been empty for so\nlong...", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, False))
		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "It feels great to have a\nSOUL inside me again.", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "Mmmm, I can feel them\nwriggling...", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "Awww, you're feeling\nleft out, aren't you?", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "Well, that's just perfect.", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "After all, I only have\nsix souls.", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "I still need one more...", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "Before I become GOD.", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, True))
		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "And then, with my\nnewfound powers...", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, True))
		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "Monsters.", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, True))
		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "Humans.", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, True))
		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "Everyone.", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, True))
		self.pre_fight_story_before_second_snicker.append(line(self.undertale, "I'll show them all the REAL\nmeaning of this world.", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, True))
		self.pre_fight_story_before_second_snicker.append(clear_line(True))

		self.pre_fight_story_before_walk.append(line(self.undertale, "Oh, and forget about escaping\nto your old SAVE FILE.", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, False))
		self.pre_fight_story_before_walk.append(line(self.undertale, "It's gone FOREVER.", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, True))
		self.pre_fight_story_before_walk.append(line(self.undertale, "But don't worry.", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_walk.append(line(self.undertale, "Your old friend FLOWEY...", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_walk.append(line(self.undertale, "Has worked out a replacement\nfor you!", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_walk.append(line(self.undertale, "I'll SAVE over your own\ndeath.", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, True))
		self.pre_fight_story_before_walk.append(line(self.undertale, "So you can watch me tear\nyou to bloody pieces...", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, True))
		self.pre_fight_story_before_walk.append(line(self.undertale, "Over, and over, and over...", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, True))
		self.pre_fight_story_before_walk.append(clear_line(True))

		self.pre_fight_story_before_fight.append(line(self.undertale, "... what?", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, False))
		self.pre_fight_story_before_fight.append(line(self.undertale, "Do you really think\nyou can stop ME?", 120, pre_fight_y_location, effects.FLOWEY_TALK_INTENSE, pre_fight_speed, 1, 0, False, False))
		self.pre_fight_story_before_fight.append(line(self.undertale, "Hee hee hee...", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, pre_fight_speed, 0, 0, False, True))
		self.pre_fight_story_before_fight.append(line(self.undertale, "You really ARE an idiot.", 120, pre_fight_y_location, effects.FLOWEY_TALK_NORMAL, 8, 0, 0, False, True))
		self.pre_fight_story_before_fight.append(clear_line(True))

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

					if self.check_special_instructions(char)[0]:
						return

					if index > -1:
						self.letters.append(letter(self.animation.sprites[index].image, self.x, self.y, self.is_high(char), self.get_y_offset(char)))

						if self.voice != None:
							self.voice.play()

					self.x += 16

					if char == '\n':
						self.x = self.origin_x
						self.y += 38
						self.extra_delay = 0
					elif char == ',' or char == ':' or char == ';':
						self.extra_delay = 10
						self.extra_tick = 0
					elif char == '.' or char == '!' or char == '?':
						if self.current >= len(self.text) - 1 or self.text[self.current + 1] != '.':
							self.extra_delay = 15
							self.extra_tick = 0
					else:
						self.extra_delay = 0

					self.current += 1
				elif self.speed <= 0:
					skip_amount = 0

					for i in range(len(self.text)):
						char = self.text[i]
						index = self.allowed.find(char)

						cont, skip = self.check_special_instructions(char)

						if cont or skip_amount > 0:
							skip_amount -= 1

							if skip > 0:
								skip_amount += skip

							continue

						if index > -1:
							self.letters.append(letter(self.animation.sprites[index].image, self.x, self.y, self.is_high(char), self.get_y_offset(char)))

						self.x += 16

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

		for item in self.letters:
			item.update()

	def check_special_instructions(self, char: str):
		if char == '{':
			output_i = 0
			statement = ""

			for i in range(len(self.text) - self.current):
				statement += self.text[self.current + i]

				if self.text[self.current + i] == '}':
					self.current += i + 1
					output_i = i + 1
					statement = statement[1:-1]

					break

			if statement.startswith("d="):
				statement = int(statement[2:])

				self.extra_delay = statement
			elif statement.startswith("p="):
				statement = int(statement[2:])

				self.y += statement

			return True, output_i

		return False, 0

	def clear(self) -> None:
		self.say("{c=True}", 0, 0, False, None, 0)

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
		global MY_SCREEN

		self.my_screen = MY_SCREEN
		self.image = image
		self.x = x
		self.y = y
		self.x_origin = self.x
		self.y_origin = self.y
		self.x_rand = 0
		self.y_rand = 0
		self.y_offset = y_offset
		self.top_only = top_only
		self.image_rect = self.image.get_rect()
		self.image_rect.left = self.x + self.my_screen.x

		if self.top_only:
			self.image_rect.top = self.y + self.my_screen.y - self.image.get_height() + self.y_offset
		else:
			self.image_rect.bottom = self.y + self.my_screen.y

	def random_shake(self, x_limit: int = 1, y_limit: int = 1) -> None:
		self.x_rand = randint(-x_limit, x_limit)
		self.y_rand = randint(-y_limit, y_limit)

	def update(self) -> None:
		self.image_rect.left = self.x + self.x_rand + self.my_screen.x

		if self.top_only:
			self.image_rect.top = self.y + self.y_rand + self.my_screen.x - self.image.get_height() + self.y_offset
		else:
			self.image_rect.bottom = self.y + self.y_rand + self.my_screen.y