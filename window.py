import cv2
import numpy as np
import time
from blend_images import blend_images

SPEED = 5
PAUSE = 112


class Window:

    def __init__(self, snake, res, speed=SPEED):
        self.width = snake.n_x * res
        self.height = snake.n_y * res
        self.res = res
        self.snake = snake
        self.window = np.zeros((self.height, self.width, 3), np.uint8)
        self.delay = int(1000/speed)

    def __draw_grid(self):
        for i in range(0, self.height, self.res):
            cv2.line(self.window, (0, i), (self.width, i), (50, 50, 50), 1)
        for i in range(0, self.width, self.res):
            cv2.line(self.window, (i, 0), (i, self.height), (50, 50, 50), 1)

    def __draw_snake(self, segment, isHead):
        if segment is not None:
            cv2.circle(self.window, (segment.x * self.res + self.res // 2, segment.y * self.res + self.res // 2),
                       self.res // 2, (0, 255, 0), -1)

            if isHead:
                eyes = np.zeros((self.res, self.res, 3), np.uint8)
                eyes.fill(255)
                cv2.circle(eyes, (self.res // 4, self.res // 4), self.res // 5, (245, 245, 245), -1)
                cv2.circle(eyes, (3 * self.res // 4, self.res // 4), self.res // 5, (245, 245, 245), -1)
                cv2.circle(eyes, (self.res // 4, self.res // 4), self.res // 6, (2, 2, 2), -1)
                cv2.circle(eyes, (3 * self.res // 4, self.res // 4), self.res // 6, (2, 2, 2), -1)
                if segment.vector == (1, 0): eyes = cv2.rotate(eyes, cv2.ROTATE_180)
                elif segment.vector == (0, 1): eyes = cv2.rotate(eyes, cv2.ROTATE_90_CLOCKWISE)
                elif segment.vector == (0, -1): eyes = cv2.rotate(eyes, cv2.ROTATE_90_COUNTERCLOCKWISE)
                self.window = blend_images(self.window, eyes, (segment.y * self.res, segment.x * self.res), 1, 1)
                cv2.imshow("eyes", eyes)
            else:
                cv2.circle(self.window, (segment.x * self.res + self.res // 2, segment.y * self.res + self.res // 2),
                           self.res // 3, (0, 100, 0), -1)
            self.__draw_snake(segment.previous, False)

    def __draw_apples(self):
        for apple in self.snake.apples:
            cv2.circle(self.window, (apple.x * self.res + self.res // 2, apple.y * self.res + self.res // 2),
                       self.res // 3, (0, 0, 255), -1)
            cv2.circle(self.window, (apple.x * self.res + self.res // 2, apple.y * self.res + self.res // 4),
                       self.res // 6, (0, 150, 0), -1)

    def __draw_score(self):
        cv2.putText(self.window, str(self.snake.score), (self.width // 2, 2*self.res), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (0, 0, 150), 2)

    def __wait_delay(self):
        initial_time = time.time()
        k = cv2.waitKey(self.delay)
        final_time = time.time() - initial_time

        if final_time < self.delay * 0.001:
            time.sleep(self.delay * 0.001 - final_time)
        return k

    def start(self):

        while True:
            self.window = np.zeros((self.height, self.width, 3), np.uint8)
            self.snake.play()
            self.__draw_snake(self.snake.head, True)
            self.__draw_score()
            self.__draw_apples()
            self.__draw_grid()

            if self.snake.collision(self.snake.head, self.snake.head.previous):
                break

            cv2.imshow("Snake", self.window)
            k = self.__wait_delay()

            if k == PAUSE:
                cv2.waitKey(0)
            else:
                self.snake.rotate_head(k)

        cv2.putText(self.window, "GAME OVER", (self.width//4, self.height//2), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Snake", self.window)

        cv2.waitKey(0)


