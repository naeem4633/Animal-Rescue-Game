import pygame
import random

class Animal:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_vanished = False

    def getImage(self):
        return self.image

    def draw(self, window):
        if not self.is_vanished:
            window.blit(self.image, self.rect)

    def vanish(self):
        self.is_vanished = True

    def getx(self):
        return self.rect.x
    def gety(self):
        return self.rect.y

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def setxy(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def spawn_randomly(self, rescuer_rect, animals, obstacle_list):
        x = random.randint(0, 700)
        y = random.randint(0, 700)
        is_overlapping_animal = False
        is_overlapping_rescuer = False
        for animal in animals:
            if abs(x - animal.getx()) < 100 and abs(y - animal.gety()) < 100:
                is_overlapping_animal = True
                break
        if abs(x - rescuer_rect.x) < 100 and abs(y - rescuer_rect.y) < 100:
            is_overlapping_rescuer = True
                
        if not is_overlapping_animal and not is_overlapping_rescuer:
            self.setxy(x, y)
            obstacle_list.add(self)