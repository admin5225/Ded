import pygame

import os
import sys

pygame.init()
size = width, height = 800, 400
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
groupDED = pygame.sprite.Group()

images = list()
for i in range(1, 35):
    images.append(load_image(f"ded{i}.png"))


class DedMoroz(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)

        self.moved = 0

        self.image = images[self.moved]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.add(groupDED)

    def update(self):
        if self.moved == 33:
            self.moved = 0
        else:
            self.moved += 1

        if left_move:
            self.rect.x -= 5
        elif right_move:
            self.rect.x += 5
        elif up_move:
            self.rect.y -= 5
        elif down_move:
            self.rect.y += 5


        self.image = images[self.moved]


if __name__ == '__main__':
    screen.fill((255, 255, 255))
    ded = DedMoroz(0, 250)

    clock = pygame.time.Clock()

    left_move, right_move, up_move, down_move, move = False, False, False, False, False
    running = True
    while running:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (0, 380, 800, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                move = True
            else:
                left_move, right_move, up_move, down_move, move = False, False, False, False, False

        if move:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                left_move = True
                right_move = False
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                left_move = False
                right_move = True
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                down_move = False
                up_move = True
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                down_move = True
                up_move = False

        all_sprites.update()
        all_sprites.draw(screen)

        clock.tick(10)
        pygame.display.flip()
    pygame.quit()
