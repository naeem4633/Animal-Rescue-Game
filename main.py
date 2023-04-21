import pygame
import random

# Initialize Pygame
pygame.init()

# Define the window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the window title
pygame.display.set_caption("Animal Rescue Game")

# Define the forest green color
FOREST_GREEN = (34, 139, 34)

# Load the rescuer image
rescuer_image = pygame.image.load("res/rescuer-right.png")
rescuer_damaged_image = pygame.image.load("res/rescuer-damaged.png")
rescuer_rect = rescuer_image.get_rect()
game_over = False
# Define the restart button
restart_button = pygame.Rect(250, 400, 100, 50)  # x, y, width, height

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

fire = Obstacle("res/flame.png")
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
    fire = Obstacle("res/flame.png")
    fire.setxy(x, y)
    obstacle_list.add(fire)
    x+=40

def restart_game():
    global game_over, rescuer_rect, rescuer_image, animals, obstacle_list
    rescuer_image = pygame.image.load("res/rescuer-right.png")
    game_over = False
    rescuer_rect.x = 50
    rescuer_rect.y = 50
    for animal in animals:
        animal.is_vanished = False
    obstacle_list.empty()
    
    fire = Obstacle("res/flame.png")
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
        fire = Obstacle("res/flame.png")
        fire.setxy(x, y)
        obstacle_list.add(fire)
        x+=40
    
def show_message(message, show_restart_button=False):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    window.blit(text, text_rect)

    if show_restart_button:
        # Draw restart button
        restart_button_rect = pygame.draw.rect(window, (255, 0, 0), (WINDOW_WIDTH/2 - 50, WINDOW_HEIGHT/2 + 50, 100, 50))
        restart_button_font = pygame.font.Font(None, 40)
        restart_button_text = restart_button_font.render("Restart", True, (255, 255, 255))
        restart_button_text_rect = restart_button_text.get_rect(center=restart_button_rect.center)
        window.blit(restart_button_text, restart_button_text_rect)

    pygame.display.update()

# Set the speed of the rescuer
rescuer_speed = 1

# Define the keys for player controls
MOVE_LEFT = pygame.K_LEFT
MOVE_RIGHT = pygame.K_RIGHT
MOVE_UP = pygame.K_UP
MOVE_DOWN = pygame.K_DOWN

# Main game loop
while True:
    # Check for events
    for event in pygame.event.get():
        # Check if the user closed the window
        if event.type == pygame.QUIT:
            # Quit Pygame and exit the program
            pygame.quit()
            exit()
    
    # # Check if the game is over
    # if game_over:
        
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

    # Clear the screen with the forest green color
    window.fill(FOREST_GREEN)

    # Draw the animals
    for animal in animals:
        animal.draw(window)
        
    

    # Draw the rescuer image
    window.blit(rescuer_image, rescuer_rect)

    obstacle_list.draw(window)

    for obstacle in obstacle_list:
            if rescuer_rect.colliderect(obstacle.rect):
                rescuer_image = rescuer_damaged_image
                game_over = True
                
                # Show the game over message and restart button
                show_message("Game Over", True)

                # Check if the restart button is clicked
                if pygame.mouse.get_pressed()[0] and restart_button.collidepoint(pygame.mouse.get_pos()):
                    restart_game()

    # Update the window
    pygame.display.update()