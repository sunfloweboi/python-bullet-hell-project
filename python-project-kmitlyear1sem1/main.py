import pygame
import math
import random
import os


pygame.font.init()
pygame.mixer.init()


BOSSLEVEL = 3
POWERUPS = []
POINTS = []
SHOOTDELAY = 20
CIRCLESHOOTDELAY = 40
SPIRALSHOOTDELAY = 1


WIDTH, HEIGHT = 700, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pointsimg = pygame.image.load("points.png")
pygame.display.set_caption("buretto heru")
ENEMYIMG = pygame.image.load("enemy.png")
BOMBIMG = pygame.image.load("bomb.png")
bombimg = pygame.transform.scale(BOMBIMG, (30, 40))
playerimg = pygame.image.load("player.png")
PLAYERIMG = pygame.transform.scale(playerimg, (23, 40))
BOSS = pygame.image.load("boss.png")
BOSSIMG = pygame.transform.scale(BOSS, (150, 150))
RED_bullet = pygame.image.load("redbullet.png")
REDBULLET = pygame.transform.scale(RED_bullet, (40, 40))
BLUE_bullet = pygame.image.load("new_bullet.png")
NEWBULLET = pygame.transform.scale(BLUE_bullet, (18, 18))
NEWBULLET = NEWBULLET.convert_alpha()
NEWBULLET.set_alpha(180)
alt_bullet = pygame.image.load("alt_bullet.png")
ALTBULLET = pygame.transform.scale(alt_bullet, (10, 10))

BG = pygame.transform.scale(pygame.image.load("BG.jpg"), (WIDTH, HEIGHT))


class BULLET:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def moveangle(self, rotation, vel):
        self.x = math.cos(rotation) * vel + self.x
        self.y = math.sin(rotation) * vel + self.y

    def off_screen_height(self, height):
        return not (self.y <= height+200 and self.y >= -200)

    def off_screen_width(self, width):
        return not (self.x <= width+200 and self.x >= -200)

    def collision(self, obj):
        return collide(self, obj)


class Character:



    def __init__(self, x, y, health=1):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.bullet_img = None
        self.bullets = []
        self.leftbullets = []
        self.rightbullets = []
        self.cd = 0
        

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window)
        for bullet in self.leftbullets:
            bullet.draw(window)
        for bullet in self.rightbullets:
            bullet.draw(window)

    
    def shoot(self):
        bullet = BULLET(self.x, self.y, self.bullet_img)
        self.bullets.append(bullet)

    def doubleshoot(self):
        bullet1 = BULLET(self.x+10, self.y, self.bullet_img)
        self.bullets.append(bullet1)
        bullet2 = BULLET(self.x-10, self.y, self.bullet_img)
        self.bullets.append(bullet2)

    def tripleshoot(self):
        bullet1 = BULLET(self.x+10, self.y, self.bullet_img)
        self.rightbullets.append(bullet1)
        bullet2 = BULLET(self.x, self.y, self.bullet_img)
        self.bullets.append(bullet2)
        bullet3 = BULLET(self.x-10, self.y, self.bullet_img)
        self.leftbullets.append(bullet3)

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()


class Player(Character):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.img = PLAYERIMG
        self.bullet_img = NEWBULLET
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = health
        self.score = 0
        self.bombcount = 1

    def bomb(self, obj):
        if self.bombcount > 0:
            for i in range(6):
                for i in obj.allbullets:
                    for bullet in i:
                        point = Points(bullet.x, bullet.y)
                        POINTS.append(point)
                        i.remove(bullet)

            self.bombcount -= 1

    def move_bullets(self, vel, objs):

        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen_height(HEIGHT) or bullet.off_screen_width(WIDTH):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        self.score += random.randrange(950, 1000)
                        if obj.health > 50:
                            obj.health -= 50
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                        else:
                            objs.remove(obj)
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                                if random.randrange(0, 6) == 1:
                                    powerup = Powerups(obj.x, obj.y)
                                    POWERUPS.append(powerup)

        for bullet in self.rightbullets:
            bullet.moveangle(100*math.pi/180, vel)
            if bullet.off_screen_height(HEIGHT) or bullet.off_screen_width(WIDTH):
                self.rightbullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        self.score += random.randrange(800, 1000)
                        if obj.health > 50:
                            obj.health -= 50
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                        else:
                            objs.remove(obj)
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                                if random.randrange(0, 6) == 1:
                                    powerup = Powerups(obj.x, obj.y)
                                    POWERUPS.append(powerup)

        for bullet in self.leftbullets:
            bullet.moveangle(80*math.pi/180, vel)
            if bullet.off_screen_height(HEIGHT) or bullet.off_screen_width(WIDTH):
                self.leftbullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        self.score += random.randrange(800, 1000)
                        if obj.health > 50:
                            obj.health -= 50
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                        else:
                            objs.remove(obj)
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                                if random.randrange(0, 6) == 1:
                                    powerup = Powerups(obj.x, obj.y)
                                    POWERUPS.append(powerup)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                         self.img.get_height() + 10, self.img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.img.get_height() +
                         10, self.img.get_width() * (self.health/self.max_health), 10))


