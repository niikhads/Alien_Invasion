import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alien Invasion")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont(None, 36)

def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

class Spaceship:
    def __init__(self):
        self.image = pygame.image.load("spaceship3.jpeg")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

class Meteor:
    def __init__(self, speed):
        self.image = pygame.image.load("meteor.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 20), -20))
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

class StrongMeteor:
    def __init__(self, speed):
        self.image = pygame.image.load("large_meteor.jpeg")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 20), -20))
        self.speed = speed
        self.hp = 3

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

class EnemySpaceship:
    def __init__(self, speed):
        self.image = pygame.image.load("spaceship_enemy.jpeg")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 20), -20))
        self.speed = speed
        self.hp = 2

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y):
        self.image = pygame.image.load("bullet.jpeg")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7

    def move(self):
        self.rect.y -= self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

class PowerUp:
    def __init__(self, x, y, power_type):
        self.image = None
        self.type = power_type
        if self.type == "life":
            self.image = pygame.image.load("life_powerup.jpeg")
        elif self.type == "speed":
            self.image = pygame.image.load("speed_powerup.jpeg")
        elif self.type == "ammo":
            self.image = pygame.image.load("ammo_powerup.png")
        
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

spaceship = Spaceship()
meteors = []
strong_meteors = []  
enemy_spaceships = [] 
bullets = []
power_ups = []  
score = 0
lives = 3
meteor_speed = 2
last_special_enemy_time = pygame.time.get_ticks()  
special_enemy_interval = 10000  

def add_meteor():
    if random.randint(1, 20) == 1:
        meteor = Meteor(meteor_speed)
        meteors.append(meteor)

def add_strong_meteor():
    if random.randint(1, 100) == 1:  
        meteor = StrongMeteor(meteor_speed + 2)  
        strong_meteors.append(meteor)

def add_enemy_spaceship():
    global last_special_enemy_time
    if pygame.time.get_ticks() - last_special_enemy_time >= special_enemy_interval:
        enemy = EnemySpaceship(4)  
        enemy_spaceships.append(enemy)
        last_special_enemy_time = pygame.time.get_ticks()  

def add_power_up():
    if random.randint(1, 1000) <= 5:  
        power_type = random.choice(["life", "speed", "ammo"])  
        x = random.randint(20, SCREEN_WIDTH - 20)
        power_ups.append(PowerUp(x, -20, power_type))

levels = {"Easy": 2, "Normal": 4, "Difficult": 6}
level_selected = False

pygame.mixer.music.load("background_music.mp3")  
pygame.mixer.music.play(-1)  

while not level_selected:
    screen.fill(BLACK)
    draw_text("Seviyyeni seçin: Easy (E), Normal (N), Difficult (D)", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 20)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                meteor_speed = levels["Easy"]
                level_selected = True
            elif event.key == pygame.K_n:
                meteor_speed = levels["Normal"]
                level_selected = True
            elif event.key == pygame.K_d:
                meteor_speed = levels["Difficult"]
                level_selected = True

def restart_game():
    global spaceship, meteors, strong_meteors, enemy_spaceships, bullets, power_ups, score, lives, meteor_speed
    spaceship = Spaceship()
    meteors.clear()
    strong_meteors.clear()
    enemy_spaceships.clear()
    bullets.clear()
    power_ups.clear()
    score = 0
    lives = 3
    meteor_speed = 2

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  
                bullet = Bullet(spaceship.rect.centerx, spaceship.rect.top)
                bullets.append(bullet)

            if event.key == pygame.K_r:  # Restart game when R is pressed
                restart_game()

    keys = pygame.key.get_pressed()
    spaceship.move(keys)

    add_meteor()
    for meteor in meteors[:]:
        meteor.move()
        if meteor.rect.colliderect(spaceship.rect):
            meteors.remove(meteor)
            lives -= 1
            if lives == 0:
                running = False
        elif meteor.rect.top > SCREEN_HEIGHT:
            meteors.remove(meteor)
            score += 1

    add_strong_meteor()
    for strong_meteor in strong_meteors[:]:
        strong_meteor.move()
        if strong_meteor.rect.colliderect(spaceship.rect):
            strong_meteors.remove(strong_meteor)
            lives -= 1
            if lives == 0:
                running = False
        elif strong_meteor.rect.top > SCREEN_HEIGHT:
            strong_meteors.remove(strong_meteor)

    add_enemy_spaceship()
    for enemy_spaceship in enemy_spaceships[:]:
        enemy_spaceship.move()
        if enemy_spaceship.rect.colliderect(spaceship.rect):
            enemy_spaceships.remove(enemy_spaceship)
            lives -= 1
            if lives == 0:
                running = False
        elif enemy_spaceship.rect.top > SCREEN_HEIGHT:
            enemy_spaceships.remove(enemy_spaceship)

    add_power_up()
    for power_up in power_ups[:]:
        power_up.move()
        if power_up.rect.colliderect(spaceship.rect):
            power_ups.remove(power_up)
            if power_up.type == "life":
                lives += 1
            elif power_up.type == "speed":
                spaceship.speed += 1
            elif power_up.type == "ammo":
                pass

        if power_up.rect.top > SCREEN_HEIGHT:
            power_ups.remove(power_up)

    for bullet in bullets[:]:
        bullet.move()
        for meteor in meteors[:]:
            if bullet.rect.colliderect(meteor.rect):
                meteors.remove(meteor)
                bullets.remove(bullet)
                score += 1
                break
        for strong_meteor in strong_meteors[:]:
            if bullet.rect.colliderect(strong_meteor.rect):
                strong_meteors.remove(strong_meteor)
                bullets.remove(bullet)
                score += 3
                break
        for enemy_spaceship in enemy_spaceships[:]:
            if bullet.rect.colliderect(enemy_spaceship.rect):
                enemy_spaceships.remove(enemy_spaceship)
                bullets.remove(bullet)
                score += 5
                break

        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    spaceship.draw()
    for meteor in meteors:
        meteor.draw()
    for strong_meteor in strong_meteors:
        strong_meteor.draw()
    for enemy_spaceship in enemy_spaceships:
        enemy_spaceship.draw()

    for bullet in bullets:
        bullet.draw()

    for power_up in power_ups:
        power_up.draw()

    draw_text(f"Skor: {score}", 10, 10)
    draw_text(f"Live: {lives}", 10, 50)

    if lives == 0:
        draw_text("Game Over!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30)
        draw_text(f"Final Skor: {score}", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 10)
        draw_text("Press 'R' to Restart", SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 50)
        pygame.display.flip()

        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart game when R is pressed
                        restart_game()
                        waiting_for_restart = False
            clock.tick(FPS)

    pygame.display.flip()
    clock.tick(FPS)
