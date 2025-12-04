# Turtle 贪吃蛇 (Snake) — Python

麦子小朋友喜欢玩贪吃蛇，战绩也不错。 大姨说，要不我们自己做一条蛇吧

这是一个使用 `turtle` 实现的贪吃蛇游戏，只有一条蛇，撞墙就game over

先用copilot 生成了一个草稿，接着在上面加功能，改代码


文件简介：

- `snake.py`: 包含 `Snake` 类，管理蛇的size、移动、增长与碰撞检测。
- `food.py`: `Food` 类，负责生成食物位置。
- `game.py`: 游戏主循环、配置读取与键盘事件绑定（运行入口）。
- `plan.py` : 负责snake行走的路线，找食物的方式
- `config.ini`: 可配置的屏幕大小、颜色和速度。
- `requirements.txt`: 记录依赖（turtle 为 Python 标准库，无需 pip 安装）。

