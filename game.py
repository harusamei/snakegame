import turtle
import tkinter
import time
import configparser
import os
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
                "screen": {"width": 800, "height": 600, "bg_color": "black"},
                "snake": {"sleep": 0.12, "snake_color": "green", "length": 5, 
                          "food_color": "red"}
            })

        self.width = int(config["screen"]["width"])
        self.height = int(config["screen"]["height"])
        self.bg_color = config["screen"].get("bg_color", "black")
        self.sleep = float(config["snake"].get("sleep", 0.12))
        snake_color = config["snake"].get("snake_color", "green")
        snake_length = int(config["snake"].get('length', 5))
        food_color = config["snake"].get("food_color", "red")

        self.screen = turtle.Screen()
        self.screen.setup(self.width, self.height)
        self.screen.bgcolor(self.bg_color)
        self.screen.title("Turtle Snake Game")
        # 关闭自动刷屏
        self.screen.tracer(0)

        self.snake = Snake(color=snake_color, length=snake_length)
        # bounds for food placement slightly smaller than screen half-size
        self.food = Food(x_bound=self.width//2-20, y_bound=self.height//2-20, 
                         color=food_color)

        self.score = 0
        self.running = False
        self.penNote = turtle.Turtle()
        self.penNote.hideturtle()
        self.penNote.penup()
        self.penNote.goto(0, 0)
        
        # high score persisted in a plain text file at project root
        project_root = os.path.dirname(__file__)
        self.highscore_path = os.path.join(project_root, "highscore.txt")
        print(f"High score path: {self.highscore_path}")
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
        self.paused = False

        # key bindings
        self.screen.listen()
        self.screen.onkey(self.snake.up, "Up")
        self.screen.onkey(self.snake.down, "Down")
        self.screen.onkey(self.snake.left, "Left")
        self.screen.onkey(self.snake.right, "Right")
        # now bind pause toggles
        self.screen.onkey(self.toggle_pause, "space")
        self.screen.onkey(self.toggle_pause, "p")


    def _create_scoreboard(self):
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.penup()
        self.pen.color("white")
        self.pen.goto(0, self.height // 2 - 40)
        self._update_scoreboard()
        
        
    def _update_scoreboard(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.pen.clear()
        self.pen.write(f"Score: {self.score}  High Score: {self.high_score}", align="center", font=("Arial", 16, "normal"))

    def toggle_pause(self):
        """Toggle pause state. When paused, the main loop will show a PAUSED overlay and suspend updates."""
        self.paused = not self.paused
        if not self.paused:
            self.penNote.clear()
        else:
            self.penNote.clear()
            self.penNote.pencolor("yellow")
            self.penNote.write("PAUSED", align="center", font=("Arial", 24, "bold"))
        

    def food_hit(self):
        """count food items which snake head collides with, remove them, and return the count."""
        eated = []
        for idx in range(len(self.food.beans)-1, -1, -1):
            bean, t = self.food.beans[idx]
            if self.snake.head.distance(bean) < 20:
                # collision
                bean.hideturtle()
                bean.clear()
                del bean
                eated.append(idx)
        self.food.beans = [b for i, b in enumerate(self.food.beans) if i not in eated]
        return len(eated)

    def wall_collision(self):
        """Check if snake head collides with wall."""
        x, y = self.snake.head.xcor(), self.snake.head.ycor()
        if x > self.width//2 - 10 or x < -self.width//2 + 10 or y > self.height//2 - 10 or y < -self.height//2 + 10:
            print("Wall collision detected", x, y)
            return True
        return False
    
    def run(self):
        try:
            while True:
                self.screen.update()
                if self.paused:
                    time.sleep(0.1)
                    continue
                if self.running is False:
                    self.running = True
                    self.snake.reset()
                    self.score = 0
                    self._update_scoreboard()
                    self.penNote.clear()
                    self.food.clear()
                    self.food.refresh(200)
                    self.screen.update()
                
                self.snake.move()
 
                # food hit
                count = self.food_hit()
                if count > 0:
                    self.snake.grow(count=count)
                    self.score += 10 * count
                    self._update_scoreboard()

                # check collisions with wall
                if self.wall_collision():
                    self._game_over()
                    self.running = False
                    self.paused = True

                time.sleep(self.sleep)

        except (turtle.Terminator, tkinter.TclError):
            # Turtle's underlying Tk Canvas was closed/destroyed; exit cleanly.
            self._save_high_score()

    def _game_over(self):
        # Save high score on game over (simple exit-time persistence)
        self.penNote.clear()
        self.penNote.pencolor("red")
        self.penNote.write("GAME OVER !", align="center", font=("Arial", 24, "bold"))
        try:
            self._save_high_score()
        except Exception:
            pass


    def _save_high_score(self):
        """Save current high score into `highscore.txt` at project root."""
        try:
            with open(self.highscore_path, "w", encoding="utf-8") as f:
                f.write(str(self.high_score))
        except Exception:
            pass


def periodic_refresh(game, interval=5):
    """Periodically refresh food items on the screen."""
    if not getattr(game, 'paused', False):
        game.food.refresh(20)
        print(f"Food refreshed, in {time.strftime('%H:%M:%S')}")
    screen = game.screen
    screen.ontimer(lambda: periodic_refresh(game, interval), interval * 1000)
    
def peridic_update(game, interval=5):
    if not getattr(game, 'paused', False):
        game.food.update()
        print(f"Food updated, in {time.strftime('%H:%M:%S')}")
    screen = game.screen
    screen.ontimer(lambda: peridic_update(game, interval), interval * 1000)
    

def main():
    here = os.path.dirname(__file__)
    config_path = os.path.join(here, os.pardir, "config.ini")
    game = Game(config_path=config_path)
    peridic_update(game)
    game.run()


if __name__ == "__main__":
    main()
