import pyray as rl

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 20
BRICK_SPACING = 10


class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.radius = BALL_RADIUS
        self.speed_x = 5
        self.speed_y = -5

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.speed_x *= -1
        if self.y <= self.radius:
            self.speed_y *= -1

    def draw(self):
        rl.draw_circle(self.x, self.y, self.radius, rl.RED)


class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - 40
        self.speed = 8

    def update(self):
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
            self.x -= self.speed
        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
            self.x += self.speed

        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))

    def draw(self):
        rl.draw_rectangle(self.x, self.y, self.width, self.height, rl.BLUE)

    def get_rect(self):
        return rl.Rectangle(self.x, self.y, self.width, self.height)


class Brick:
    def __init__(self, x, y):
        self.rect = rl.Rectangle(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.destroyed = False

    def draw(self):
        if not self.destroyed:
            rl.draw_rectangle_rec(self.rect, rl.DARKGREEN)


rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Breakout with Raylib")
rl.set_target_fps(60)

ball = Ball()
paddle = Paddle()

bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLUMNS):
        x = col * (BRICK_WIDTH + BRICK_SPACING) + 35
        y = row * (BRICK_HEIGHT + BRICK_SPACING) + 50
        bricks.append(Brick(x, y))

while not rl.window_should_close():
    ball.update()
    paddle.update()

    if rl.check_collision_circle_rec((ball.x, ball.y), ball.radius, paddle.get_rect()):
        ball.speed_y *= -1
        ball.y = paddle.y - ball.radius

    for brick in bricks:
        if not brick.destroyed and rl.check_collision_circle_rec(
            (ball.x, ball.y), ball.radius, brick.rect
        ):
            brick.destroyed = True
            ball.speed_y *= -1
            break

    if ball.y > SCREEN_HEIGHT:
        ball = Ball()

    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    ball.draw()
    paddle.draw()
    for brick in bricks:
        brick.draw()

    score = sum(brick.destroyed for brick in bricks)
    rl.draw_text(f"Score: {score}", 10, 10, 20, rl.DARKGRAY)

    rl.end_drawing()

rl.close_window()
