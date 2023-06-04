import pygame
import random
import math
from player import Player
from bullet import Bullet
from enemy import Enemy

# Initialization
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dodge Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Player settings
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height // 2 - player_height // 2
player_speed = 3
player = Player(player_x, player_y, player_width, player_height, player_speed)

# Bullet settings
bullet_radius = 5
bullet_speed = 10
bullet_cooldown = 10  # Number of frames between each bullet when shooting automatically
bullets = []

# Enemy settings
enemy_width = 20
enemy_height = 20
num_enemies = 5
enemies = []
average_speed = 1

for _ in range(num_enemies):
    enemy = Enemy.generate_random_enemy(screen_width, screen_height, enemy_width, enemy_height, average_speed)
    enemies.append(enemy)

# Game status
game_over = False

# Clock settings
clock = pygame.time.Clock()
FPS = 60

# Helper function to calculate distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Function to reset the game
def reset_game():
    global player, enemies, bullets, game_over

    player = Player(player_x, player_y, player_width, player_height, player_speed)

    enemies = []
    bullets = []
    for _ in range(num_enemies):
        enemy = Enemy.generate_random_enemy(screen_width, screen_height, enemy_width, enemy_height, average_speed)
        enemies.append(enemy)

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Player shooting
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if len(bullets) < 1:  # Limit the number of bullets shot automatically
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullet_x = player.x + player.width // 2
            bullet_y = player.y + player.height // 2
            direction_x = mouse_x - bullet_x
            direction_y = mouse_y - bullet_y
            distance = calculate_distance(mouse_x, mouse_y, bullet_x, bullet_y)

            if distance != 0:
                direction_x /= distance
                direction_y /= distance

            bullet_direction = (direction_x, direction_y)
            bullet = Bullet(bullet_x, bullet_y, bullet_radius, bullet_speed, bullet_direction)
            bullets.append(bullet)

    # Player movement
    player.move(keys, screen_width, screen_height)

    # Bullet movement
    for bullet in bullets:
        bullet.move()

    # Enemy movement
    for enemy in enemies:
        enemy.move_towards_player(player.x + player.width // 2, player.y + player.height // 2)

        # Collision detection with enemies
        if player.x < enemy.x + enemy.width and player.x + player.width > enemy.x and player.y < enemy.y + enemy.height and player.y + player.height > enemy.y:
            reset_game()

        # Collision detection with bullets
        for bullet in bullets:
            if bullet.x < enemy.x + enemy.width and bullet.x + bullet.radius > enemy.x and bullet.y < enemy.y + enemy.height and bullet.y + bullet.radius > enemy.y:
                enemies.remove(enemy)
                bullets.remove(bullet)
                break

    # Screen drawing
    screen.fill(black)
    player.draw(screen, white)
    for enemy in enemies:
        enemy.draw(screen, white)
    for bullet in bullets:
        bullet.draw(screen, white)
    pygame.display.update()

    # FPS control
    clock.tick(FPS)

# Quit the game
pygame.quit()
