import pygame


class Button:
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.image_name = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_over(self, pos):
        if self.x - self.rect.width/2 < pos[0] < self.x + self.rect.width/2:
            if self.y - self.rect.height/2 < pos[1] < self.y + self.rect.height/2:
                return True

        return False
