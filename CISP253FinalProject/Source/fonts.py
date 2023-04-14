from sprites import animation
from pygame import Surface
from random import randint

class undertale_font:
	ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':,!_.?\";#$%&()@[]^-`{}~+=*/\\><|"

	def __init__(self, animation: animation) -> None:
		self.animation = animation
		self.origin_x = 0
		self.x = 0
		self.y = 0
		self.text = ""
		self.shake = False
		self.speed = 0
		self.current = 0
		self.tick = 0
		self.shake_tick = 0
		self.letters = []

	def say(self, text: str, x: int, y: int, shake: bool = False, speed: int = 5) -> None:
		self.origin_x = x
		self.x = x
		self.y = y
		self.text = text
		self.shake = shake
		self.speed = speed
		self.current = 0
		self.tick = 0
		self.shake_tick = 0
		self.letters = []
	
	def update(self) -> None:
		if self.current < len(self.text):
			self.tick += 1

			if self.tick % self.speed == 0:
				print(self.tick)

				index = self.ALLOWED_CHARS.find(self.text[self.current])

				if index > -1:
					self.letters.append(letter(self.animation.sprites[index].image, self.x, self.y))

				self.x += 20

				if self.text[self.current] == '\n':
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

class letter:
	def __init__(self, image: Surface, x: int, y: int) -> None:
		self.image = image
		self.x = x
		self.y = y
		self.image_rect = self.image.get_rect()
		self.image_rect.left = x
		self.image_rect.bottom = y

	def random_shake(self, x_limit: int = 1, y_limit: int = 1) -> None:
		x_rand = randint(-x_limit, x_limit)
		y_rand = randint(-y_limit, y_limit)

		self.image_rect.left = self.x + x_rand
		self.image_rect.bottom = self.y + y_rand