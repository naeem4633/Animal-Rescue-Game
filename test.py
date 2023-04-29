import unittest
import pygame
from classes import Animal, Obstacle

class TestAnimal(unittest.TestCase):
    def setUp(self):
        self.animal = Animal("res/fox.png", 100, 100)

    def test_initialization(self):
        # check animal instantiation and position
        self.assertEqual(self.animal.rect.x, 100)
        self.assertEqual(self.animal.rect.y, 100)
        self.assertFalse(self.animal.is_vanished)

    def test_draw(self):
        # Create a fake window to pass to the draw function
        # and check if the animal rect was drawn in the correct position inside the window
        window = pygame.Surface((800, 800))
        self.animal.draw(window)
        expected_rect = pygame.Rect(100, 100, self.animal.image.get_width(), self.animal.image.get_height())
        self.assertEqual(self.animal.rect, expected_rect)

class TestObstacle(unittest.TestCase):
    # initialize pygame window
    def setUp(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 800))

    # check if the obstacle was set at the right position
    def test_setxy(self):
        obstacle = Obstacle("res/fire.png")
        obstacle.setxy(100, 100)
        self.assertEqual(obstacle.rect.x, 100)
        self.assertEqual(obstacle.rect.y, 100)

class TestPlayer(unittest.TestCase):
    # initialize pygame window
    def setUp(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 800))

    # check if the player's image exists and if the dimensions are correct
    def test_player_image(self):
        rescuer_image = pygame.image.load('res/rescuer-right.png')
        self.assertIsNotNone(rescuer_image)
        self.assertEqual(rescuer_image.get_width(), 64)
        self.assertEqual(rescuer_image.get_height(), 64)

if __name__ == '__main__':
    unittest.main()