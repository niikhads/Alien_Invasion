import pygame
import sys
import random

# Pygame-in başlanğıcı
pygame.init()

# Ekran ölçüləri
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alien Invasion")

# Rənglər
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Şrift
font = pygame.font.SysFont(None, 36)

# Mətn yaratma funksiyası
def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Kosmik gəmi class
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

# Meteorlar class
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

# Mərmilər class (Həm meteorlardan, həm də gəmidən atılan mərmilər üçün)
class Bullet:
    def __init__(self, x, y):
        self.image = pygame.image.load("bullet.jpeg")  # bullet.png şəklini istifadə edirik
        # Mərminin ölçüsünü kiçiltmək
        self.image = pygame.transform.scale(self.image, (30, 30))  # Bu ölçüləri tənzimləyin
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7

    def move(self):
        self.rect.y -= self.speed  # Mərmi yuxarıya hərəkət edir

    def draw(self):
        screen.blit(self.image, self.rect)

# Güc artırıcıları class
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

# Oyun parametrləri
spaceship = Spaceship()
meteors = []
bullets = []
power_ups = []  # Güc artırıcıları üçün siyahı
score = 0
lives = 3
meteor_speed = 2

# Meteor əlavə etmə funksiyası
def add_meteor():
    if random.randint(1, 20) == 1:
        meteor = Meteor(meteor_speed)
        meteors.append(meteor)

# Güc artırıcıları əlavə etmək funksiyası
def add_power_up():
    if random.randint(1, 200) <= 5:  # Güc artırıcıların 200-də bir ehtimalla ekrana düşməsi
        power_type = random.choice(["life", "speed", "ammo"])  # Həyat, sürət və ya ammo
        x = random.randint(20, SCREEN_WIDTH - 20)
        power_ups.append(PowerUp(x, -20, power_type))

# Səviyyə seçimi
levels = {"Easy": 2, "Normal": 4, "Difficult": 6}
level_selected = False

# Musiqi çalınması
pygame.mixer.music.load("background_music.mp3")  # Musiqi faylını yükləyin
pygame.mixer.music.play(-1)  # Sonsuz dövrədə musiqi çalsın

while not level_selected:
    screen.fill(BLACK)
    draw_text("Səviyyəni seçin: Easy (E), Normal (N), Difficult (D)", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 20)
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

# Oyun döngüsü
running = True
while running:
    screen.fill(BLACK)

    # Hadisələrin yoxlanması
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Gəmini atış etdirmək
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Mərmi atmaq üçün Space düyməsi
                bullet = Bullet(spaceship.rect.centerx, spaceship.rect.top)
                bullets.append(bullet)

    # Klaviatura ilə hərəkət
    keys = pygame.key.get_pressed()
    spaceship.move(keys)

    # Meteorları əlavə et və hərəkət etdir
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

    # Güc artırıcıları əlavə et və hərəkət etdir
    add_power_up()
    for power_up in power_ups[:]:
        power_up.move()
        if power_up.rect.colliderect(spaceship.rect):
            power_ups.remove(power_up)
            if power_up.type == "life":
                lives += 1  # Həyat artırılır
            elif power_up.type == "speed":
                spaceship.speed += 1  # Gəminin sürəti artırılır
            elif power_up.type == "ammo":
                pass  # Əlavə mərmi ehtiyatı təmin edilə bilər

        if power_up.rect.top > SCREEN_HEIGHT:  # Ekranı tərk edən güc artırıcıları
            power_ups.remove(power_up)

    # Mərmilərdən və meteorlardan atəşləri yoxla
    for bullet in bullets[:]:
        bullet.move()
        for meteor in meteors[:]:
            if bullet.rect.colliderect(meteor.rect):
                meteors.remove(meteor)
                bullets.remove(bullet)
                score += 1  # Hər vurulan meteor üçün xal
                break

        if bullet.rect.bottom < 0:  # Ekranı tərk edən mərmilər
            bullets.remove(bullet)

    # Gəmi və meteorların çəkilməsi
    spaceship.draw()
    for meteor in meteors:
        meteor.draw()

    # Mərmilərin çəkilməsi
    for bullet in bullets:
        bullet.draw()

    # Güc artırıcılarının çəkilməsi
    for power_up in power_ups:
        power_up.draw()

    # Skor və həyatlar
    draw_text(f"Skor: {score}", 10, 10)
    draw_text(f"Həyat: {lives}", 10, 50)

    # Ekranı yeniləmə
    pygame.display.flip()
    clock.tick(FPS)

# Oyun bitdikdə restart seçimi
while True:
    screen.fill(BLACK)
    draw_text("Oyun Bitdi!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 40)
    draw_text(f"Yekun Skor: {score}", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
    draw_text("Yenidən başlamaq üçün R basın", SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 40)
    draw_text("Çıxmaq üçün Q basın", SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 80)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                spaceship = Spaceship()
                meteors = []
                bullets = []
                power_ups = []
                score = 0
                lives = 3
                running = True
                pygame.mixer.music.play(-1)  # Musiqi təkrarlanır
                break
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    if running:
        break
