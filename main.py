import pygame
import sys


# Initialize Pygame
pygame.init()

# Define the window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the window title
pygame.display.set_caption("Animal Rescue Game")

# Set up the font
font = pygame.font.Font(None, 32)

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# Define the forest green color
FOREST_GREEN = (34, 139, 34)

# Load the rescuer image
rescuer_image = pygame.image.load("res/rescuer-right.png")
rescuer_rect = rescuer_image.get_rect()
rescuer_damaged_image = pygame.image.load("res/rescuer-damaged.png")

animal_sanctuary_image = pygame.image.load("res/animalSanctuary.png")
animal_sanctuary_rect = animal_sanctuary_image.get_rect()
animal_sanctuary_rect.x = WINDOW_WIDTH/2 - 64
animal_sanctuary_rect.y = WINDOW_HEIGHT - 128

vet_sign_image = pygame.image.load("res/veterinary.png")
vet_sign_rect = vet_sign_image.get_rect()
vet_sign_rect.x = WINDOW_WIDTH/2 - 90
vet_sign_rect.y = WINDOW_HEIGHT - 96

game_over = False
level_passed = False
animal_counter = 0
required_number_of_animals = 2

# Define button sizes
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50

# Define button positions
start_button_rect = pygame.Rect((WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 - 50, 200, 100))
htp_button_rect = pygame.Rect((WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 75, 200, 100))
quit_button_rect = pygame.Rect((WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 200, 200, 100))
restart_button_rect = pygame.Rect((WINDOW_WIDTH/2 - 300, WINDOW_HEIGHT/2 + 250, 200, 100))
next_level_button_rect = pygame.Rect((WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 - 100, 200, 100))

restart_rect = pygame.draw.rect(window, (255, 0, 0), (WINDOW_WIDTH/2 - 50, WINDOW_HEIGHT/2 + 50, 100, 50))

# Define the Animal class
class Animal:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_vanished = False

    def draw(self, window):
        if not self.is_vanished:
            window.blit(self.image, self.rect)

    def vanish(self):
        self.is_vanished = True

    def get_image(self):
        return self.image

# Load the animal images and create animal objects
fox_image_path = "res/fox.png"
chameleon_image_path = "res/chameleon.png"
koala_image_path = "res/koala.png"
animals = [
    Animal(fox_image_path, 200, 300),
    Animal(chameleon_image_path, 300, 400),
    Animal(koala_image_path, 500, 600)
]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def setxy(self, x, y):
        self.rect.x = x
        self.rect.y = y

obstacle_list = pygame.sprite.Group()

fire = Obstacle("res/fire.png")
fire.setxy(150, 250)
garbage = Obstacle("res/garbage.png")
garbage.setxy(550, 350)
cactus = Obstacle("res/cactus.png")
cactus.setxy(350, 450)


obstacle_list.add(fire)
obstacle_list.add(garbage)
obstacle_list.add(cactus)

def draw_start_menu():

    # Draw the menu background image
    menu_bg_image = pygame.image.load("res/animalRescueBackground.png")
    window.blit(menu_bg_image, (0, 0))

    # load start button image, display button
    start_button_image = pygame.image.load("res/startButton.png")
    window.blit(start_button_image, start_button_rect)

    # load how to play button image, display button
    # HTP: How To Play
    htp_button_image = pygame.image.load("res/howToPlayButton.png")
    window.blit(htp_button_image, htp_button_rect)

    # load quit button image, display button
    quit_button_image = pygame.image.load("res/quitButton.png")
    window.blit(quit_button_image, quit_button_rect)

def draw_level_failed_menu():
    # Draw the menu background image
    menu_bg_image = pygame.image.load("res/levelFailedBackground.png")
    window.blit(menu_bg_image, (0, 0))

    restart_button_image = pygame.image.load("res/restartButton.png")
    restart_button_rect.x = WINDOW_WIDTH/2 - 300
    restart_button_rect.y = WINDOW_HEIGHT/2 + 250
    window.blit(restart_button_image, restart_button_rect)

    quit_button_rect.x = WINDOW_WIDTH/2 + 100
    quit_button_rect.y = WINDOW_HEIGHT/2 + 250
    quit_button_image = pygame.image.load("res/quitButton.png")
    window.blit(quit_button_image, quit_button_rect)

