from sprites import animation, predef_spritesheets
from sound import predef_effects
from input import keyboard
from pygame import Surface
from random import randint
from sound import effect

MY_SCREEN = None

#Setup to allow for screen shaking.
class fonts_init:
	def __init__(self, my_screen) -> None:
		global MY_SCREEN

		MY_SCREEN = my_screen

#Set up the Undertale story.
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
		#Lists use to store the texts.
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
		pre_fight_speed = 3

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

	#Play a specific story.
	def play(self, story: list) -> None:
		self.stories_played += 1
		self.current_story = story
		self.current = 0
		self.events = 0
		self.play_new_line = True
		self.story_finished = False

	#Wait for Z to be pressed to continue to the next line.
	def wait_for_z(self) -> None:
		if self.await_z_press == 1 and not self.keyboard.is_z():
			self.await_z_press = 2
		elif self.await_z_press == 2 and self.keyboard.is_z():
			self.await_z_press = 3

	def update(self) -> None:
		#If there is a story...
		if self.current_story != None:
			#If the current position is more than the length of the current story...
			if self.current >= len(self.current_story):
				#Finish the story.
				self.story_finished = True

				return

			#Get the current line from the story.
			self.current_line = self.current_story[self.current]

			#If there is a current line, update the line.
			if self.current_line != None:
				self.current_line.update()

			#If the current line is not displayed yet...
			if self.play_new_line:
				#Then say the current line retrieved.
				if self.current_line.say_line():
					#Increase the events by 1.
					self.events += 1

				#No longer display the current line.
				self.play_new_line = False

			#If there is no font in the current line...
			if self.current_line.font == None:
				#Check if it is a clear line.
				if self.current_line.clear:
					#If so, just continue.
					self.current += 1

				return

			#If the line is not done...
			if not self.current_line.font.complete:
				#Stop here.
				return

			#If the line is auto proceeding...
			if self.current_line.auto_proceed:
				#Play a new line upon completion.
				self.play_new_line = True
				self.current += 1
				return

			#Otherwise, we wait for the Z key to be pressed.
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

#This creates a line to state certain text to the screen.
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

	#Print the data to the screen.
	def say_line(self) -> bool:
		self.font.say(self.text, self.x, self.y, self.shake, self.sound, self.speed)

		return self.change_event

	def update(self):
		self.font.update()

	def render(self, screen: Surface):
		self.font.render(screen)

#This creates a line to clear the text from the screen.
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

