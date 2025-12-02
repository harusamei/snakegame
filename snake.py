import turtle
import time
import random
import math


class Snake:
    """Snake represented as a list of turtle segments.

    Methods:
    - move(): advance the snake forward one step
    - change_direction(dir): change movement direction (prevents reverse)
    - up()/down()/left()/right(): helpers to set direction
    - grow(): add a segment at the tail
    - reset(): reset to initial state
    - check_self_collision(): return True if head collides with body
    """
    Stretch_factor = 1                      # 放大倍数为1，即不放大，default基准，20*20
    TURTLE_SIZE = 20                        # turtle的基准大小是20x20像素
    MOVE_DISTANCE = TURTLE_SIZE * Stretch_factor     # 一个身位
    DIRECTIONS = {"up": 90, "down": 270, "left": 180, "right": 0}
    opposites = {"up": 270, "down": 90, "left": 0, "right": 180}

    def __init__(self, color="blue", length=3):
        self.color = color
        self.direction = "right"
        self.segments = []
        self._create_snake(length)
        self.head = self.segments[0]

    def _create_head(self, position):
        seg = turtle.Turtle("arrow")       # 蛇头是个三角
        seg.color("green")
        seg.setheading(self.DIRECTIONS['right'])
        seg.shapesize(self.Stretch_factor * 0.9, self.Stretch_factor * 0.9, 5)
        seg.penup()
        seg.goto(position)
        return seg
    
    def _create_segment(self, position):
        seg = turtle.Turtle("circle")
        seg.shapesize(stretch_wid=self.Stretch_factor * 0.9,
                      stretch_len=self.Stretch_factor * 0.9)  # slightly smaller than default
        seg.color(self.color)
        seg.penup()
        seg.goto(position)
        return seg

    def _create_snake(self, length=3):
        self._remove_snake()
        length = max(3, length)
        starting_positions = (0, 0)
        self.segments.append(self._create_head(starting_positions))
        for i in range(length-1):
            pos = (-self.TURTLE_SIZE * self.Stretch_factor * (i+1), 0)
            self.segments.append(self._create_segment(pos))
        self.head = self.segments[0]

    def _remove_snake(self):
        # del segments and recreate
        for seg in self.segments:
            seg.hideturtle()
            del seg
        self.segments.clear()

    def reset(self, length=3):
        self._create_snake(length)
    
    def move(self):
        # Move segments from tail to head
        for idx in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[idx - 1].xcor()+random.randint(-1,1)
            new_y = self.segments[idx - 1].ycor()+random.randint(-1,1)
            self.segments[idx].goto(new_x, new_y)
        # move head
        self.head.forward(self.MOVE_DISTANCE)
    
    # return the number of steps moved
    def set_head_angle(self, pos):
        x1, y1 = self.head.pos()
        x2, y2 = pos
        dy = y2 - y1
        dx = x2 - x1
        tan = math.atan2(dy, dx)
        angle = math.degrees(tan)
        self.head.setheading(angle)
        distance = math.sqrt(dx*dx + dy*dy)
        step = distance // self.MOVE_DISTANCE
        return int(step)

    def change_direction(self, dir_name):
        if dir_name in self.DIRECTIONS:
            self.direction = dir_name
            self.head.setheading(self.DIRECTIONS[self.direction])

    def up(self):
        self.change_direction("up")

    def down(self):
        self.change_direction("down")

    def left(self):
        self.change_direction("left")

    def right(self):
        self.change_direction("right")

    def grow(self):
        # add a new segment at the position of the last segment
        tail = self.segments[-1]
        new_seg = self._create_segment((tail.xcor(), tail.ycor()))
        opp_dir = self.opposites[self.direction]
        new_seg.setheading(opp_dir)
        new_seg.forward(self.MOVE_DISTANCE)
        self.segments.append(new_seg)
    
    def shrink(self):
        if len(self.segments) > 1:
            tail = self.segments.pop()
            tail.hideturtle()
            del tail
       
    def check_head_collision(self) -> bool:
        for seg in self.segments[1:]:
            if self.head.distance(seg) < 10:
                return True
        return False
       
if __name__ == "__main__":
    # Simple test of the Snake class
    screen = turtle.Screen()
    screen.setup(width=1000, height=1000)
    screen.title("Snake Test")
    screen.tracer(0)

    snake = Snake(length=5)
    screen.update()
    for _ in range(10):
        snake.move()
        screen.update()
        time.sleep(0.2)
    snake.up()
    for _ in range(10):
        snake.move()
        screen.update()
        time.sleep(0.2)
    
    for _ in range(5):
        snake.grow()
        screen.update()
        time.sleep(0.2)
    for _ in range(5):
        snake.shrink()
        screen.update()
        time.sleep(0.2)
    
    snake.reset()
    screen.update()
    steps = snake.set_head_angle((200, 200))
    for _ in range(steps):
        snake.move()
        screen.update()
        time.sleep(0.2)
    print(snake.head.pos())
    turtle.done()