def draw_level_passed_menu():
    # Draw the menu background image
    menu_bg_image = pygame.image.load("res/levelPassedBackground.png")
    window.blit(menu_bg_image, (0, 0))

    next_level_button_image = pygame.image.load("res/nextLevelButton.png")
    window.blit(next_level_button_image, next_level_button_rect)

    restart_button_image = pygame.image.load("res/restartButton.png")
    restart_button_rect.x = WINDOW_WIDTH/2 - 100
    restart_button_rect.y = WINDOW_HEIGHT/2 + 25
    window.blit(restart_button_image, restart_button_rect)

    quit_button_image = pygame.image.load("res/quitButton.png")
    quit_button_rect.x = WINDOW_HEIGHT/2 - 100
    quit_button_rect.y = WINDOW_HEIGHT/2 + 150
    window.blit(quit_button_image, quit_button_rect)

def restart_game():
    global game_over, rescuer_rect, rescuer_image, animals, obstacle_list, animal_counter
    animal_counter = 0
    rescuer_image = pygame.image.load("res/rescuer-right.png")
    game_over = False
    rescuer_rect.x = 50
    rescuer_rect.y = 50
    for animal in animals:
        animal.is_vanished = False
    obstacle_list.empty()
    
    fire = Obstacle("res/fire.png")
    fire.setxy(150, 250)
    garbage = Obstacle("res/garbage.png")
    garbage.setxy(250, 350)
    cactus = Obstacle("res/cactus.png")
    cactus.setxy(350, 450)
    obstacle_list.add(fire)
    obstacle_list.add(garbage)
    obstacle_list.add(cactus)

    x = 150
    y = 150
    for i in range(14):
        fire = Obstacle("res/fire.png")
        fire.setxy(x, y)
        obstacle_list.add(fire)
        x+=40

def level_not_passed_yet():
    animal_counter_rect = pygame.Rect(WINDOW_WIDTH/2 - 250, WINDOW_HEIGHT/2, 100, 50)
    animal_counter_font = pygame.font.SysFont('Arial', 25)
    animal_counter_text = animal_counter_font.render("Collect at least " + str(required_number_of_animals) + " animals in order to pass the level.", True, (255, 255, 255))
    window.blit(animal_counter_text, animal_counter_rect)
    
def show_message(message, game_status):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    window.blit(text, text_rect)

    if game_status == "failed":
        # Draw restart button
        restart_button_rect = pygame.draw.rect(window, (255, 0, 0), (WINDOW_WIDTH/2 - 50, WINDOW_HEIGHT/2 + 35, 100, 50))
        restart_button_font = pygame.font.Font(None, 40)
        restart_button_text = restart_button_font.render("Restart", True, (255, 255, 255))
        window.blit(restart_button_text, restart_rect)
    elif game_status == "passed":
        animal_counter_rect = pygame.Rect(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 35, 100, 50)
        animal_counter_font = pygame.font.Font(None, 30)
        animal_counter_text = animal_counter_font.render("Animals collected: " + str(animal_counter), True, (255, 255, 255))
        window.blit(animal_counter_text, animal_counter_rect)
    elif game_status == "not passed":
        animal_counter_rect = pygame.Rect(WINDOW_WIDTH/2 - 110, WINDOW_HEIGHT/2 + 35, 100, 50)
        animal_counter_font = pygame.font.SysFont('Arial', 25)
        animal_counter_text = animal_counter_font.render("Collect at least " + str(required_number_of_animals) + " animals.", True, (255, 255, 255))
        window.blit(animal_counter_text, animal_counter_rect)

    pygame.display.update()

def draw_animal_counter(window):
    font = pygame.font.SysFont('Arial', 20)
    counter_text = font.render("Animals Collected: " + str(animal_counter), True, (0, 0, 0))
    counter_rect = counter_text.get_rect()
    counter_rect.topright = (WINDOW_WIDTH - 10, 40)
    window.blit(counter_text, counter_rect)
