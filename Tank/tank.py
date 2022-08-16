import math
from random import randint as rnd

import pygame as pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
screen_color = (170, 200, 227)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x: int = 50, y: int = 50) -> None:
        """
        ball constructor

        Args:
            x - start horizontal point
            y - start vertical poit
            screen - game field 800 x 600
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 5
        self.vx = 10
        self.vy = -100
        self.color = BLACK
        self.live = 30

    def move(self) -> None:
        """
        move ball per unit of time .

        move the ball in one redraw frame. update self.x and self.y depending on:
        1) self.vx и self.vy,
        2) gravity,
        3) reflection from walls and ground.
        """
        self.vy += 1  # gravity
        if self.x + self.vx > 800 or self.x + self.vx < 0:
            self.vx = -self.vx
        if self.y + self.vy > 600:
            self.vy = -self.vy
            # dampening of inertia during contact with the ground
            self.vx = self.vx / 3
            self.vy = self.vy / 3
            if abs(self.vx) and abs(self.vy) < 2:
                self.y = 1000
                self.vx = 0
                self.vy = 0

        self.x += self.vx
        self.y += self.vy

    def draw(self) -> None:
        """
        draw the ball
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj) -> bool:
        """checks collision ball with target.

        Args:
            obj: target, which collision checking .
        Returns:
            if ball hit the target return true . else return False.
        """
        x_check = abs(self.x - obj.x) - (self.r + obj.r)
        y_check = abs(self.y - obj.y) - (self.r + obj.r)
        if x_check < 0 and y_check < 0:
            return True
        else:
            return False


class TargetBullet(Ball):
    def __init__(self, screen: pygame.Surface, x: int, y: int) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 5
        self.color = WHITE
        self.vx = 0
        self.vy = 0
        self.live = 1

    def move(self) -> None:
        self.vy += 1  # gravity
        self.x += self.vx
        self.y += self.vy
        if self.y > 596:
            self.y = 1000
            self.live = 0

    def hittest_tank(self, obj) -> bool:
        """checks collision ball with tank.

        Args:
            obj: target, which collision checking .
        Returns:
            if ball hit the target return true . else return False.
        """
        x_check = abs(self.x - obj.x) - (self.r + obj.r)
        y_check = abs(self.y - obj.y) - (self.r + obj.r)
        if x_check < 0 and y_check < 0:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen: pygame.Surface) -> None:
        """
        ball constructor

        Args:
            screen - game field 800 x 600
        """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x_gan = 1
        self.y_gan = 450

    def fire2_start(self, event) -> None:
        """
        up the flag when user push mouse button
        Args:
            event: MOUSEBUTTONDOWN
        """
        self.f2_on = 1

    def fire2_end(self, event) -> None:
        """
        Shut with ball when MOUSE left BUTTON UP

        Start velocity (vx and vy) depend on mouse position

        Args:
            event: mouse position
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x_gan, self.y_gan)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - self.y_gan), (event.pos[0] - self.x_gan))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event) -> None:
        """
        takes aim. Depend on mouse cursor position.
        Args:
            event: MOUSEMOTION (mouse position x,y)
        """
        if event:
            self.an = math.atan2((event.pos[1] - self.y_gan), (event.pos[0] - self.x_gan))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self) -> None:
        """
        draw the gun
        """
        st = [self.x_gan, self.y_gan]
        fnx = (st[0] + math.cos(self.an) * (self.f2_power + 30))
        fny = (st[1] + math.sin(self.an) * (self.f2_power + 30))
        pygame.draw.line(screen, self.color, (st[0], st[1]), (fnx, fny), 7)

    def power_up(self) -> None:
        """
        increases power of shoot
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Tank(Gun):
    def __init__(self, screen: pygame.Surface, x_tank: int = 400, y_tank: int = 590) -> None:
        """
        Tank constructor

        """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREEN
        self.x_tank = x_tank
        self.y_tank = y_tank
        self.x_gan = self.x_tank
        self.y_gan = self.y_tank
        self.life = 10

    def move(self, event) -> None:
        """
        move Tank left or right depending of pressed key
        Args:
            event: pressed key on keyboard
        """
        if event.key == pygame.K_LEFT:
            self.x_tank -= 10

        if event.key == pygame.K_RIGHT:
            self.x_tank += 10

    def draw(self) -> None:
        """
        draw the Tank
        """
        fnx = (self.x_tank + math.cos(self.an) * (self.f2_power + 30))
        fny = (self.y_tank + math.sin(self.an) * (self.f2_power + 30))
        pygame.draw.line(screen, self.color, (self.x_tank, self.y_tank), (fnx, fny), 7)
        pygame.draw.line(screen, self.color, (self.x_tank, self.y_tank + 7), (self.x_tank + 15, self.y_tank + 7), 14)
        pygame.draw.line(screen, self.color, (self.x_tank, self.y_tank + 7), (self.x_tank - 15, self.y_tank + 7), 14)

    def fire2_end(self, event) -> None:
        """
        Shut with ball when MOUSE left BUTTON UP

        Start velocity (vx and vy) depend on mouse position

        Args:
            event: mouse position
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x_tank, self.y_tank)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - self.y_gan), (event.pos[0] - self.x_gan))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10


class Target:
    def __init__(self, screen: pygame.Surface, x: int = 400, y: int = 450) -> None:
        """
        target constructor

        Args:
        x - start horizontal point
        y - start vertical poit
        screen - game field 800 x 600
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.color = RED
        self.live = 1
        self.points = 1

    def new_target(self) -> None:
        """
        new target initiation
        """
        x = self.x = rnd(300, 780)
        y = self.y = rnd(50, 550)
        r = self.r = rnd(5, 25)
        color = self.color = RED
        self.live = 1

    def hit(self, points) -> int:
        """
        score calculation.
        Args:
            points: game score

        Returns:
            Int: game score
        """
        points += self.points
        return points

    def draw(self) -> None:
        """
        draw the ball
        """
        self.screen = screen
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


