from snake import Snake
from window import Window


if __name__ == '__main__':
    snake = Snake(15, 15, 3)
    myWindow = Window(snake, res=20, speed=8)
    myWindow.start()
