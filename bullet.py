import pygame

class Bullet:
    def __init__(self, x, y, radius, speed, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction = direction

    def move(self):
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
