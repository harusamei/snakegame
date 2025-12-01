import turtle
import time


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
    opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}

    def __init__(self, color="blue", length=3):
        self.color = color
        self.segments = []
        self._create_snake(length)
        self.head = self.segments[0]
        self.direction = "right"

    def _create_head(self, position):
        seg = turtle.Turtle("arrow")       # 蛇头是个上三角
        seg.color("green")
        seg.setheading(self.DIRECTIONS["right"])
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

    def _create_snake(self, length):
        self.segments.clear()
        starting_positions = (0, 0)
        self.segments.append(self._create_head(starting_positions))
        for i in range(length-1):
            pos = (-self.TURTLE_SIZE * self.Stretch_factor * (i+1), 0)
            self.segments.append(self._create_segment(pos))

    def move(self):
        # Move segments from tail to head
        for idx in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[idx - 1].xcor()
            new_y = self.segments[idx - 1].ycor()
            self.segments[idx].goto(new_x, new_y)
        # move head
        self.head.setheading(self.DIRECTIONS.get(self.direction, 0))
        self.head.forward(self.MOVE_DISTANCE)
        
    def change_direction(self, dir_name):
        if dir_name in self.DIRECTIONS:
            self.direction = dir_name

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
        self.segments.append(new_seg)
        
    def reset(self):
        # move segments off-screen and recreate
        
        for seg in self.segments:
            seg.goto(0,0)
            time.sleep(1)
        self.segments.clear()
        self._create_snake(3)
        self.head = self.segments[0]
        self.direction = "right"
        
    def check_self_collision(self) -> bool:
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
    time.sleep(2)
