import cv2
import numpy as np
import random
import time

VOID = 0
SNAKE = 1
APPLE = 2
STARTING_SIZE = 4

EN = 0
FR = 1

PAUSE = 112

UP = (119, 122)
DOWN = (115, 115)
LEFT = (97, 113)
RIGHT = (100, 100)


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
        self.apples = []
        self.head = Segment(self.n_y // 2, self.n_x // 2)
        self.__set_length(STARTING_SIZE)
        self.score = 0
        self.language = EN

    def __set_grid(self):
        for i in range(0, self.height, self.res):
            cv2.line(self.window, (0, i), (self.width, i), (50, 50, 50), 1)
        for i in range(0, self.width, self.res):
            cv2.line(self.window, (i, 0), (i, self.height), (50, 50, 50), 1)

    def __set_length(self, size):
        """ LOGIC FUNCTION

        :param size:
        :return:
        """
        for i in range(size-1):
            self.__grow(self.head)

    def __draw_snake(self, head):
        """ GRAPHIC FUNCTION
        :param head:
        :return:
        """
        if head is not None:
            cv2.circle(self.window, (head.x * self.res + self.res // 2, head.y * self.res + self.res // 2),
                       self.res // 2, (0, 255, 0), -1)
            cv2.circle(self.window, (head.x * self.res + self.res // 2, head.y * self.res + self.res // 2),
                       self.res // 3, (0, 100, 0), -1)
            self.__draw_snake(head.previous)

    def __draw_apples(self):
        """ GRAPHIC FUNCTION
        :return:
        """
        for apple in self.apples:
            cv2.circle(self.window, (apple.x * self.res + self.res // 2, apple.y * self.res + self.res // 2),
                       self.res // 3, (0, 0, 255), -1)
            cv2.circle(self.window, (apple.x * self.res + self.res // 2, apple.y * self.res + self.res // 4),
                       self.res // 6, (0, 150, 0), -1)

    def __draw_score(self):
        text = "Score: " + str(self.score)
        cv2.putText(self.window, text, (self.width // 2, self.height // 2), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (0, 0, 255), 2)

    def __snake_update(self, head):
        """ LOGIC FUNCTION
        :param head:
        :return:
        """
        if head is not None:
            head.y = (head.y + head.vector[0]) % self.n_y
            head.x = (head.x + head.vector[1]) % self.n_x
            self.__snake_update(head.previous)
            if head.previous is not None:
                if head.vector != head.previous.vector:
                    head.previous.vector = head.vector

    def __apple_update(self):
        """ LOGIC FUNCTION
        :return:
        """
        if len(self.apples) == 0:
            overlap = True
            x, y = (0, 0)
            while overlap:
                x = random.randint(0, self.n_x - 1)
                y = random.randint(0, self.n_y - 1)
                overlap = self.__apple_update_helper(x, y, self.head)
            self.apples.append(Apple(y, x))

    def __apple_update_helper(self, x, y, head):
        if head.x == x and head.y == y:
            print("OVERLAP")
            return True
        else:
            if head.previous is not None:
                return self.__apple_update_helper(x, y, head.previous)
            else:
                return False

    def __grow(self, head):
        """ LOGIC FUNCTION
        :param head:
        :return:
        """
        if head.previous is not None:
            self.__grow(head.previous)
        else:
            tail = Segment(head.y-head.vector[0], head.x-head.vector[1], head.vector)
            head.previous = tail

    def __eat(self, head):
        """ LOGIC FUNCTION
        :param head:
        :return:
        """
        for apple in self.apples:
            if apple.x == head.x and apple.y == head.y:
                self.__grow(head)
                self.apples.remove(apple)
                self.score += 1

    def __collision(self, head, segment):
        """ LOGIC FUNCTION
        :param head:
        :param segment:
        :return:
        """
        if segment:
            if head.x == segment.x and head.y == segment.y:
                return True
            else:
                return self.__collision(head, segment.previous)
        return False

    def start(self):

        while True:
            self.window = np.zeros((self.n_y * self.res, self.n_x * self.res, 3), np.uint8)
            self.__snake_update(self.head)
            self.__eat(self.head)
            self.__apple_update()
            self.__draw_score()
            self.__draw_snake(self.head)
            self.__draw_apples()
            self.__set_grid()

            if self.__collision(self.head, self.head.previous):
                break

            cv2.imshow("Snake", self.window)

            k = cv2.waitKey(200)
            if k == -1:
                continue
            elif k == PAUSE:
                cv2.waitKey(0)
            elif k == UP[self.language]:
                if self.head.vector != (1, 0):
                    self.head.vector = (-1, 0)
            elif k == DOWN[self.language]:
                if self.head.vector != (-1, 0):
                    self.head.vector = (1, 0)
            elif k == LEFT[self.language]:
                if self.head.vector != (0, 1):
                    self.head.vector = (0, -1)
            elif k == RIGHT[self.language]:
                if self.head.vector != (0, -1):
                    self.head.vector = (0, 1)

        print("hey")
        cv2.putText(self.window, "GAME OVER", (self.width//2, self.height//2), cv2.FONT_HERSHEY_COMPLEX, 20, (0, 0, 255), 4)
        # TODO text of the Game Over doesn't work

        cv2.waitKey(2000)


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
