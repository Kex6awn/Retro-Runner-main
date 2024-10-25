import pygame
import os
import random

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
try:
    RUNNING = [pygame.image.load(os.path.join("./marioMoving2", "marioMoving1.gif")),
               pygame.image.load(os.path.join("./marioMoving2", "marioMoving2.gif")),
               pygame.image.load(os.path.join("./marioMoving2", "marioMoving3.gif"))]
    JUMPING = pygame.image.load(os.path.join("./marioJumping2", "marioJumping.png"))
    CROUCHING = pygame.image.load(os.path.join("./MarioCrouching2", "marioCrouching.png"))

    # Load the background and scale it to fit the screen
    BG = pygame.image.load(os.path.join("./Background", "background.jpg"))
    BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
    BG_WIDTH = BG.get_width()

    # Scaling factor for Mario
    SCALE_FACTOR_MARIO = 1.75

    # Scale Mario images
    RUNNING = [pygame.transform.scale(img, (int(img.get_width() * SCALE_FACTOR_MARIO), int(img.get_height() * SCALE_FACTOR_MARIO))) for img in RUNNING]
    JUMPING = pygame.transform.scale(JUMPING, (int(JUMPING.get_width() * SCALE_FACTOR_MARIO), int(JUMPING.get_height() * SCALE_FACTOR_MARIO)))
    CROUCHING = pygame.transform.scale(CROUCHING, (int(CROUCHING.get_width() * SCALE_FACTOR_MARIO), int(CROUCHING.get_height() * SCALE_FACTOR_MARIO)))

    # Load obstacle images
    GOOMBA = [pygame.image.load(os.path.join("./Goomba", "frame_0_delay-0.15s.gif")),
              pygame.image.load(os.path.join("./Goomba", "frame_1_delay-0.15s.gif"))]
    KOOPA = [pygame.image.load(os.path.join("./Koopa", "frame_0_delay-0.2s.gif")),
             pygame.image.load(os.path.join("./Koopa", "frame_1_delay-0.2s.gif"))]
    PLANT = [pygame.image.load(os.path.join("./Plant", "frame_0_delay-0.2s.gif")),
             pygame.image.load(os.path.join("./Plant", "frame_1_delay-0.2s.gif"))]
    BULLETBILL = [pygame.image.load(os.path.join("./BulletBill", "BulletBill.png")),
                  pygame.image.load(os.path.join("./BulletBill", "BulletBill.png"))]

except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

# CLASSES
class Mario:
    X_POS = 80
    Y_POS = 370
    Y_POS_DUCK = 400
    JUMP_VEL = 7.5

    def __init__(self):
        self.jump_img = JUMPING
        self.run_img = RUNNING
        self.duck_img = CROUCHING

        self.mario_duck = False
        self.mario_run = True
        self.mario_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.mario_rect = self.image.get_rect()
        self.mario_rect.x = self.X_POS
        self.mario_rect.y = self.Y_POS

    def update(self, userInput):
        if self.mario_run:
            self.run()
        if self.mario_jump:
            self.jump()
        if self.mario_duck:
            self.duck()

        if self.step_index >= 10:
            self.step_index = 0
        
        if userInput[pygame.K_UP] and not self.mario_jump:
            self.mario_run = False
            self.mario_jump = True
            self.mario_duck = False
        elif userInput[pygame.K_DOWN] and not self.mario_jump:
            self.mario_duck = True
            self.mario_run = False
            self.mario_jump = False
        elif not (self.mario_jump or userInput[pygame.K_DOWN]):
            self.mario_run = True
            self.mario_jump = False
            self.mario_duck = False
    
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.mario_rect = self.image.get_rect()
        self.mario_rect.x = self.X_POS
        self.mario_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.mario_jump:
            self.mario_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.mario_jump = False
            self.jump_vel = self.JUMP_VEL

    def duck(self):
        self.image = self.duck_img
        self.mario_rect = self.image.get_rect()
        self.mario_rect.x = self.X_POS
        self.mario_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.mario_rect.x, self.mario_rect.y))

class Obstacles:
    def __init__(self, image, type, scale_factor):
        self.image = [pygame.transform.scale(img, (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor))) for img in image]
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class Plant(Obstacles):
    def __init__(self, image, scale_factor=4):
        self.type = 0
        super().__init__(image, self.type, scale_factor)
        self.rect.y = 380
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class Koopa(Obstacles):
    def __init__(self, image, scale_factor=4):
        self.type = 0
        super().__init__(image, self.type, scale_factor)
        self.rect.y = 382
        self.index = 0
    
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class Goomba(Obstacles):
    def __init__(self, image, scale_factor=4):
        self.type = 0
        super().__init__(image, self.type, scale_factor)
        self.rect.y = 387
        self.index = 0
    
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class BulletBill(Obstacles):
    def __init__(self, image, scale_factor=4):
        self.type = 0
        super().__init__(image, self.type, scale_factor)
        self.rect.y = 330
        self.index = 0
    
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

# Load game
def main():
    global game_speed, x_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Mario()
    game_speed = 3
    x_pos_bg = 0
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, 0))  # Draw the background
        SCREEN.blit(BG, (image_width + x_pos_bg, 0))  # Draw a second copy for seamless scrolling
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed  # Move the background left to create scrolling effect

    jump_sfx = pygame.mixer.Sound("jump.mp3")
    death_sfx = pygame.mixer.Sound("death.mp3")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        userInput = pygame.key.get_pressed()

        if userInput[pygame.K_UP]:
            jump_sfx.play()
            

        background()  # Draw the background first
        player.draw(SCREEN)  # Then draw Mario on top of the background
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 3) == 0:
                obstacles.append(Plant(PLANT, scale_factor=2.0))  # Adjust scale_factor as needed
            elif random.randint(0, 3) == 1:
                obstacles.append(Koopa(KOOPA, scale_factor=2))  # Adjust scale_factor as needed
            elif random.randint(0, 3) == 2:
                obstacles.append(Goomba(GOOMBA, scale_factor=1.3))  # Adjust scale_factor as needed
            elif random.randint(0,3) == 3:
                obstacles.append(BulletBill(BULLETBILL)) # Adjust scale_factor as needed

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.mario_rect.colliderect(obstacle.rect):
                death_sfx.play()
                pygame.time.delay(100)
                death_count += 1
                menu(death_count)
            
        score()

        clock.tick(60)
        pygame.display.update()

# Start the game
def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()

menu(death_count=0)
