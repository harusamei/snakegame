import turtle
import tkinter
import time
import configparser
import os
import sys
from snake import Snake
from food import Food

class Game:
    def __init__(self, config_path=None):
        
        config = configparser.ConfigParser()
        if os.path.exists(config_path):
            config.read(config_path)
        else:
            # defaults
            config.read_dict({
                "screen": {"width": "600", "height": "600", "bg_color": "black"},
                "snake": {"speed": "0.12", "snake_color": "green", "length": "5", "food_color": "red"},
            })

        self.width = int(config["screen"]["width"])
        self.height = int(config["screen"]["height"])
        self.bg_color = config["screen"].get("bg_color", "black")
        self.delay = float(config["snake"].get("speed", 0.12))
        snake_color = config["snake"].get("snake_color", "green")
        snake_length = config["snake"].get('length', 5)
        food_color = config["snake"].get("food_color", "red")

        self.screen = turtle.Screen()
        self.screen.setup(self.width, self.height)
        self.screen.bgcolor(self.bg_color)
        self.screen.title("Turtle Snake Game")
        # 关闭自动刷屏
        self.screen.tracer(0)

        self.snake = Snake(color=snake_color, length = snake_length)
        # bounds for food placement slightly smaller than screen half-size
        self.food = Food(x_bound=self.width-20, y_bound=self.height-20, 
                         color=food_color)

        self.score = 0
        # keep config and path (config still used for other settings)
        self.config = config
        self.config_path = config_path

        # high score persisted in a plain text file at project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.highscore_path = os.path.join(project_root, "highscore.txt")
        try:
            if os.path.exists(self.highscore_path):
                with open(self.highscore_path, "r", encoding="utf-8") as f:
                    raw = f.read().strip()
                    self.high_score = int(raw) if raw else 0
            else:
                self.high_score = 0
        except Exception:
            self.high_score = 0
        self._create_scoreboard()

        # key bindings
        self.screen.listen()
        self.screen.onkey(self.snake.up, "Up")
        self.screen.onkey(self.snake.down, "Down")
        self.screen.onkey(self.snake.left, "Left")
        self.screen.onkey(self.snake.right, "Right")

    def _create_scoreboard(self):
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.penup()
        self.pen.color("white")
        self.pen.goto(0, self.height // 2 - 40)
        self._update_scoreboard()
        # pause overlay pen (hidden by default)
        self.pause_pen = turtle.Turtle()
        self.pause_pen.hideturtle()
        self.pause_pen.penup()
        self.pause_pen.color("yellow")
        self.pause_pen.goto(0, 0)
        # now bind pause toggles
        self.paused = False
        self.screen.onkey(self.toggle_pause, "space")
        self.screen.onkey(self.toggle_pause, "p")

    def _update_scoreboard(self):
        self.pen.clear()
        self.pen.write(f"Score: {self.score}  High Score: {self.high_score}", align="center", font=("Arial", 16, "normal"))

    def toggle_pause(self):
        """Toggle pause state. When paused, the main loop will show a PAUSED overlay and suspend updates."""
        self.paused = not getattr(self, "paused", False)
        if not self.paused:
            try:
                self.pause_pen.clear()
            except Exception:
                pass

    def run(self):
        try:
            while True:
                self.screen.update()
                if self.paused:
                    try:
                        self.pause_pen.clear()
                        self.pause_pen.write("PAUSED", align="center", font=("Arial", 24, "bold"))
                    except Exception:
                        pass
                    time.sleep(0.1)
                    continue
                else:
                    try:
                        self.pause_pen.clear()
                    except Exception:
                        pass

                self.snake.move()

                # check collision with food
                if self.snake.head.distance(self.food) < 15:
                    self.food.refresh()
                    self.snake.grow()
                    self.score += 10
                    if self.score > self.high_score:
                        self.high_score = self.score
                    self._update_scoreboard()

                # check collisions with wall
                x, y = self.snake.head.xcor(), self.snake.head.ycor()
                if x > self.width//2 - 10 or x < -self.width//2 + 10 or y > self.height//2 - 10 or y < -self.height//2 + 10:
                    self._game_over()

                # check self collision
                if self.snake.check_self_collision():
                    self._game_over()

                time.sleep(self.delay)
        except (turtle.Terminator, tkinter.TclError):
            # Turtle's underlying Tk Canvas was closed/destroyed; exit cleanly.
            pass

    def _game_over(self):
        # Save high score on game over (simple exit-time persistence)
        try:
            self._save_high_score()
        except Exception:
            pass

        # simple reset behavior
        self.score = 0
        self._update_scoreboard()
        self.snake.reset()

    def _save_high_score(self):
        """Save current high score into `highscore.txt` at project root."""
        try:
            with open(self.highscore_path, "w", encoding="utf-8") as f:
                f.write(str(self.high_score))
        except Exception:
            # ignore failures to avoid crashing game
            pass


def main():
    here = os.path.dirname(__file__)
    config_path = os.path.join(here, os.pardir, "config.ini")
    game = Game(config_path=config_path)
    game.run()


if __name__ == "__main__":
    main()
