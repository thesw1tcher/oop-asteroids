import pygame
import random
import math
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Asteroid:
    def __init__(self, x=None, y=None, radius=None, speed_x=None, speed_y=None, color=(200, 200, 200)):
        self.radius = radius if radius is not None else random.randint(10, 50)
        self.x = x if x is not None else random.randint(self.radius, WIDTH - self.radius)
        self.y = y if y is not None else random.randint(self.radius, HEIGHT - self.radius)
        self.speed_x = speed_x if speed_x is not None else random.choice([1, -1])*random.uniform(3, 7)
        self.speed_y = speed_y if speed_y is not None else random.choice([1, -1])*random.uniform(3, 7)
        self.color = color

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        fl = 0
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.speed_x *= -1
            fl = 1

        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.speed_y *= -1
            fl = 1
        return fl

    def check_collision(self, other):
        return math.hypot(self.x - other.x, self.y - other.y) <= self.radius + other.radius

    def resolve_collision(self, other):
        if self.check_collision(other):
            self.speed_x, other.speed_x = other.speed_x, self.speed_x
            self.speed_y, other.speed_y = other.speed_y, self.speed_y
            return 1
        return 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class Blackhole(Asteroid):
    def __init__(self):
        super().__init__(radius=random.randint(10, 40), speed_x=random.uniform(-1, 1), speed_y=random.uniform(-1, 1))

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (50, 50, 50), (int(self.x), int(self.y)), self.radius, 3)


class Comet(Asteroid):
    def __init__(self, x=None, y=None, radius=random.randint(30, 70), speed_x=None, speed_y=None, color=(255, 150, 50)):
        super().__init__(x, y, radius, speed_x, speed_y, color=color)

    def reduce_size(self):
        if self.radius > 5:
            self.radius *= 0.75
    def resolve_collision(self, other):
        if Asteroid.resolve_collision(self, other): # оверрайд метода родительского класса, при этом вызывая его же
            self.reduce_size()
            if other.__class__ == Comet:
                other.reduce_size()
    def move(self):
        if Asteroid.move(self):
            self.reduce_size()

asteroids = [Asteroid() for _ in range(2)]
blackholes = [Blackhole()]
comets = [Comet()]
objs = asteroids + comets
last_spawn_time = time.time()


clock = pygame.time.Clock()
while 1:
    screen.fill((0, 0, 0))
    fl = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fl = 1
    if fl:
        break
    for blackhole in blackholes:
        blackhole.move()
        blackhole.draw(screen)

    objs = [obj for obj in objs if not any(blackhole.check_collision(obj) for blackhole in blackholes)]

    for i, obj in enumerate(objs):
        for j in range(i + 1, len(objs)):
            obj.resolve_collision(objs[j])
    for obj in objs:
        obj.move()
        obj.draw(screen)

    if time.time() - last_spawn_time > 2:
        obj_type = random.choice([Asteroid, Comet])
        if len(blackholes) < 2:
            obj_type = random.choice([obj_type, obj_type, Blackhole])
        if obj_type == Asteroid:
            objs.append(Asteroid())
        elif obj_type == Blackhole:
            blackholes.append(Blackhole())
        else:
            objs.append(Comet())
        last_spawn_time = time.time()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
