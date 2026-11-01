import pygame
pygame.init()

win_width = 700
win_height = 500
pygame.display.set_caption("Rural Maze Battlefield")
window = pygame.display.set_mode((win_width, win_height))

back = pygame.image.load('Topdown_landview.jpg')
back = pygame.transform.scale(back, (win_width, win_height))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = pygame.sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = pygame.sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.side = "left"
    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= win_width - 80:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width:
            self.kill()

w1 = GameSprite('houses.png', win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('housesv.png', 370, 100, 50, 400)
packman = Player('Player-green tank.png', 5, win_height - 80, 80, 80, 0, 0)

img_original = packman.image
packman_right = pygame.transform.rotate(img_original, 0)
packman_left = pygame.transform.rotate(img_original, 180)
packman_up = pygame.transform.rotate(img_original, 90)
packman_down = pygame.transform.rotate(img_original, 270)

barriers = pygame.sprite.Group()
monsters = pygame.sprite.Group()
bullets = pygame.sprite.Group()

barriers.add(w1)
barriers.add(w2)

monster1 = Enemy('Enemy-black tank.png', win_width - 80, 150, 80, 80, 5)
monster2 = Enemy('Enemy-black tank.png', win_width - 80, 230, 80, 80, 5)
final_sprite = GameSprite('Enemy-black tank.png', win_width - 85, win_height - 100, 80, 80)

monsters.add(monster1)
monsters.add(monster2)

finish = False
run = True

while run:
    pygame.time.delay(50)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                packman.x_speed = -5
            elif e.key == pygame.K_d:
                packman.x_speed = 5
            elif e.key == pygame.K_w:
                packman.y_speed = -5
            elif e.key == pygame.K_s:
                packman.y_speed = 5
            elif e.key == pygame.K_SPACE:
                packman.fire()
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_a or e.key == pygame.K_d:
                packman.x_speed = 0
            if e.key == pygame.K_w or e.key == pygame.K_s:
                packman.y_speed = 0

    if not finish:
        window.blit(back, (0, 0))
        if packman.x_speed > 0:
            packman.image = packman_right
        elif packman.x_speed < 0:
            packman.image = packman_left
        elif packman.y_speed < 0:
            packman.image = packman_up
        elif packman.y_speed > 0:
            packman.image = packman_down
        packman.update()
        bullets.update()
        monsters.update()
        pygame.sprite.groupcollide(monsters, bullets, True, True)
        for bullet in bullets:
            if pygame.sprite.spritecollide(bullet, barriers, False):
                bullet.kill()
        barriers.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        final_sprite.reset()
        packman.reset()
        if pygame.sprite.spritecollide(packman, monsters, False):
            finish = True
            img = pygame.image.load('mission failed.jpg')
            window.fill((255, 255, 255))
            window.blit(pygame.transform.scale(img, (win_width, win_height)), (0, 0))
        elif pygame.sprite.collide_rect(packman, final_sprite):
            finish = True
            img = pygame.image.load('mission completed.png')
            window.fill((255, 255, 255))
            window.blit(pygame.transform.scale(img, (win_width, win_height)), (0, 0))
    pygame.display.update()

pygame.quit()