import pygame

import os
import sys

pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group()
plates = pygame.sprite.Group()
groupDED = pygame.sprite.Group()

images = list()
for i in range(1, 35):
    images.append(load_image(f"ded{i}.png"))


class Plate(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites, plates)

        self.image = pygame.Surface((x2, y2))
        self.image.fill((150, 150, 150))
        self.rect = pygame.Rect(x1, y1, x2, y2)


class DedMoroz(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)

        self.moved = 1

        self.image = images[self.moved - 1]
        self.rect = self.image.get_rect()

        self.width = 150
        self.height = 150
        self.rect.x = x
        self.rect.y = y
        self.add(groupDED)

        self.jump = False
        #Начальная скорость прыжка
        self.speed_jump = 15
        self.jump_count = self.speed_jump
        self.step = 5

    def get_jump(self):
        self.jump = True
        self.jump_count = self.speed_jump

    def update(self):
        if self.moved % 10 == 0:
            self.image = images[(self.moved - 1) // 10]
        self.moved = (self.moved + 1) % 331

        if left_move:
            self.rect.x -= self.step
        if right_move:
            self.rect.x += self.step

        if self.jump:
            if self.jump_count >= -self.speed_jump:
                self.rect.y -= self.jump_count
                self.jump_count -= 1
            else:
                self.jump = False

    def move_next(self):
        self.rect.x = 0
        self.rect.y = 430

    def move_back(self):
        self.rect.x = 950
        self.rect.y = 430


if __name__ == '__main__':
    screen.fill((255, 255, 255))
    ded = DedMoroz(0, 430)
    plate = Plate(0, 580, 1000, 20)
    clock = pygame.time.Clock()

    fons = [load_image('fon1.jpg'), load_image('fon2.jpg')]
    count = 1

    left_move, right_move, move = False, False, False

    running = True
    while running:
        screen.blit(fons[count - 1], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                move = True
            else:
                if not(keys[pygame.K_LEFT]) and not(keys[pygame.K_RIGHT]):
                    right_move = False
                    left_move = False
                    move = False

        if move:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                left_move = True
                right_move = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                left_move = False
                right_move = True

            if ded.rect.x > 950:
                ded.move_next()
                count = (count + 1) % (len(fons) + 1)
            if ded.rect.x < -30:
                ded.move_back()
                count = (count - 1) % (len(fons) + 1)

            if not (ded.jump):
                if keys[pygame.K_UP]:
                    ded.get_jump()

        all_sprites.update()
        all_sprites.draw(screen)

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
