import turtle
import random


class Food(turtle.Turtle):
    """Food item for the snake to eat. Randomly placed."""

    def __init__(self, x_bound=280, y_bound=260, color="red"):
        super().__init__(shape="circle")
        self.penup()
        self.color(color)
        self.speed("fastest")
        self.x_bound = x_bound
        self.y_bound = y_bound
        self.refresh()

    def refresh(self):
        x = random.randint(-self.x_bound // 20, self.x_bound // 20) * 20
        y = random.randint(-self.y_bound // 20, self.y_bound // 20) * 20
        self.goto(x, y)

if __name__ == "__main__":
    screen = turtle.Screen()
    screen.setup(width=600, height=600)
    food = Food()
    turtle.done()