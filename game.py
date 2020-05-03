import arcade
import os
import random

TITLE  = "A Void Life"
WIDTH  = 800
HEIGHT = 600
SCALE  = 0.2

START     = 4
RUNNING   = 1
PAUSE     = 2
GAME_OVER = 3
FINISHED  = 5

SPEED = 10

START_TEXT = """
PRESS 'S' TO START

PRESS 'P' TO PAUSE
 
PRESS 'Q'TO QUIT
 """

GAME_OVER_TEXT = """
GAME OVER

YOU GOT HIT BY A RESPONSIBILITY

PRESS 'R' TO RESTART
 
PRESS 'Q' TO QUIT
"""

GAME_FINISHED_TEXT = """
GAME FINISHED

YOU SURVIVED TILL 
RETIREMENT

REST IN PEACE
"""


BACKGROUND = "sprites/background/hyperspace2.jpeg"


def get_responsibilities(folder : str) -> list:
    basepath = "sprites/responsibilities/{}".format(folder)
    files = []

    for file in os.listdir(basepath):

        if os.path.isfile(os.path.join(basepath, file)):
            files.append(file)

    return files


MINOR = get_responsibilities('minor')
ADULT = get_responsibilities('adult')
OLD   = get_responsibilities('old')


class RisingText(arcade.Sprite):

    def update(self):
        super().update()

        if self.bottom > SCREEN_HEIGHT:
            self.remove_from_sprite_lists()


class FallingText(arcade.Sprite):

    def update(self):
        super().update()

        if self.top < 0:
            self.remove_from_sprite_lists()


class ScrollingText(arcade.Sprite):

    def update(self):
        super().update()

        if self.right < 0:
            self.remove_from_sprite_lists()


