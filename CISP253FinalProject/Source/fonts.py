from sprites import animation, predef_spritesheets
from pygame import Surface
from random import randint
from sound import effect

class custom_font:
	def __init__(self, animation: animation, allowed_characters) -> None:
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

	def say(self, text: str, x: int, y: int, shake: bool = False, voice: effect = None, speed: int = 5) -> None:
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
	
	def update(self) -> None:
		if self.current < len(self.text):
			if self.extra_delay > 0:
				self.extra_tick += 1

				if self.extra_tick >= self.extra_delay:
					self.extra_delay = 0
			else:
				self.tick += 1

				if self.speed > 0 and self.tick % self.speed == 0:
					char = self.text[self.current]
					index = self.allowed.find(char)

					if index > -1:
						self.letters.append(letter(self.animation.sprites[index].image, self.x, self.y, self.is_high(char), self.get_y_offset(char)))

						if self.voice != None:
							self.voice.play()

					self.x += 20

					if char == '\n':
						self.x = self.origin_x
						self.y += 30
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

						if index > -1:
							self.letters.append(letter(self.animation.sprites[index].image, self.x, self.y, self.is_high(char), self.get_y_offset(char)))

						self.x += 20

						if char == '\n':
							self.x = self.origin_x
							self.y += 30

						self.current += 1

		if self.shake:
			self.shake_tick += 1

			if self.shake_tick % 3 == 0:
				for item in self.letters:
					item.random_shake()

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