import pygame
import random
import math

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

# Bullet settings
bullet_radius = 5
bullet_speed = 8
bullet_cooldown = 10  # Number of frames between each bullet when shooting automatically
bullets = []

# Enemy settings
enemy_width = 20
enemy_height = 20
num_enemies = 5
enemies = []
average_speed = 1

for _ in range(num_enemies):
    side = random.randint(1, 4)  # Determine which side the enemy spawns (1: top, 2: right, 3: bottom, 4: left)
    if side == 1:  # Top side
        enemy_x = random.randint(-enemy_width, screen_width - enemy_width)
        enemy_y = random.randint(-screen_height, -enemy_height)
    elif side == 2:  # Right side
        enemy_x = random.randint(screen_width, screen_width + enemy_width)
        enemy_y = random.randint(-enemy_height, screen_height - enemy_height)
    elif side == 3:  # Bottom side
        enemy_x = random.randint(-enemy_width, screen_width - enemy_width)
        enemy_y = random.randint(screen_height, screen_height + enemy_height)
    else:  # Left side
        enemy_x = random.randint(-screen_width, -enemy_width)
        enemy_y = random.randint(-enemy_height, screen_height - enemy_height)
    enemy_speed = random.uniform(average_speed - 0.5, average_speed + 0.5)
    enemies.append([enemy_x, enemy_y, enemy_speed])

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
    global player_x, player_y, enemies, bullets, game_over

    player_x = screen_width // 2 - player_width // 2
    player_y = screen_height // 2 - player_height // 2

    enemies = []
    bullets = []
    for _ in range(num_enemies):
        side = random.randint(1, 4)
        if side == 1:
            enemy_x = random.randint(-enemy_width, screen_width - enemy_width)
            enemy_y = random.randint(-screen_height, -enemy_height)
        elif side == 2:
            enemy_x = random.randint(screen_width, screen_width + enemy_width)
            enemy_y = random.randint(-enemy_height, screen_height - enemy_height)
        elif side == 3:
            enemy_x = random.randint(-enemy_width, screen_width - enemy_width)
            enemy_y = random.randint(screen_height, screen_height + enemy_height)
        else:
            enemy_x = random.randint(-screen_width, -enemy_width)
            enemy_y = random.randint(-enemy_height, screen_height - enemy_height)
        enemy_speed = random.uniform(average_speed - 0.5, average_speed + 0.5)
        enemies.append([enemy_x, enemy_y, enemy_speed])

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
            bullet_x = player_x + player_width // 2
            bullet_y = player_y + player_height // 2
            direction_x = mouse_x - bullet_x
            direction_y = mouse_y - bullet_y
            distance = calculate_distance(mouse_x, mouse_y, bullet_x, bullet_y)

            if distance != 0:
                direction_x /= distance
                direction_y /= distance

            bullet_vel_x = direction_x * bullet_speed
            bullet_vel_y = direction_y * bullet_speed
            bullets.append([bullet_x, bullet_y, bullet_vel_x, bullet_vel_y])

    # Player movement
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < screen_height - player_height:
        player_y += player_speed

    # Bullet movement
    for bullet in bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

    # Enemy movement
    for enemy in enemies:
        enemy_x, enemy_y, enemy_speed = enemy

        player_center_x = player_x + player_width // 2
        player_center_y = player_y + player_height // 2
        enemy_center_x = enemy_x + enemy_width // 2
        enemy_center_y = enemy_y + enemy_height // 2
        direction_x = player_center_x - enemy_center_x
        direction_y = player_center_y - enemy_center_y
        distance = calculate_distance(player_center_x, player_center_y, enemy_center_x, enemy_center_y)

        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        enemy_x += direction_x * enemy_speed
        enemy_y += direction_y * enemy_speed

        enemy[0] = enemy_x
        enemy[1] = enemy_y

        # Collision detection with enemies
        if player_x < enemy_x + enemy_width and player_x + player_width > enemy_x and player_y < enemy_y + enemy_height and player_y + player_height > enemy_y:
            reset_game()

        # Collision detection with bullets
        for bullet in bullets:
            bullet_x, bullet_y, _, _ = bullet
            if bullet_x < enemy_x + enemy_width and bullet_x + bullet_radius > enemy_x and bullet_y < enemy_y + enemy_height and bullet_y + bullet_radius > enemy_y:
                enemies.remove(enemy)
                bullets.remove(bullet)
                break

    # Screen drawing
    screen.fill(black)
    pygame.draw.rect(screen, white, (player_x, player_y, player_width, player_height))
    for enemy in enemies:
        pygame.draw.rect(screen, white, (enemy[0], enemy[1], enemy_width, enemy_height))
    for bullet in bullets:
        pygame.draw.circle(screen, white, (int(bullet[0]), int(bullet[1])), bullet_radius)
    pygame.display.update()

    # FPS control
    clock.tick(FPS)

# Quit the game
pygame.quit()