#Creates the font according to the user's specifications.
class custom_font:
	#Typical initial setup.
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

	#Figure out what to print to the screen or if the screen should clear -> {c=True}.
	def say(self, text: str, x: int, y: int, shake: bool = False, voice: effect = None, speed: int = 5) -> None:
		#This if statement is if we are clearing the screen.
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
		#Otherwise, hook up the data of the parameters to the font to print.
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
	
	#This function spells out the text written either instantaneously or at the speed specified.
	def update(self) -> None:
		#If the current position is less than the length of the text to print or there is a required delay...
		if self.current < len(self.text) or self.extra_delay > 0:
			#Make sure the printing is incomplete.
			self.complete = False

			#If there is a delay...
			if self.extra_delay > 0:
				#Tick upwards.
				self.extra_tick += 1

				#Once the ticking has reached the delay required, reset the tick to end the delay.
				if self.extra_tick >= self.extra_delay:
					self.extra_delay = 0
			#Otherwise...
			else:
				#Increase the generic tick.
				self.tick += 1

				#If our texting speed is more than 0 and the generic tick is an increment of our speed...
				if self.speed > 0 and self.tick % self.speed == 0:
					#Then get the character from the "current" variable's position within the text.
					char = self.text[self.current]
					#Get the index location of the character found in our allowed characters.
					index = self.allowed.find(char)

					#Verify if there are special instructions within the character...
					if self.check_special_instructions(char)[0]:
						#If there are, then stop here.
						return

					#If there is a proper index...
					if index > -1:
						#Add the letter to the list to render.
						self.letters.append(letter(self.animation.sprites[index].image, self.x, self.y, self.is_high(char), self.get_y_offset(char)))

						#If there is a voice associated, play it.
						if self.voice != None:
							self.voice.play()

					#Increase the cursor x position by 16.
					self.x += 16

					#If we need a new line...
					if char == '\n':
						#Return the x position to the origin, reset the extra delay, and lower the y position.
						self.x = self.origin_x
						self.y += 38
						self.extra_delay = 0
					#Otherwise, if the character is non-sentence-ending punctuation...
					elif char == ',' or char == ':' or char == ';':
						#Delay the text from spelling out for 10 ticks (1/6th second).
						self.extra_delay = 10
						self.extra_tick = 0
					#Otherwise, if the character is sentence-ending punctuations...
					elif char == '.' or char == '!' or char == '?':
						#Verify the text is not a "...". If it isn't...
						if self.current >= len(self.text) - 1 or self.text[self.current + 1] != '.':
							#Delay the text from spelling out for 15 ticks (1/4th second).
							self.extra_delay = 15
							self.extra_tick = 0
					#Otherwise, just make there no delay.
					else:
						self.extra_delay = 0

					#Increase the current index by 1.
					self.current += 1
				#Otherwise, if the speed is instantaneous...
				elif self.speed <= 0:
					skip_amount = 0

					#Loop through the text...
					for i in range(len(self.text)):
						#Get the character found at the index.
						char = self.text[i]
						#Get the index of the character from the allowed characters list.
						index = self.allowed.find(char)

						#Check if there are special instructions with the character.
						cont, skip = self.check_special_instructions(char)

						#If we need to continue or skip text...
						if cont or skip_amount > 0:
							#Decrease how much we need to skip.
							skip_amount -= 1

							#If we are set to skip text...
							if skip > 0:
								#Increase the skip amount to that.
								skip_amount += skip

							#Finally, skip to the next iteration.
							continue

						#If there is a proper index...
						if index > -1:
							#Add the letter to be rendered to the screen.
							self.letters.append(letter(self.animation.sprites[index].image, self.x, self.y, self.is_high(char), self.get_y_offset(char)))

						#Move the cursor to the right 16 pixels.
						self.x += 16

						#If there is a newline character...
						if char == '\n':
							#Reset the x position to the original position.
							self.x = self.origin_x
							#Increase the y position.
							self.y += 38

						#Continue to the next letter.
						self.current += 1
		#Otherwise, make the text completely rendered.
		else:
			self.complete = True

		#If the text needs to shake...
		if self.shake:
			#Then increase the shaking tick.
			self.shake_tick += 1

			#If the shakeing tick is an increment of 3...
			if self.shake_tick % 3 == 0:
				#Shake all the letters.
				for item in self.letters:
					item.random_shake()

		#Update the letters.
		for item in self.letters:
			item.update()

	#Here we check for special instructions and perform the instruction if it is found.
	def check_special_instructions(self, char: str):
		#If the character provided is an opening curly bracket...
		if char == '{':
			#Prepare values for skipping and the statement if required.
			output_i = 0
			statement = ""

			#Loop until the end of the text...
			for i in range(len(self.text) - self.current):
				#Add text to the statement with the self.current offset.
				statement += self.text[self.current + i]

				#If there is an ending curly bracket...
				if self.text[self.current + i] == '}':
					#Change the index of the self.current by the current i.
					self.current += i + 1
					#Update the output_i to the current i.
					output_i = i + 1
					#Remove the brackets from the statement.
					statement = statement[1:-1]

					#Exit the loop.
					break

			#If we want to delay...
			if statement.startswith("d="):
				#Verify the amount of time to delay.
				statement = int(statement[2:])

				self.extra_delay = statement
			#If we want to change the y position...
			elif statement.startswith("p="):
				#Verify the amount to change the y position by.
				statement = int(statement[2:])

				self.y += statement

			#Force the text to continue and skip the amount of text provided by output_i.
			return True, output_i

		#If nothing has been found, then just continue like normal.
		return False, 0

	#Clear the screen of letters.
	def clear(self) -> None:
		self.say("{c=True}", 0, 0, False, None, 0)

	def render(self, screen: Surface):
		for item in self.letters:
			screen.blit(item.image, item.image_rect)

	#Check if there is a y offset.
	def is_high(self, char: str) -> bool:
		return self.get_y_offset(char) != 0

	#Get the y offset for certain characters.
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

#The normal white undertale font.
class undertale_font(custom_font):
	def __init__(self, all_spritesheets: predef_spritesheets) -> None:
		super().__init__(all_spritesheets.UNDERTALE_FONT_ANIMATION, """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':,!_.?";#$%&()@[]^-`{}~+=*/\\><|""")

#The normal yellow undertale font. Only the characters required where used.
class undertale_yellow_font(custom_font):
	def __init__(self, all_spritesheets: predef_spritesheets) -> None:
		super().__init__(all_spritesheets.UNDERTALE_YELLOW_FONT_ANIMATION, "ACDEFILORSVaeinorstu3")

#This handles each individual letter used.
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

	#If the letters are shaking, we call this function.
	def random_shake(self, x_limit: int = 1, y_limit: int = 1) -> None:
		self.x_rand = randint(-x_limit, x_limit)
		self.y_rand = randint(-y_limit, y_limit)

	def update(self) -> None:
		self.image_rect.left = self.x + self.x_rand + self.my_screen.x

		if self.top_only:
			self.image_rect.top = self.y + self.y_rand + self.my_screen.x - self.image.get_height() + self.y_offset
		else:
			self.image_rect.bottom = self.y + self.y_rand + self.my_screen.y