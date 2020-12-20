import pygame

import os
import sys


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
groupELF = pygame.sprite.Group()


class Elf(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)

        self.image = load_image('elf.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.add(groupELF)


class DedMoroz(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)

        self.images_right = [load_image('1.png'), load_image('2.png'), load_image('3.png'), load_image('4.png'),
                             load_image('5.png'),
                             load_image('6.png'), load_image('7.png'), load_image('8.png'), load_image('9.png'),
                             load_image('10.png'),
                             load_image('11.png'), load_image('12.png'), load_image('13.png'), load_image('14.png'),
                             load_image('15.png')]
        self.images_left = []

        for image in self.images_right:
            self.images_left.append(pygame.transform.flip(image, True, False))

        self.moved = 0
        image = self.images_right[self.moved]

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.add(groupDED)

    def restart(self):
        self.moved = 0
        self.image = self.images[self.moved]

    def update(self):
        if left_move or right_move:
            if self.moved + 1 < 15:
                self.moved += 1
            else:
                self.moved = 0
        else:
            self.moved = 0

        if left_move:
            self.rect = self.rect.move(-10, 0)
            self.image = self.images_left[self.moved]
        if right_move:
            self.rect = self.rect.move(10, 0)
            self.image = self.images_right[self.moved]


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    screen.fill((255, 255, 255))
    ded = DedMoroz(0, 265)
    elf = Elf(600, 190)

    clock = pygame.time.Clock()

    left_move = False
    right_move = False
    move = False
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
                move = False
                left_move = False
                right_move = False

        if move:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                left_move = True
                right_move = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                left_move = False
                right_move = True

        all_sprites.update()
        all_sprites.draw(screen)

        clock.tick(30)

        pygame.display.flip()
    pygame.quit()