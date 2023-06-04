import pygame
import random

class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move_towards_player(self, player_x, player_y):
        direction_x = player_x - self.x
        direction_y = player_y - self.y
        distance = max(1, abs(direction_x) + abs(direction_y))  # Avoid division by zero

        self.x += (direction_x / distance) * self.speed
        self.y += (direction_y / distance) * self.speed

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

    @staticmethod
    def generate_random_enemy(screen_width, screen_height, enemy_width, enemy_height, average_speed):
        side = random.randint(1, 4)
        if side == 1:  # Top side
            x = random.randint(-enemy_width, screen_width - enemy_width)
            y = random.randint(-screen_height, -enemy_height)
        elif side == 2:  # Right side
            x = random.randint(screen_width, screen_width + enemy_width)
            y = random.randint(-enemy_height, screen_height - enemy_height)
        elif side == 3:  # Bottom side
            x = random.randint(-enemy_width, screen_width - enemy_width)
            y = random.randint(screen_height, screen_height + enemy_height)
        else:  # Left side
            x = random.randint(-screen_width, -enemy_width)
            y = random.randint(-enemy_height, screen_height - enemy_height)

        speed = random.uniform(average_speed - 0.5, average_speed + 0.5)
        return Enemy(x, y, enemy_width, enemy_height, speed)