class MovingTarget(Target):
    def __init__(self, screen: pygame.Surface, x: int = 400, y: int = 450) -> None:
        super().__init__(screen, x, y)

        self.color = GREEN
        self.points = 2

    def new_target(self) -> None:
        """
        new moving target initiation
        """
        x = self.x = rnd(300, 780)
        y = self.y = rnd(50, 550)
        r = self.r = rnd(5, 25)
        mtarget_vel_x = self.mtarget_vel_x = rnd(-10, 10)
        mtarget_vel_y = self.mtarget_vel_y = rnd(-10, 10)
        color = self.color = GREEN
        self.live = 1

    def move(self) -> None:
        if self.x + self.mtarget_vel_x > 800 or self.x + self.mtarget_vel_x < 0:
            self.mtarget_vel_x = -self.mtarget_vel_x
        if self.y + self.r + self.mtarget_vel_y > 600 or self.y + self.mtarget_vel_y < 0:
            self.mtarget_vel_y = -self.mtarget_vel_y

        self.x += self.mtarget_vel_x
        self.y += self.mtarget_vel_y


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
points = 0
shoots = 0
balls = []
target_bullets = []
targets = []
count_targets = 1
count_moving_targets = 2
gameCountFlag = 0

clock = pygame.time.Clock()
# gun = Gun(screen)
tank = Tank(screen)

for t in range(count_targets):
    target = Target(screen)
    target.new_target()
    targets.append(target)

for t in range(count_moving_targets):
    target = MovingTarget(screen)
    target.new_target()
    targets.append(target)

finished = False
while not finished:
    screen.fill(screen_color)
    # tank draw
    #print("tank.x is ", tank.x_tank)
    tank.draw()
    # score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(points), True, BLACK)
    screen.blit(text, [30, 20])
    # shoots
    font = pygame.font.Font(None, 36)
    text = font.render("Shoots: " + str(shoots), True, BLACK)
    screen.blit(text, [30, 50])
    # target draw
    for target in targets:
        if type(target) == MovingTarget:
            target.move()
            #print("target.x is ", target.x)
            if abs(target.x - tank.x_tank) < 10:
                new_target_bullet = TargetBullet(screen, target.x, target.y)
                target_bullets.append(new_target_bullet)
                print("target_bullets sozdaldobavil ", len(target_bullets))

    for target in targets:
        if target.live:
            target.draw()
    # balls(bullets) draw
    for b in balls:
        if abs(b.vx) > 1:
            b.draw()
    # TargetBullet draw
    for tb in target_bullets:
        tb.draw()
    pygame.display.update()
    clock.tick(FPS)
    # mouse event manager
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            tank.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            tank.fire2_end(event)
            shoots += 1
        elif event.type == pygame.MOUSEMOTION:
            tank.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tank.move(event)
            if event.key == pygame.K_RIGHT:
                tank.move(event)


    # actions after event
    for b in balls:
        b.move()
        for target in targets:
            if b.hittest(target) and target.live:
                target.live = 0
                gameCountFlag += 1
                points = target.hit(points)
                # when kill all target on screen
                if gameCountFlag == count_targets + count_moving_targets:
                    gameCountFlag = 0
                    balls = []
                    for t in range(count_targets):
                        target = Target(screen)
                        target.new_target()
                        targets.append(target)

                    for t in range(count_moving_targets):
                        target = MovingTarget(screen)
                        target.new_target()
                        targets.append(target)

    tank.power_up()

pygame.quit()