def draw_required_animals(window):
    font = pygame.font.SysFont('Arial', 20)
    counter_text = font.render("Animals Required : " + str(required_number_of_animals), True, (0, 0, 0))
    counter_rect = counter_text.get_rect()
    counter_rect.topright = (WINDOW_WIDTH - 10, 10)
    window.blit(counter_text, counter_rect)

# Set the speed of the rescuer
rescuer_speed = 1

MOVE_LEFT = pygame.K_LEFT
MOVE_RIGHT = pygame.K_RIGHT
MOVE_UP = pygame.K_UP
MOVE_DOWN = pygame.K_DOWN
def menu_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    game_loop()
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif restart_button_rect.collidepoint(mouse_pos):
                    restart_game()
                    game_loop()

        pygame.display.update()

def game_loop():
    global game_over, rescuer_rect, rescuer_image, animals, obstacle_list, animal_counter
    # Main game loop
    while True:
        # Check for events
        for event in pygame.event.get():
            # Check if the user closed the window
            if event.type == pygame.QUIT:
                # Quit Pygame and exit the program
                pygame.quit()
                exit()

        # Get the state of the arrow keys
        keys = pygame.key.get_pressed()

        # Move the rescuer based on the arrow key state
        if keys[MOVE_LEFT]:
            rescuer_image = pygame.image.load("res/rescuer-left.png")
            rescuer_rect.move_ip(-rescuer_speed, 0)
        if keys[MOVE_RIGHT]:
            rescuer_image = pygame.image.load("res/rescuer-right.png")
            rescuer_rect.move_ip(rescuer_speed, 0)
        if keys[MOVE_UP]:
            # rescuer_image = pygame.image.load("res/rescuer_up.png")
            rescuer_rect.move_ip(0, -rescuer_speed)
        if keys[MOVE_DOWN]:
            # rescuer_image = pygame.image.load("res/rescuer_down.png")
            rescuer_rect.move_ip(0, rescuer_speed)

        # Keep the rescuer within the window
        if rescuer_rect.left < 0:
            rescuer_rect.left = 0
        if rescuer_rect.right > WINDOW_WIDTH:
            rescuer_rect.right = WINDOW_WIDTH
        if rescuer_rect.top < 0:
            rescuer_rect.top = 0
        if rescuer_rect.bottom > WINDOW_HEIGHT:
            rescuer_rect.bottom = WINDOW_HEIGHT

        # Check for collisions between the rescuer and animals
        for animal in animals:
            if not animal.is_vanished and rescuer_rect.colliderect(animal.rect):
                animal.vanish()
                animal_counter = animal_counter + 1

        # Clear the screen with the forest green color
        window.fill(FOREST_GREEN)

        # Draw the animals
        for animal in animals:
            animal.draw(window)
            
        # Draw the rescuer, sanctuary image
        window.blit(rescuer_image, rescuer_rect)
        window.blit(animal_sanctuary_image, animal_sanctuary_rect)
        window.blit(vet_sign_image, vet_sign_rect)

        draw_required_animals(window)
        draw_animal_counter(window)

        obstacle_list.draw(window)

        for obstacle in obstacle_list:
                if rescuer_rect.colliderect(obstacle.rect):
                    rescuer_image = rescuer_damaged_image

                    # Show the game over message and restart button
                    # show_message("Game Over", "failed")
                    draw_level_failed_menu()

                    # Check if the restart button is clicked
                    if pygame.mouse.get_pressed()[0] and restart_rect.collidepoint(pygame.mouse.get_pos()):
                        restart_game()
                        animal_counter = 0

                    if pygame.mouse.get_pressed()[0] and restart_rect.collidepoint(pygame.mouse.get_pos()):
                        restart_game()
                        animal_counter = 0

        if rescuer_rect.colliderect(animal_sanctuary_rect):
            if animal_counter >= required_number_of_animals:
                level_passed = True
                draw_level_passed_menu()
            elif animal_counter <= required_number_of_animals:
                level_not_passed_yet()
        pygame.display.update()

draw_start_menu()
menu_loop()