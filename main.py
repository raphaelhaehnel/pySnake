from snake_new import Snake
from window import Window


if __name__ == '__main__':
    snake = Snake(15, 15)
    myWindow = Window(snake, 20)
    myWindow.start()
