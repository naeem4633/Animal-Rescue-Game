import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Define the window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# timer used to spawn fire
fire_timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(fire_timer_event, 500)

# Set window title
pygame.display.set_caption("Animal Rescue Game")

# Define the forest green color
FOREST_GREEN = (34, 139, 34)


# Load the rescuer image
rescuer_image = pygame.image.load("res/rescuer-right.png")
rescuer_image_right = pygame.image.load("res/rescuer-right.png")
rescuer_image_left = pygame.image.load("res/rescuer-left.png")
rescuer_rect = rescuer_image.get_rect()
rescuer_damaged_image_right = pygame.image.load("res/rescuer-damaged-right.png")
rescuer_damaged_image_left = pygame.image.load("res/rescuer-damaged-left.png")

animal_sanctuary_image = pygame.image.load("res/animalSanctuary.png")
animal_sanctuary_rect = animal_sanctuary_image.get_rect()
animal_sanctuary_rect.x = WINDOW_WIDTH - 128
animal_sanctuary_rect.y = WINDOW_HEIGHT - 128

vet_sign_image = pygame.image.load("res/veterinary.png")
vet_sign_rect = vet_sign_image.get_rect()
vet_sign_rect.x = WINDOW_WIDTH - 150
vet_sign_rect.y = WINDOW_HEIGHT - 96

# Counter functionaity
animal_counter = 0
required_number_of_animals = 2

# Button positions
start_button_rect = pygame.Rect((WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 - 50, 200, 100))
htp_button_rect = pygame.Rect((WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 75, 200, 100))
quit_button_rect = pygame.Rect((WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 200, 200, 100))
restart_button_rect = pygame.Rect((WINDOW_WIDTH/2 - 300, WINDOW_HEIGHT/2 + 250, 200, 100))
next_level_button_rect = pygame.Rect((WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 - 100, 200, 100))

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

    def getx(self):
        return self.rect.x
    def gety(self):
        return self.rect.y

