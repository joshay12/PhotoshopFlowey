from sprites import animation
from pygame import Surface

class undertale_font:
	ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':,!_.?\";#$%&()@[]^-`{}~+=*/\\><|"

	def __init__(self, animation: animation) -> None:
		self.animation = animation
		self.x = 0
		self.y = 0
		self.speed = 0
		self.text = ""
		self.current = 0
		self.tick = 0
		self.images = []

	def say(self, text: str, x: int, y: int, speed: int) -> None:
		self.x = x
		self.y = y
		self.text = text
		self.current = 0
		self.tick = 0
		self.images = []
		self.speed = speed
	
	def update(self) -> None:
		if self.current < len(self.text):
			self.tick += 1

			if self.tick % self.speed == 0:
				index = self.ALLOWED_CHARS.find(self.text[self.current])

				self.current += 1

				if index > -1:
					self.images.append((self.animation.sprites[index].image, self.x, self.y))

				self.x += 24

	def clear(self) -> None:
		self.images = []

	def render(self, screen: Surface):
		for item in self.images:
			sprite = item[0]
			sprite_rect = sprite.get_rect()
			sprite_rect.left = item[1]
			sprite_rect.bottom = item[2]

			screen.blit(sprite, sprite_rect)