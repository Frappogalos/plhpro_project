import pygame


class PedestrianLights:
	ped_lights_list = []
	directions = [1, 2, 3, 4]
	images_dict = {"off": "images/traffic_lights/pedestrian_off.png",
				   "red": "images/traffic_lights/pedestrian_red.png",
				   "green": "images/traffic_lights/pedestrian_green.png"}
	images = {}

	def __init__(self, x, y, direction):
		self.operation = "off"
		self.light = "off"
		self.direction = direction
		self.image = self.find_image()
		self.x = x
		self.y = y
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)
		self.on_time = 0
		self.duration = 0
		self.delay = 1000
		PedestrianLights.ped_lights_list.append(self)

	def draw(self, screen):
		if self.operation == "green" and pygame.time.get_ticks() - self.on_time >= self.delay:
			self.light = self.operation
			self.operation = None
			self.image = self.find_image()
		if self.light == "green" and pygame.time.get_ticks() - self.on_time >= self.duration:
			self.light = "red"
			self.image = self.find_image()
		screen.blit(self.image, self.rect)

	def turn_green(self, duration):
		self.on_time = pygame.time.get_ticks()
		self.duration = duration
		self.operation = "green"
		self.image = self.find_image()

	def find_image(self):
		return PedestrianLights.images[self.direction][self.light]

	@classmethod
	def preload_images(cls):
		temp = {}
		for x in PedestrianLights.directions:
			for i in PedestrianLights.images_dict.keys():
				temp[i] = pygame.transform.rotate(pygame.image.load(PedestrianLights.images_dict[i]), 90 * x)
			PedestrianLights.images[x] = temp
			temp = {}


class TrafficLights:
	traffic_lights_list = []
	directions = [1, 2, 3, 4]
	groups_directions = {"1": [], "2": [], "3": [], "4": []}
	images_dict = {"off": "images/traffic_lights/car_off.png",
				   "red": "images/traffic_lights/car_red.png",
				   "orange": "images/traffic_lights/car_orange.png",
				   "green": "images/traffic_lights/car_green.png"}
	images = {}

	def __init__(self, x, y, direction, green_time=30000, orange_time=3000, red_time=15000):
		self.green_time = green_time
		self.orange_time = orange_time
		self.red_time = red_time
		self.operation = "off"
		self.light = "off"
		self.direction = direction
		self.image = self.find_image()
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.on_time = 0
		self.ped = []
		self.sync = []
		self.secondary = []
		self.next = None
		TrafficLights.traffic_lights_list.append(self)
		TrafficLights.groups_directions[str(self.direction)].append(self)

	def find_image(self):
		return TrafficLights.images[self.direction][self.light]

	def draw(self, screen):
		self.control_lights()
		screen.blit(self.image, self.rect)
		if self.next:
			self.next.draw(screen)
		for i in self.ped:
			i.draw(screen)
		for i in self.sync:
			i.draw(screen)
		for i in self.secondary:
			i.draw(screen)

	def control_lights(self):
		if self.light == "orange" and pygame.time.get_ticks() - self.on_time > self.orange_time:
			self.turn_red()
		elif self.light == "green" and pygame.time.get_ticks() - self.on_time > self.green_time:
			self.turn_orange()
		elif self.light == "red" and pygame.time.get_ticks() - self.on_time > self.red_time:
			self.turn_green()

	def turn_on(self):
		self.turn_green()
		if self.next:
			self.next.turn_on()
		for i in self.ped:
			i.light = "red"
			i.image = i.find_image()
		for i in self.secondary:
			i.turn_red()
		for i in self.sync:
			i.turn_on()

	def turn_off(self):
		self.light = "off"
		self.image = self.find_image()
		if self.next:
			self.next.turn_off()
		for i in self.ped:
			i.light = "off"
			i.image = i.find_image()
		for i in self.secondary:
			i.turn_off()
		for i in self.sync:
			i.turn_off()

	def turn_green(self):
		self.on_time = pygame.time.get_ticks()
		self.light = "green"
		self.image = self.find_image()
		for i in self.sync:
			i.turn_green()

	def turn_orange(self):
		self.on_time = pygame.time.get_ticks()
		self.light = "orange"
		self.image = self.find_image()
		for i in self.sync:
			i.turn_orange()

	def turn_red(self):
		self.on_time = pygame.time.get_ticks()
		self.light = "red"
		self.image = self.find_image()
		for i in self.sync:
			i.turn_red()
		for i in self.ped:
			i.turn_green(self.red_time - 5000)

	@classmethod
	def preload_images(cls):
		temp = {}
		for x in TrafficLights.directions:
			for i in TrafficLights.images_dict.keys():
				temp[i] = pygame.transform.rotate(pygame.image.load(TrafficLights.images_dict[i]), 90 * x)
			TrafficLights.images[x] = temp
			temp = {}