# Load the animal images and create animal objects
fox_image_path = "res/fox.png"
chameleon_image_path = "res/chameleon.png"
koala_image_path = "res/koala.png"
animals = [
    Animal(fox_image_path, 600, 100),
    Animal(chameleon_image_path, 100, 600),
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
garbage.setxy(200, 0)
garbage2 = Obstacle("res/garbage.png")
garbage2.setxy(20, 550)
cactus = Obstacle("res/cactus.png")
cactus.setxy(350, 450)
cactus2 = Obstacle("res/cactus.png")
cactus2.setxy(550, 350)

obstacle_list.add(fire, garbage, garbage2, cactus, cactus2)

def spawn_fire_randomly():
    global rescuer_rect, animals
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
        fire = Obstacle("res/fire.png")
        fire.setxy(x, y)
        obstacle_list.add(fire)

def draw_start_menu():
    # Draw the start menu background image
    menu_bg_image = pygame.image.load("res/animalRescueBackground.png")
    window.blit(menu_bg_image, (0, 0))

    # load and display start button image(rect defined in the global variable space)
    start_button_image = pygame.image.load("res/startButton.png")
    window.blit(start_button_image, start_button_rect)

    # load and display htp button image(rect defined in the global variable space)
    # HTP: How To Play
    htp_button_image = pygame.image.load("res/howToPlayButton.png")
    window.blit(htp_button_image, htp_button_rect)

    # load and display quit button image(rect defined in the global variable space)
    quit_button_image = pygame.image.load("res/quitButton.png")
    window.blit(quit_button_image, quit_button_rect)

def draw_level_failed_menu():
    # Draw the level failed menu background image
    menu_bg_image = pygame.image.load("res/levelFailedBackground.png")
    window.blit(menu_bg_image, (0, 0))

    # load and display restart button image(rect defined in the global variable space)
    restart_button_image = pygame.image.load("res/restartButton.png")
    restart_button_rect.x = WINDOW_WIDTH/2 - 300
    restart_button_rect.y = WINDOW_HEIGHT/2 + 250
    window.blit(restart_button_image, restart_button_rect)

    # load and display restart button image(rect defined in the global variable space)
    quit_button_rect.x = WINDOW_WIDTH/2 + 100
    quit_button_rect.y = WINDOW_HEIGHT/2 + 250
    quit_button_image = pygame.image.load("res/quitButton.png")
    window.blit(quit_button_image, quit_button_rect)

def draw_how_to_play_menu():
    # Draw the level failed menu background image
    menu_bg_image = pygame.image.load("res/htpMenuBackground.png")
    window.blit(menu_bg_image, (0, 0))

    # load and display start button image(rect defined in the global variable space)
    start_button_rect.x = WINDOW_WIDTH/2 - 100
    start_button_rect.y = WINDOW_HEIGHT/2 + 280    
    start_button_image = pygame.image.load("res/startButton.png")
    window.blit(start_button_image, start_button_rect)

def draw_level_passed_menu():
    # Draw the level passed menu background image
    menu_bg_image = pygame.image.load("res/levelPassedBackground.png")
    window.blit(menu_bg_image, (0, 0))

    # load and display next level button image(rect defined in the global variable space)
    next_level_button_image = pygame.image.load("res/nextLevelButton.png")
    window.blit(next_level_button_image, next_level_button_rect)

    # load and display restart button image(rect defined in the global variable space)
    restart_button_image = pygame.image.load("res/restartButton.png")
    restart_button_rect.x = WINDOW_WIDTH/2 - 100
    restart_button_rect.y = WINDOW_HEIGHT/2 + 25
    window.blit(restart_button_image, restart_button_rect)

    # load and display quit button image(rect defined in the global variable space)
    quit_button_image = pygame.image.load("res/quitButton.png")
    quit_button_rect.x = WINDOW_HEIGHT/2 - 100
    quit_button_rect.y = WINDOW_HEIGHT/2 + 150
    window.blit(quit_button_image, quit_button_rect)

def too_much_fire():
    # Draw the level passed menu background image
    menu_bg_image = pygame.image.load("res/tooMuchFireBackground.png")
    window.blit(menu_bg_image, (0, 0))

    # load and display restart button image(rect defined in the global variable space)
    restart_button_image = pygame.image.load("res/restartButton.png")
    restart_button_rect.x = WINDOW_WIDTH/2 - 300
    restart_button_rect.y = WINDOW_HEIGHT/2 + 250
    window.blit(restart_button_image, restart_button_rect)

    # load and display restart button image(rect defined in the global variable space)
    quit_button_rect.x = WINDOW_WIDTH/2 + 100
    quit_button_rect.y = WINDOW_HEIGHT/2 + 250
    quit_button_image = pygame.image.load("res/quitButton.png")
    window.blit(quit_button_image, quit_button_rect)

def restart_game():
    # Get the global values of these variables, reset animal counter, reset rescuer position
    global rescuer_rect, rescuer_image, animals, obstacle_list, animal_counter
    animal_counter = 0
    rescuer_image = pygame.image.load("res/rescuer-right.png")
    rescuer_rect.x = 50
    rescuer_rect.y = 50

    # reset obstacles, animals
    for animal in animals:
        animal.is_vanished = False
    obstacle_list.empty()
    
    fire = Obstacle("res/fire.png")
    fire.setxy(150, 250)
    garbage = Obstacle("res/garbage.png")
    garbage.setxy(200, 50)
    garbage2 = Obstacle("res/garbage.png")
    garbage2.setxy(20, 550)
    cactus = Obstacle("res/cactus.png")
    cactus.setxy(350, 450)
    cactus2 = Obstacle("res/cactus.png")
    cactus2.setxy(550, 350)

    obstacle_list.add(fire, garbage, garbage2, cactus, cactus2)

# Appears when player goes to the animal shelter without collecting the minimum number of animals
def draw_level_not_passed_yet():
    animal_counter_rect = pygame.Rect(WINDOW_WIDTH/2 - 250, WINDOW_HEIGHT/2, 100, 50)
    animal_counter_font = pygame.font.SysFont('Arial', 25)
    animal_counter_text = animal_counter_font.render("Collect at least " + str(required_number_of_animals) + " animals in order to pass the level.", True, (255, 255, 255))
    window.blit(animal_counter_text, animal_counter_rect)

def draw_animal_counter(window):
    font = pygame.font.SysFont('Arial', 20)
    counter_text = font.render("Animals Collected: " + str(animal_counter), True, (0, 0, 0))
    counter_rect = counter_text.get_rect()
    counter_rect.topright = (WINDOW_WIDTH - 10, 130)
    window.blit(counter_text, counter_rect)
def draw_required_animals(window):
    font = pygame.font.SysFont('Arial', 20)
    counter_text = font.render("Animals Required : " + str(required_number_of_animals), True, (0, 0, 0))
    counter_rect = counter_text.get_rect()
    counter_rect.topright = (WINDOW_WIDTH - 10, 100)
    window.blit(counter_text, counter_rect)

# Set the speed of the rescuer
rescuer_speed = 5

MOVE_LEFT = pygame.K_LEFT
MOVE_RIGHT = pygame.K_RIGHT
MOVE_UP = pygame.K_UP
MOVE_DOWN = pygame.K_DOWN

# Called when displaying any kind of menus
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
                elif htp_button_rect.collidepoint(mouse_pos):
                    draw_how_to_play_menu()
                    menu_loop()
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif restart_button_rect.collidepoint(mouse_pos):
                    restart_game()
                    game_loop()

        pygame.display.update()

def game_loop():
    global rescuer_rect, rescuer_image, animals, obstacle_list, animal_counter
    # Main game loop
    while True:
        # Check for events
        for event in pygame.event.get():
            # Check if the user closed the window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == fire_timer_event:
                spawn_fire_randomly()

        # Get the state of the arrow keys
        keys = pygame.key.get_pressed()

        # Move the rescuer based on the arrow key state
        if keys[MOVE_LEFT]:
            rescuer_image = rescuer_image_left
            rescuer_rect.move_ip(-rescuer_speed, 0)
        if keys[MOVE_RIGHT]:
            rescuer_image = rescuer_image_right
            rescuer_rect.move_ip(rescuer_speed, 0)
        if keys[MOVE_UP]:
            rescuer_rect.move_ip(0, -rescuer_speed)
        if keys[MOVE_DOWN]:
            rescuer_rect.move_ip(0, rescuer_speed)

        # Get the position of the mouse cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Check if the left mouse button is pressed
        if pygame.mouse.get_pressed()[0]:
            # Calculate the distance between the player and the mouse cursor
            dist_x = mouse_x - rescuer_rect.centerx
            dist_y = mouse_y - rescuer_rect.centery

            # Move the player in the direction of the mouse cursor
            if abs(dist_x) > abs(dist_y):
                if dist_x > 0:
                    rescuer_image = rescuer_image_right
                    rescuer_rect.move_ip(rescuer_speed, 0)
                else:
                    rescuer_image = rescuer_image_left
                    rescuer_rect.move_ip(-rescuer_speed, 0)
            else:
                if dist_y > 0:
                    rescuer_rect.move_ip(0, rescuer_speed)
                else:
                    rescuer_rect.move_ip(0, -rescuer_speed)

        # Keep the rescuer within screenbounds
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

        # set background
        menu_bg_image = pygame.image.load("res/gameBackground.png")
        window.blit(menu_bg_image, (0, 0))

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
                    if rescuer_image == rescuer_image_right:
                        rescuer_image = rescuer_damaged_image_right
                    else:
                        rescuer_image = rescuer_damaged_image_left
                    window.blit(rescuer_image, rescuer_rect)
                    pygame.display.update()
                    pygame.time.delay(500)
                    draw_level_failed_menu()
                    menu_loop()

        if rescuer_rect.colliderect(animal_sanctuary_rect):
            if animal_counter >= required_number_of_animals:
                time.sleep(0.2)
                draw_level_passed_menu()
                menu_loop()
            elif animal_counter <= required_number_of_animals:
                draw_level_not_passed_yet()

        if(len(obstacle_list) > 150):
            too_much_fire()
            menu_loop()

        # Update the window
        pygame.display.update()
        clock.tick(60)

draw_start_menu()
menu_loop()