# noinspection PyAttributeOutsideInit
class AvoidLife(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(width, height, title, fullscreen=True)

        self.current_state = START
        self.time = 0.0
        self.age  = 0

        self.scrolling = arcade.SpriteList()
        self.falling   = arcade.SpriteList()
        self.rising    = arcade.SpriteList()
        self.sprites   = arcade.SpriteList()

        self.background = None
        self.memes = {}

        start = arcade.load_texture("sprites/memes/start.jpg")
        pause = arcade.load_texture("sprites/memes/pause.jpg")
        game_over = arcade.load_texture("sprites/memes/game_over.jpg")
        finished  = arcade.load_texture("sprites/memes/dancing-funeral.jpg")

        self.memes[START] = start
        self.memes[PAUSE] = pause
        self.memes[GAME_OVER] = game_over
        self.memes[FINISHED]  = finished

        width, height = self.get_size()

        self.set_viewport(0, width, 0, height)
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):

        self.background = arcade.load_texture(BACKGROUND)

        self.player = arcade.Sprite("sprites/player/plane.png", SCALE)
        self.player.center_y = self.height / 2
        self.player.left = 10

        self.time = 0.0

        self.sprites.append(self.player)

        global SCREEN_HEIGHT
        global SCREEN_WIDTH

        _, SCREEN_WIDTH, _, SCREEN_HEIGHT = self.get_viewport()

    def on_update(self, delta_time):

        self.time += delta_time

        if self.current_state == PAUSE:
            return

        if self.player.collides_with_list(self.scrolling):
            self.game_over()

        if self.player.collides_with_list(self.falling):
            self.game_over()

        if self.player.collides_with_list(self.rising):
            self.game_over()

        self.sprites.update()

        if self.player.top > self.height:
            self.player.top = self.height

        if self.player.right > self.width:
            self.player.right = self.width

        if self.player.left < 0:
            self.player.left = 0

        if self.player.bottom < 0:
            self.player.bottom = 0

        self.scrolling_text()

        if self.age > 18:
            self.falling_text()

        if self.age > 45:
            self.rising_text()

        if self.age >= 20:
            self.game_finished()

    def on_draw(self):

        arcade.start_render()

        self.age = int(self.time) % 60
        time = "AGE: {age:02d}".format(age=self.age)

        self.draw_background()

        if self.current_state == START:
            self.draw_meme(START)
            self.write_text(START_TEXT)

        elif self.current_state == PAUSE:
            self.draw_meme(PAUSE)
            self.write_text("BRUH")

        elif self.current_state == RUNNING:
            self.draw_game()
            self.show_timer(time)

        elif self.current_state == FINISHED:
            self.draw_meme(FINISHED)
            self.write_text(GAME_FINISHED_TEXT)
            self.show_score(self.age)

        else:
            self.draw_meme(GAME_OVER)
            self.write_text(GAME_OVER_TEXT, size=40, align='center')
            self.show_score(self.age)

    def show_score(self, age):

        left, right, bottom, top = self.get_viewport()

        score = "YOU SURVIVED \n{age} YEARS".format(age=age)

        arcade.draw_text(score, right - 500, bottom + 50, arcade.color.WHITE, 40, align='center')

    def game_over(self):
        arcade.pause(0.2)
        self.current_state = GAME_OVER
        self.reset_game()

    def game_finished(self):
        arcade.pause(0.2)
        self.current_state = FINISHED
        self.reset_game()

    def scrolling_text(self):

        if len(self.scrolling) >= 3:
            return

        res = random.choice(MINOR)
        text = ScrollingText("sprites/responsibilities/minor/{}".format(res), 1)

        text.left = random.randint(self.width, self.width + 80)
        text.top = random.randint(10, self.height - 10)

        text.velocity = (random.randint(-10, -5), 0)

        self.scrolling.append(text)
        self.sprites.append(text)

    def falling_text(self):

        if len(self.falling) >= 2:
            return

        res  = random.choice(ADULT)
        text = FallingText("sprites/responsibilities/adult/{}".format(res), 1)

        text.center_x = random.randrange(self.width)
        text.center_y = random.randrange(self.height, self.height+100)

        text.velocity = (0, random.randint(-10, -5))

        self.falling.append(text)
        self.sprites.append(text)

    def rising_text(self):

        if len(self.rising) >= 1:
            return

        res  = random.choice(OLD)
        text = RisingText("sprites/responsibilities/old/{}".format(res))

        text.center_x = random.randrange(self.width)
        text.center_y = random.randrange(-10, 0)

        text.velocity = (0, random.randint(5, 10))

        self.rising.append(text)
        self.sprites.append(text)

    def reset_game(self):

        self.scrolling = arcade.SpriteList()
        self.falling   = arcade.SpriteList()
        self.rising    = arcade.SpriteList()
        self.sprites   = arcade.SpriteList()

    def draw_background(self):

        left, width, bottom, height = self.get_viewport()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            width, height,
                                            self.background)

    def show_timer(self, time):

        _, right, _, top = self.get_viewport()

        arcade.draw_text(time, right - 150, top - 50, arcade.color.WHITE, 20)

    def write_text(self, text: str, x=None, y=None,
                   color=arcade.color.WHITE, size=50, align='center'):

        left, width, bottom, height = self.get_viewport()

        if not x and not y:
            x = width / 2
            y = height / 2

        arcade.draw_text(text, x, y, color, size, align=align)

    def draw_meme(self, meme):

        meme = self.memes[meme]

        arcade.draw_texture_rectangle(WIDTH / 2, HEIGHT / 2,
                                      meme.width,
                                      meme.height,
                                      meme, 0)

    def draw_game(self):

        self.sprites.draw()

    def on_key_press(self, symbol: int, modifiers: int):

        if symbol == arcade.key.S:
            self.reset_game()
            self.setup()
            self.current_state = RUNNING

        if symbol == arcade.key.Q:
            arcade.close_window()

        if symbol == arcade.key.P:

            if self.current_state == RUNNING:
                self.current_state = PAUSE

            elif self.current_state == PAUSE:
                self.current_state = RUNNING

            self.draw_meme(PAUSE)

        if symbol == arcade.key.R:
            self.reset_game()
            self.setup()
            self.current_state = RUNNING

        if (symbol == arcade.key.I) or (symbol == arcade.key.UP):
            self.player.change_y = SPEED

        if (symbol == arcade.key.K) or (symbol == arcade.key.DOWN):
            self.player.change_y = -SPEED

        if (symbol == arcade.key.J) or (symbol == arcade.key.LEFT):
            self.player.change_x = -SPEED

        if (symbol == arcade.key.L) or (symbol == arcade.key.RIGHT):
            self.player.change_x = SPEED

    def on_key_release(self, symbol: int, modifiers: int):

        if (
                symbol == arcade.key.I or
                symbol == arcade.key.K or
                symbol == arcade.key.UP or
                symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0

        if (
                symbol == arcade.key.J or
                symbol == arcade.key.L or
                symbol == arcade.key.LEFT or
                symbol == arcade.key.RIGHT
        ):
            self.player.change_x = 0


def main():
    life = AvoidLife(WIDTH, HEIGHT, TITLE)

    life.setup()
    arcade.run()


if __name__ == '__main__':
    main()
