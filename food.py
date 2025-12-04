import turtle
import random
import time


class Food:
    """Food item for the snake to eat. Randomly placed."""
    DURATIONS = {'fastest': 4, 'short': 8, 'medium': 16, 'long': 32,'forever': -1}

    def __init__(self, x_bound=400, y_bound=300, color="red", expiration="fastest"):

        self.beans = []
        self.color = color
        self.timespan = self.DURATIONS['fastest']
        if expiration in self.DURATIONS:
            self.timespan = self.DURATIONS[expiration]
        
        self.x_bound = x_bound
        self.y_bound = y_bound

    def refresh(self, num=1):
        for _ in range(num):
            bean = turtle.Turtle("circle")
            bean.color(self.color)
            x = random.randint(-self.x_bound // 20, self.x_bound // 20) * 20
            y = random.randint(-self.y_bound // 20, self.y_bound // 20) * 20
            print(f"Placing food at: ({x}, {y})")
            bean.penup()
            bean.goto(x, y)
            self.beans.append((bean, time.time()))
        
    def update(self):
        # forever
        if self.timespan < 0:
            return
        
        current_time = time.time()
        before = -1

        for idx in range(0, len(self.beans), 1):
            bean, t = self.beans[idx]
            if current_time - t > self.timespan:
                before = idx
            else:
                break
        # remove expired beans
        removes =[]
        for idx in range(before + 1):
            bean, t = self.beans[idx]
            flag = random.random()
            if flag < 0.5:
                bean.hideturtle()
                del bean
                removes.append(idx)
        self.beans = [b for i, b in enumerate(self.beans) if i not in removes]

    def clear(self):
        for bean, t in self.beans:
            bean.hideturtle()
            bean.clear()
            del bean
        self.beans.clear()

if __name__ == "__main__":
    screen = turtle.Screen()
    screen.setup(width=600, height=600)
    screen.tracer(0)
    food = Food(x_bound=screen.window_width()//2 -20, y_bound=screen.window_height()//2 -20)
    for _ in range(5):
        food.refresh(5)
        time.sleep(1)
        food.update()
        screen.update()
    
    turtle.done()