class Boss(Character):
    def __init__(self, x, y, health=100000):
        super().__init__(x, y, health)
        self.img = BOSSIMG
        self.bullet_img = REDBULLET
        self.bullet_img2 = ALTBULLET
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = health
        self.bulletrotation = 0.25
        self.allbullets = []
        for i in range (95):
            self.allbullets.append([])
       

    def draw(self, window):
        super().draw(window)
        window.blit(self.img, (self.x, self.y))
        for i in range(len(self.allbullets)):
            for bullet in self.allbullets[i]:
                bullet.draw(window)
        self.healthbar(window)

    def move(self, vel):
        self.y += vel

    def move_bullets(self, vel, player):
        for i in range(85, 95):
            for bullet in self.allbullets[i]:

                bullet.move(vel)

                if bullet.off_screen_height(HEIGHT) or bullet.off_screen_width(WIDTH):
                    self.allbullets[i].remove(bullet)
                else:
                    if bullet.collision(player):
                        self.allbullets[i].remove(bullet)
                        player.health -= 10

    def move_circular(self, vel, player):

        for i in range(25):
            for bullet in self.allbullets[i]:
                bullet.moveangle(0+i*self.bulletrotation, vel)
                if bullet.off_screen_height(HEIGHT) or bullet.off_screen_width(WIDTH):
                    self.allbullets[i].remove(bullet)
                else:
                    if bullet.collision(player):
                        self.allbullets[i].remove(bullet)
                        player.health -= 10
        for i in range(25, 50):
            for bullet in self.allbullets[i]:
                bullet.moveangle(0.125+(i-14)*0.25, vel)
                if bullet.off_screen_height(HEIGHT) or bullet.off_screen_width(WIDTH):
                    self.allbullets[i].remove(bullet)
                else:
                    if bullet.collision(player):
                        self.allbullets[i].remove(bullet)
                        player.health -= 10

    def movespiral(self, vel, player):
        for i in range(51, 80):
            for bullet in self.allbullets[i]:
                bullet.moveangle(0+i*0.217, vel)
                if bullet.off_screen_height(HEIGHT) or bullet.off_screen_width(WIDTH):
                    self.allbullets[i].remove(bullet)
                else:
                    if bullet.collision(player):
                        self.allbullets[i].remove(bullet)
                        player.health -= 10

    def healthbar(self, window):
        pygame.draw.rect(window, (0, 0, 0), (0, 0, WIDTH, 15))
        pygame.draw.rect(window, (200, 0, 0), (0, 0, WIDTH *
                         (self.health/self.max_health), 15))

    def waterfallshoot(self):
        for i in range(85, 95):
            bullet = BULLET(0+1+(i-85)*75, self.y+130, self.bullet_img2)
            self.allbullets[i].append(bullet)

    def shoot_circular1(self):
        for i in range(25):
            bullet = BULLET(self.x + 50, self.y + 130, self.bullet_img)
            self.allbullets[i].append(bullet)

    def shoot_circular2(self):
        for i in range(25, 50):
            bullet = BULLET(self.x + 50, self.y + 130, self.bullet_img)
            self.allbullets[i].append(bullet)

    def shootspiral(self, i):
        bullet = BULLET(self.x + 50, self.y + 130, self.bullet_img)
        self.allbullets[i+51].append(bullet)

    def reverseshootspiral(self, i):
        bullet = BULLET(self.x + 50, self.y + 130, self.bullet_img)
        self.allbullets[79-i].append(bullet)


