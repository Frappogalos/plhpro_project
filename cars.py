import pygame
import random
from traffic_lights import TrafficLights


class Cars(pygame.sprite.Sprite):
    car_image_1 = "images/cars/car_01.png"
    car_image_2 = "images/cars/car_02.png"
    starting_positions = {}
    cars_group = pygame.sprite.Group()
    groups_directions = {}
    last_spawn = 0
    cars_limit = 10

    def __init__(self, pos, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(random.choice([Cars.car_image_1, Cars.car_image_2]))
        self.image = pygame.transform.rotate(self.image, 90*direction)
        self.direction = direction
        self.velocity = self.find_velocity()
        self.rect = self.image.get_rect()
        self.rect.center = pygame.Vector2(pos)
        self.stopped = None
        self.tr_light = None
        if pygame.sprite.spritecollideany(self, Cars.cars_group):
            self.kill()
        else:
            Cars.cars_group.add(self)
            Cars.groups_directions[str(self.direction)].add(self)
            Cars.last_spawn = pygame.time.get_ticks()

    def update(self):
        self.restart_movement()
        self.detect_collision()
        self.detect_traffic_light()
        self.rect.center += self.velocity
        self.map_boundaries()

    def map_boundaries(self):
        if (self.rect.centerx < -90 or self.rect.centery < -90 or
                self.rect.centerx > pygame.display.get_window_size()[0] + 90 or
                self.rect.centery > pygame.display.get_window_size()[1] + 90):
            self.kill()

    def detect_collision(self):
        for i in Cars.groups_directions[str(self.direction)]:
            if i != self and self.direction == 1 and 0 < self.rect.y - i.rect.y < 100:
                self.velocity = pygame.Vector2(0, 0)
                self.stopped = i
            elif i != self and self.direction == 2 and 0 < self.rect.x - i.rect.x < 100:
                self.velocity = pygame.Vector2(0, 0)
                self.stopped = i
            elif i != self and self.direction == 3 and -100 < self.rect.y - i.rect.y < 0:
                self.velocity = pygame.Vector2(0, 0)
                self.stopped = i
            elif i != self and self.direction == 4 and -100 < self.rect.x - i.rect.x < 0:
                self.velocity = pygame.Vector2(0, 0)
                self.stopped = i
        if TrafficLights.groups_directions["1"][0].light == "off" and (self.direction == 1 or self.direction == 3):
            for i in Cars.groups_directions["4"]:
                if self.direction == 1 and 0 < self.rect.y - i.rect.y < 100 and 0 < self.rect.x - i.rect.x < 200:
                    self.velocity = pygame.Vector2(0, 0)
                    self.stopped = i
                elif self.direction == 3 and -200 < self.rect.y - i.rect.y < -150 and 50 < self.rect.x - i.rect.x < 400:
                    self.velocity = pygame.Vector2(0, 0)
                    self.stopped = i
            for i in Cars.groups_directions["2"]:
                if self.direction == 3 and -100 < self.rect.y - i.rect.y < 0 and -200 < self.rect.x - i.rect.x < 0:
                    self.velocity = pygame.Vector2(0, 0)
                    self.stopped = i
                elif self.direction == 1 and 150 < self.rect.y - i.rect.y < 200 and -400 < self.rect.x - i.rect.x < -50:
                    self.velocity = pygame.Vector2(0, 0)
                    self.stopped = i

    def restart_movement(self):
        if (self.stopped is not None and pygame.math.Vector2(self.rect.x, self.rect.y).
                distance_to((self.stopped.rect.x, self.stopped.rect.y)) > 120):
            self.velocity = self.find_velocity()
            self.stopped = None

    def find_velocity(self):
        if self.direction == 1:
            return pygame.Vector2(0, -2)
        elif self.direction == 2:
            return pygame.Vector2(-2, 0)
        elif self.direction == 3:
            return pygame.Vector2(0, 2)
        else:
            return pygame.Vector2(2, 0)

    def detect_traffic_light(self):
        for i in TrafficLights.groups_directions[str(self.direction)]:
            if ((self.direction == 1 and 50 < self.rect.y - i.rect.y < 100) or
                    (self.direction == 2 and 50 < self.rect.x - i.rect.x < 100) or
                    (self.direction == 3 and -100 < self.rect.y - i.rect.y < -50) or
                    (self.direction == 4 and -100 < self.rect.x - i.rect.x < -50)):
                if i.light == "red" or i.light == "orange":
                    self.velocity = pygame.Vector2(0, 0)
                    self.tr_light = i
                elif self.tr_light is not None and (self.tr_light.light == "green" or self.tr_light.light == "off"):
                    self.velocity = self.find_velocity()
                    self.tr_light = None

    @classmethod
    def create_cars(cls):
        now = pygame.time.get_ticks()
        if now - Cars.last_spawn > 2000 and len(Cars.cars_group) <= Cars.cars_limit:
            rand_num = random.randint(1, 100)
            if rand_num <= 15:
                direction = 1
            elif rand_num <= 50:
                direction = 2
            elif rand_num <= 65:
                direction = 3
            else:
                direction = 4
            Cars(pos=Cars.starting_positions[str(direction)], direction=direction)
