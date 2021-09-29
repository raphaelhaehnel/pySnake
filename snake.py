import cv2
import numpy as np
import random

VOID = 0
SNAKE = 1
APPLE = 2

PAUSE = 112
UP = 122
DOWN = 115
LEFT = 113
RIGHT = 100


class Snake:

    def __init__(self, n_y, n_x, res):
        """ Initialize the parameters of the windows and the board game.
        The board is an easier representation of the window. It is made of squares, while the windows is the graphical
        representation of the board, and made of pixels
        :param n_y: The number of squares in y axis
        :param n_x: The number of squares in x axis
        :param res: The number of pixels taken by each square
        """
        self.n_x = n_x
        self.n_y = n_y
        self.res = res
        self.width = n_x * res
        self.height = n_y * res
        self.window = np.zeros((n_y * res, n_x * res, 3), np.uint8)
        self.board = np.zeros((n_y, n_x))
        self.apples = []

    def __draw_snake(self, head):
        if head is not None:
            cv2.circle(self.window, (head.x * self.res + self.res // 2, head.y * self.res + self.res // 2),
                       self.res // 2, (0, 255, 0), -1)
            cv2.circle(self.window, (head.x * self.res + self.res // 2, head.y * self.res + self.res // 2),
                       self.res // 3, (0, 100, 0), -1)
            self.__draw_snake(head.previous)

    def __draw_apples(self):
        for apple in self.apples:
            cv2.circle(self.window, (apple.x * self.res + self.res // 2, apple.y * self.res + self.res // 2),
                       self.res // 3, (0, 0, 255), -1)
            cv2.circle(self.window, (apple.x * self.res + self.res // 2, apple.y * self.res + self.res // 4),
                       self.res // 6, (0, 150, 0), -1)

    def __snake_update(self, head):
        if head is not None:
            head.y = (head.y + head.vector[0]) % self.n_y
            head.x = (head.x + head.vector[1]) % self.n_x
            self.__snake_update(head.previous)
            if head.previous is not None:
                if head.vector != head.previous.vector:
                    head.previous.vector = head.vector

    def __apple_update(self):
        if len(self.apples) == 0:
            x = random.randint(0, self.n_x-1)
            y = random.randint(0, self.n_y-1)
            self.apples.append(Apple(y, x))
            print("Apple in position (", y, ", ", x, ")")

    def __grow(self, head):
        if head.previous is not None:
            self.__grow(head.previous)
        else:
            tail = Segment(head.y-head.vector[0], head.x-head.vector[1], head.vector)
            head.previous = tail

    def __eat(self, head):
        for apple in self.apples:
            if apple.x == head.x and apple.y == head.y:
                self.__grow(head)
                self.apples.remove(apple)

    def __collision(self, head, segment):
        if segment:
            if head.x == segment.x and head.y == segment.y:
                return True
            else:
                return self.__collision(head, segment.previous)
        return False

    def start(self):
        head = Segment(self.n_y//2, self.n_x//2)

        while True:
            self.window = np.zeros((self.n_y * self.res, self.n_x * self.res, 3), np.uint8)
            self.__eat(head)
            self.__apple_update()
            self.__draw_apples()
            self.__snake_update(head)
            self.__draw_snake(head)

            if self.__collision(head, head.previous):
                break

            cv2.imshow("Snake", self.window)

            k = cv2.waitKey(250)
            if k == -1:
                continue
            elif k == PAUSE:
                cv2.waitKey(0)
            elif k == UP:
                if head.vector != (1, 0):
                    head.vector = (-1, 0)
            elif k == DOWN:
                if head.vector != (-1, 0):
                    head.vector = (1, 0)
            elif k == LEFT:
                if head.vector != (0, 1):
                    head.vector = (0, -1)
            elif k == RIGHT:
                if head.vector != (0, -1):
                    head.vector = (0, 1)

        cv2.putText(self.window, "GAME OVER", (self.width//2, self.height//2), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 4)
        # TODO text of the Game Over doesn't work

        cv2.waitKey(0)


class Segment:

    def __init__(self, y, x, vector=(1, 0)):
        self.x = x
        self.y = y
        self.vector = vector
        self.previous = None


class Apple:

    def __init__(self, y, x):
        self.x = x
        self.y = y