class Enemy(Character):

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.img, self.bullet_img = ENEMYIMG, REDBULLET
        self.mask = pygame.mask.from_surface(self.img)
        self.enemyshootdelay = 30

    def move(self, vel):
        self.y += vel
        self.x += random.randint(-1, 1)

    def shoot(self):
        if self.cd == 0:
            bullet = BULLET(self.x-20, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.cd = 1

    def move_bullets(self, vel, obj):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            # bullet.move(vel)
            if bullet.off_screen_height(HEIGHT) or bullet.off_screen_width(WIDTH):
                self.bullets.remove(bullet)

            elif bullet.collision(obj):
                obj.health -= 10
                self.bullets.remove(bullet)

    def cooldown(self):
        if self.cd >= self.enemyshootdelay:
            self.cd = 0
        elif self.cd > 0:
            self.cd += 1



class Points:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pointsimg
        self.mask = pygame.mask.from_surface(self.img)

    def moveangle(self, rotation, vel):
        self.x = math.cos(rotation) * vel + self.x
        self.y = math.sin(rotation) * vel + self.y

    def move(self, vel, player):

        self.moveangle(homing(self, player), vel)
        if self.collision(player):
            player.score += 100
            POINTS.remove(self)
        if self.off_screen_height(HEIGHT) or self.off_screen_width(WIDTH):
            POINTS.remove(self)

    def off_screen_height(self, height):
        return not (self.y <= height and self.y >= 0)

    def off_screen_width(self, width):
        return not (self.x <= width and self.x >= 0)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def collision(self, obj):
        return collide(self, obj)

class Powerups:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        powerupimg = pygame.image.load("powerup.png")
        self.img = pygame.transform.scale(powerupimg, (20, 20))
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, obj, vel=1):
        self.y += vel
        if self.collision(obj):
            if obj.health < obj.max_health:
                obj.health += 10
            POWERUPS.remove(self)
        if self.off_screen_height(HEIGHT):
            POWERUPS.remove(self)

    def off_screen_height(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


        
clock = pygame.time.Clock()
pause_font = pygame.font.SysFont("comicsans", 100)

def pause():
        Paused = True
        while Paused == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        Paused = False
            pygame.display.update()
            pause_label = pause_font.render("l l", 1, (255, 255, 255))
            WIN.blit(pause_label, (WIDTH/2 - pause_label.get_width() /
                     2, HEIGHT/2 - pause_label.get_height()/2))
            clock.tick(10)

def homing(self, obj):
    dx = self.x - obj.x
    dy = self.y - obj.y
    if dx == 0:
        return math.atan(-dx/dy)
    elif dx > 0:
        if dy > 0:
            return (math.atan(dy/dx) + math.pi)
        else:
            return (math.atan(dy/dx) + math.pi)
    else:
        return (math.atan(dy/dx))


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
        
    HIGHSCOREFILE = open("highscore.txt", "r")
    HIGHSCORE = int(HIGHSCOREFILE.read())
    HIGHSCOREFILE.close()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1, 0.0, 5000)

   

    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    score_font = pygame.font.SysFont("comicsans", 30)
    

    enemies = []
    wave_length = 5
    enemy_vel = 1
    boss_vel = 0.5
    BOSSES = []

    player_vel = 3.5
    bullet_vel = 10
    enemybullet_vel = 5
    bossbullet_vel = 3

    player = Player(WIDTH/2-20, HEIGHT-100)
    clock = pygame.time.Clock()

    

    def redraw_window():
        WIN.blit(BG, (0, 0))
        HIGHSCOREFILE = open("highscore.txt", "r")
        HIGHSCORE = int(HIGHSCOREFILE.read())
        HIGHSCOREFILE.close()
        if player.score > HIGHSCORE:
            HIGHSCORE = player.score

        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        score_label = score_font.render(f"Score: {player.score}", 1, (255, 255, 255))
        highscore_label = score_font.render(f"Highscore: {HIGHSCORE}", 1, (255, 255, 255))
        lives_label = score_font.render(f"Lives: {lives}", 1, (255, 255, 255))

        WIN.blit(lives_label, (WIDTH - lives_label.get_width() - 10, HEIGHT-50))
        WIN.blit(score_label, (WIDTH - score_label.get_width() - 500, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(highscore_label, (WIDTH - level_label.get_width() - 503, 40))

        for i in range(player.bombcount):
            WIN.blit(bombimg, (10 + i*40, HEIGHT-50))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        for powerup in POWERUPS:
            powerup.draw(WIN)

        for point in POINTS:
            point.draw(WIN)

        for boss in BOSSES:
            boss.draw(WIN)

        pygame.display.update()

    turn = -1
    bossspiralshootimer = 0
    shootimer = 0
    bossshootimer1 = 0
    bossshootimer2 = 0
    circlestart = False
    hitleft = False
    hitright = False

    while run:

        clock.tick(FPS)
        redraw_window()
        shootimer += 1

        if shootimer == SHOOTDELAY and player.score < 50000:
            player.shoot()
            shootimer = 0
        elif shootimer == SHOOTDELAY and player.score >= 50000 and player.score < 100000:
            player.doubleshoot()
            shootimer = 0
        elif shootimer == SHOOTDELAY and player.score >= 100000:
            player.tripleshoot()
            shootimer = 0

        if lives <= 0 or player.health <= 0:
            if player.score > HIGHSCORE:
                    HIGHSCORE = player.score
                    HIGHSCOREFILE = open("highscore.txt", "w")
                    HIGHSCOREFILE.write(str(HIGHSCORE))
                    HIGHSCOREFILE.close()
               
            pygame.mixer.music.stop()
            lose()

        if len(enemies) == 0 and len(BOSSES) == 0:

            level += 1
            wave_length += 5
            if level < BOSSLEVEL:
                for i in range(wave_length):
                    # if else random(0,1) == 1 to add different type of enemies.
                    enemy = Enemy(random.randrange(
                        50, WIDTH-100), random.randrange(-1500, -100), random.randrange(50, 100))
                    enemies.append(enemy)
            elif level == BOSSLEVEL:
                boss = Boss(WIDTH/2 - 100, -100)
                BOSSES.append(boss)

                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load("bossmusic.mp3")
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1, 0.0, 5000)
            elif level > BOSSLEVEL:
                if player.score > HIGHSCORE:
                    HIGHSCORE = player.score
                    HIGHSCOREFILE = open("highscore.txt", "w")
                    HIGHSCOREFILE.write(str(HIGHSCORE))
                    HIGHSCOREFILE.close()
                pygame.mixer.music.stop()
                won(player.score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_p]:
            pause()
        if keys[pygame.K_b]:
            if level == BOSSLEVEL:
                player.bomb(boss)
            

        for powerup in POWERUPS:
            powerup.move(player)

        for points in POINTS:
            points.move(10, player)

        for enemy in enemies:
            enemy.move(enemy_vel)
            # movebullet
            enemy.move_bullets(enemybullet_vel, player)

            if random.randrange(0, 1*60) == 1:
                # enemyshoot
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        for boss in BOSSES:

            if boss.y < 0:
                boss.move(enemy_vel)

            if boss.health < boss.max_health*9/10:
                if boss.x == 0:
                    hitleft = True
                    hitright = False

                elif boss.x == WIDTH - boss.get_width():
                    hitleft = False
                    hitright = True

                if hitright == True:
                    boss.x -= boss_vel
                if hitleft == True:
                    boss.x += boss_vel
                if boss.y == 0 and hitright == False and hitleft == False:
                    boss.x += boss_vel

            if boss.health <= boss.max_health/2:
                if boss.y >= 0:
                    bossshootimer1 += 1
                if circlestart == True:
                    bossshootimer2 += 1

                if bossshootimer1 == CIRCLESHOOTDELAY:
                    boss.shoot_circular1()
                    bossshootimer1 = 0

                    circlestart = True
                if bossshootimer2 == CIRCLESHOOTDELAY/2:
                    boss.shoot_circular2()
                    bossshootimer2 = 0
                    boss.waterfallshoot()
                    circlestart = False

            else:
                if boss.y >= 0:
                    bossspiralshootimer += 1

                    for spiralcounter in range(10000):
                        if bossspiralshootimer == SPIRALSHOOTDELAY*(spiralcounter+1):
                            if spiralcounter % 29 == 0:
                                turn += 1
                            if boss.health > boss.max_health/2:
                                boss.shootspiral(spiralcounter-(turn*29))
                        if bossspiralshootimer == SPIRALSHOOTDELAY*(spiralcounter*50):
                            boss.waterfallshoot()

            boss.movespiral(bossbullet_vel, player)
            boss.move_circular(bossbullet_vel, player)
            boss.move_bullets(bossbullet_vel, player)

        if level < BOSSLEVEL:
            player.move_bullets(-bullet_vel, enemies)
        elif level >= BOSSLEVEL:
            player.move_bullets(-bullet_vel, BOSSES)

    

def won(score):
    HIGHSCOREFILE = open("highscore.txt", "r")
    HIGHSCORE = int(HIGHSCOREFILE.read())
    HIGHSCOREFILE.close()
    won_font = pygame.font.SysFont("comicsans", 70)
    score_font = pygame.font.SysFont("comicsans", 50)
    hihgscorefont = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = won_font.render("You won!", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        score_label = score_font.render(
            "Score: " + str(score), 1, (255, 255, 255))
        WIN.blit(score_label, (WIDTH/2 - score_label.get_width()/2, 450))
        highscore_label = hihgscorefont.render(
            "Highscore: " + str(HIGHSCORE), 1, (255, 255, 255))
        WIN.blit(highscore_label, (WIDTH/2 - highscore_label.get_width()/2, 500))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


def lose():
    won_font = pygame.font.SysFont("comicsans", 35)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = won_font.render(
            "You lose, better luck next time!", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
        
    pygame.quit()



def check_files():
    if os.path.exists("highscore.txt"):
        return FileNotFoundError
    else:
        raise ValueError



try :
    check_files()
    
except ValueError:
    print("This must be the first time you have played this game, a highscore file has been created")
    f = open("highscore.txt", "w") 
    f.write("0")
    f.close()

main()
        

    
