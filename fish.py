import math
import random
import pygame
import taichi as ti
from pygame.math import Vector2
from menu import Menu

WIDTH = 1200
HEIGHT = 800


class Fishes:

    def __init__(self, amount):
        self.fishes = [Fish() for _ in range(amount)]

    def update(self):
        for i, fish in enumerate(self.fishes):

            fish.move()
            fish.brain()
            fish.show()


class Fish:
    c_perception = 100  # c for controlled
    c_size = 6
    c_tail_size = 18
    c_view_angle = 270
    c_separation_force = 4
    c_align_force = 2
    c_cohesion_force = 4
    c_max_speed = 3
    c_amount = 100

    def __init__(self):
        self.position = Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * 4
        self.angle = self.velocity.as_polar()[1]
        self.acc = Vector2(0, 0)
        self.color = tuple(random.randint(0, 255) for _ in range(3))
        self.tail = []

    def move(self):
        self.acc += self.rules()
        self.position += self.velocity
        self.velocity += self.acc
        self.velocity = self.velocity.normalize() * self.c_max_speed
        self.acc.xy = (0, 0)

    def tail_logic(self):
        if len(self.tail) < self.c_tail_size:
            self.tail.append(self.position.xy)
        else:
            if len(self.tail) != 0:
                self.tail.pop(0)

    def border_logic(self):
        if self.position.x >= WIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y >= HEIGHT:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = HEIGHT

    def blind_spot(self, other_fish):
        _angle_blind = 360 - self.c_view_angle
        if _angle_blind > 90:
            _side = self.c_perception / math.sin(math.radians((180 - 90) / 2))
            _rest = (_angle_blind - 90) / 2
            _rest_side = self.c_perception / math.sin(math.radians((180 - _rest) / 2))
            point_1 = (self.position.x + _side * math.cos(math.radians(self.angle + 180 + 45)),
                       self.position.y + _side * math.sin(math.radians(self.angle + 180 + 45)))
            point_2 = (self.position.x + _side * math.cos(math.radians(self.angle + 180 - 45)),
                       self.position.y + _side * math.sin(math.radians(self.angle + 180 - 45)))
            point_35 = (self.position.x + _rest_side * math.cos(math.radians(self.angle + 180 + 45)),
                        self.position.y + _rest_side * math.sin(math.radians(self.angle + 180 + 45)))
            point_45 = (self.position.x + _rest_side * math.cos(math.radians(self.angle + 180 - 45)),
                        self.position.y + _rest_side * math.sin(math.radians(self.angle + 180 - 45)))
            point_3 = (self.position.x + _rest_side * math.cos(math.radians(self.angle + 180 + 45 + _rest)),
                       self.position.y + _rest_side * math.sin(math.radians(self.angle + 180 + 45 + _rest)))
            point_4 = (self.position.x + _rest_side * math.cos(math.radians(self.angle + 180 - 45 - _rest)),
                       self.position.y + _rest_side * math.sin(math.radians(self.angle + 180 - 45 - _rest)))
            vec_1 = Vector2(self.position.x - point_1[0],
                            self.position.y - point_1[1])
            vec_2 = Vector2(point_1[0] - point_2[0],
                            point_1[1] - point_2[1])
            vec_3 = Vector2(point_2[0] - self.position.x,
                            point_2[1] - self.position.y)
            vec_4 = Vector2(other_fish.position.x - self.position.x,
                            other_fish.position.y - self.position.y)
            vec_5 = Vector2(other_fish.position.x - point_1[0],
                            other_fish.position.y - point_1[1])
            vec_6 = Vector2(other_fish.position.x - point_2[0],
                            other_fish.position.y - point_2[1])
            vec_7 = Vector2(self.position.x - point_35[0],
                            self.position.y - point_35[1])
            vec_8 = Vector2(point_35[0] - point_3[0],
                            point_35[1] - point_3[1])
            vec_9 = Vector2(point_3[0] - self.position.x,
                            point_3[1] - self.position.y)
            vec_10 = Vector2(other_fish.position.x - self.position.x,
                             other_fish.position.y - self.position.y)
            vec_11 = Vector2(other_fish.position.x - point_35[0],
                             other_fish.position.y - point_35[1])
            vec_12 = Vector2(other_fish.position.x - point_3[0],
                             other_fish.position.y - point_3[1])
            vec_13 = Vector2(self.position.x - point_45[0],
                             self.position.y - point_45[1])
            vec_14 = Vector2(point_45[0] - point_4[0],
                             point_45[1] - point_4[1])
            vec_15 = Vector2(point_4[0] - self.position.x,
                             point_4[1] - self.position.y)
            vec_16 = Vector2(other_fish.position.x - self.position.x,
                             other_fish.position.y - self.position.y)
            vec_17 = Vector2(other_fish.position.x - point_45[0],
                             other_fish.position.y - point_45[1])
            vec_18 = Vector2(other_fish.position.x - point_4[0],
                             other_fish.position.y - point_4[1])
            vec_mult_1, vec_mult_2, vec_mult_3 = vec_1.cross(vec_4), vec_2.cross(vec_5), vec_3.cross(vec_6)
            vec_mult_4, vec_mult_5, vec_mult_6 = vec_7.cross(vec_10), vec_8.cross(vec_11), vec_9.cross(vec_12)
            vec_mult_7, vec_mult_8, vec_mult_9 = vec_13.cross(vec_16), vec_14.cross(vec_17), vec_15.cross(vec_18)

            if vec_mult_1 > 0 and vec_mult_2 > 0 and vec_mult_3 > 0:
                return True
            if vec_mult_4 > 0 and vec_mult_5 > 0 and vec_mult_6 > 0:
                return True
            if vec_mult_7 > 0 and vec_mult_8 > 0 and vec_mult_9 > 0:
                return True
            if vec_mult_1 < 0 and vec_mult_2 < 0 and vec_mult_3 < 0:
                return True
            if vec_mult_4 < 0 and vec_mult_5 < 0 and vec_mult_6 < 0:
                return True
            if vec_mult_7 < 0 and vec_mult_8 < 0 and vec_mult_9 < 0:
                return True
            else:
                return False
        if _angle_blind <= 90:
            _side = self.c_perception / math.sin(math.radians((180 - _angle_blind) / 2))
            point_1 = (self.position.x + _side * math.cos(math.radians(self.angle + 180 + _angle_blind / 2)),
                       self.position.y + _side * math.sin(math.radians(self.angle + 180 + _angle_blind / 2)))
            point_2 = (self.position.x + _side * math.cos(math.radians(self.angle + 180 - _angle_blind / 2)),
                       self.position.y + _side * math.sin(math.radians(self.angle + 180 - _angle_blind / 2)))
            vec_1 = Vector2(self.position.x - point_1[0],
                            self.position.y - point_1[1])
            vec_2 = Vector2(point_1[0] - point_2[0],
                            point_1[1] - point_2[1])
            vec_3 = Vector2(point_2[0] - self.position.x,
                            point_2[1] - self.position.y)
            vec_4 = Vector2(other_fish.position.x - self.position.x,
                            other_fish.position.y - self.position.y)
            vec_5 = Vector2(other_fish.position.x - point_1[0],
                            other_fish.position.y - point_1[1])
            vec_6 = Vector2(other_fish.position.x - point_2[0],
                            other_fish.position.y - point_2[1])
            vec_mult_1, vec_mult_2, vec_mult_3 = vec_1.cross(vec_4), vec_2.cross(vec_5), vec_3.cross(vec_6)
            if vec_mult_1 > 0 and vec_mult_2 > 0 and vec_mult_3 > 0:
                return True
            if vec_mult_1 < 0 and vec_mult_2 < 0 and vec_mult_3 < 0:
                return True
            else:
                return False

    def blind_spot_test(self):
        _angle_blind = 360 - self.c_view_angle

        if _angle_blind > 90:
            _side = self.c_perception / math.sin(math.radians((180 - 90) / 2))
            _rest = (_angle_blind - 90) / 2
            _rest_side = self.c_perception / math.sin(math.radians((180 - _rest) / 2))
            point_1 = (self.position.x + _side * math.cos(math.radians(self.angle + 180 + 45)),
                       self.position.y + _side * math.sin(math.radians(self.angle + 180 + 45)))
            point_2 = (self.position.x + _side * math.cos(math.radians(self.angle + 180 - 45)),
                       self.position.y + _side * math.sin(math.radians(self.angle + 180 - 45)))
            point_35 = (self.position.x + _rest_side * math.cos(math.radians(self.angle + 180 + 45)),
                        self.position.y + _rest_side * math.sin(math.radians(self.angle + 180 + 45)))
            point_45 = (self.position.x + _rest_side * math.cos(math.radians(self.angle + 180 - 45)),
                        self.position.y + _rest_side * math.sin(math.radians(self.angle + 180 - 45)))
            point_3 = (self.position.x + _rest_side * math.cos(math.radians(self.angle + 180 + 45 + _rest)),
                       self.position.y + _rest_side * math.sin(math.radians(self.angle + 180 + 45 + _rest)))
            point_4 = (self.position.x + _rest_side * math.cos(math.radians(self.angle + 180 - 45 - _rest)),
                       self.position.y + _rest_side * math.sin(math.radians(self.angle + 180 - 45 - _rest)))
            return point_1, point_2, point_3, point_35, point_4, point_45
        if _angle_blind <= 90:
            _side = self.c_perception / math.sin(math.radians((180 - _angle_blind) / 2))

            point_1 = (self.position.x + _side * math.cos(math.radians(self.angle + 180 + _angle_blind / 2)),

                       self.position.y + _side * math.sin(math.radians(self.angle + 180 + _angle_blind / 2)))

            point_2 = (self.position.x + _side * math.cos(math.radians(self.angle + 180 - _angle_blind / 2)),

                       self.position.y + _side * math.sin(math.radians(self.angle + 180 - _angle_blind / 2)))
            return point_1, point_2

    def rules(self):
        steering = Vector2(0, 0)
        total = 0
        blind_total = 0
        avg_vector_sep = Vector2(0, 0)
        avg_vector_align = Vector2(0, 0)
        center_of_mass = Vector2(0, 0)
        for fish in App.fishes:
            if self.position != fish.position and abs(fish.position.x - self.position.x < self.c_perception) and abs(
                    fish.position.y - self.position.y < self.c_perception):
                distance = Vector2(fish.position - self.position).length()
                if distance < self.c_perception:
                    diff = self.position - fish.position
                    diff /= distance
                    avg_vector_sep += diff
                    total += 1
                if distance < self.c_perception and self.blind_spot(fish) is False:
                    avg_vector_align += fish.velocity
                    center_of_mass += fish.position
                    blind_total += 1

        if total > 0:
            avg_vector_sep /= total
            avg_vector_sep = avg_vector_sep.normalize()
            steering += (avg_vector_sep - self.velocity).normalize() * (self.c_separation_force / 10)
        if blind_total > 0:
            avg_vector_align /= blind_total
            center_of_mass /= blind_total
            avg_vector_align = avg_vector_align.normalize()
            vec_to_com = center_of_mass - self.position
            if Vector2(vec_to_com).length() > 0:
                vec_to_com = vec_to_com.normalize()

            steering += (vec_to_com - self.velocity).normalize() * (self.c_cohesion_force / 10)
            steering += (avg_vector_align - self.velocity).normalize() * (self.c_align_force / 10)

        return steering

    def brain(self):
        self.border_logic()
        self.tail_logic()
        self.angle = self.velocity.as_polar()[1]

    def show(self):
        for i, tail_segment in enumerate(self.tail):
            if self.c_tail_size - i + 1 != 0:
                pygame.draw.circle(App.screen,
                                   (abs(self.color[0] / (self.c_tail_size - i + 1)),
                                    abs(self.color[1] / (self.c_tail_size - i + 1)),
                                    abs(self.color[2] / (self.c_tail_size - i + 1))),
                                   tail_segment.xy,
                                   self.c_size * i / self.c_tail_size)

        pygame.draw.circle(App.screen, self.color, self.position, self.c_size)

        # pygame.draw.lines(App.screen, self.color, False,
        #                   (*self.blind_spot_test(), self.position.xy))
        # pygame.draw.circle(App.screen, (255, 255, 255), self.position.xy, 100, 1)


class App:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    fishes_cls = Fishes(Fish.c_amount)
    fishes = fishes_cls.fishes
    window_cls = Menu(Fish)
    window = window_cls.make_widgets()

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        while True:
            amount_save = len(self.fishes)
            if amount_save != Fish.c_amount:
                if amount_save < Fish.c_amount:
                    self.fishes.append(Fish())
                if amount_save > Fish.c_amount:
                    self.fishes.pop(0)
            self.window_cls.update_()
            self.window.update()
            App.screen.fill(pygame.Color('Black'))
            self.fishes_cls.update()
            pygame.display.flip()
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
