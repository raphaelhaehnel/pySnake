import random
import threading
from playsound import playsound


SOUND_EAT = ['res/sound/eat_bite_apple_1.mp3',
             'res/sound/eat_bite_apple_2.mp3',
             'res/sound/eat_bite_apple_3.mp3']
SOUND_GAME_OVER = "res/sound/game-over-arcade.mp3"

EN = 0
FR = 1

""" Code of some key for an english and french keyboard"""
UP = (119, 122)
DOWN = (115, 115)
LEFT = (97, 113)
RIGHT = (100, 100)


class Snake:
    """ This class is representing the game logic, without any graphical interface
    """

    def __init__(self, n_y, n_x, starting_size):
        """ Initialize the parameters of the windows and the board game.
        The board is an easier representation of the window. It is made of squares, while the windows is the graphical
        representation of the board, and made of pixels
        :param n_y: The number of squares in y axis
        :param n_x: The number of squares in x axis
        :param res: The number of pixels taken by each square
        """
        self.n_x = n_x
        self.n_y = n_y
        self.apples = []
        self.head = Segment(self.n_y // 2, self.n_x // 2)
        self.__set_length(starting_size)
        self.score = 0
        self.language = EN

    def __set_length(self, size):
        """ Set the starting size of the snake
        :param size: The size of the snake
        :return: None
        """
        for i in range(size-1):
            self.__grow(self.head)

    def __snake_update(self, head):
        """ Advance and rotate (if necessary) each segment of the snake
        :param head: A segment object that represent the head of the snake
        :return: None
        """
        if head is not None:
            head.y = (head.y + head.vector[0]) % self.n_y
            head.x = (head.x + head.vector[1]) % self.n_x
            self.__snake_update(head.previous)
            if head.previous is not None:

                # Rotate the segment if necessary
                if head.vector != head.previous.vector:
                    head.previous.vector = head.vector

    def __apple_update(self):
        """ Generate a new apple when no apples exists on the board
        :return: None
        """
        if len(self.apples) == 0:
            overlap = True
            x, y = (0, 0)
            while overlap:
                x = random.randint(0, self.n_x - 1)
                y = random.randint(0, self.n_y - 1)

                # If the apple is overlapping with a segment, compute a new position for the apple
                overlap = self.__apple_update_helper(x, y, self.head)

            # Append the new apple in the list of apples
            self.apples.append(Apple(y, x))

    def __apple_update_helper(self, x, y, segment):
        """ Helper function for the __apple_update function. It calls of the segments of the snake recursively
        :param x: x position of the apple
        :param y: y position of the apple
        :param head: current segment of the snake
        :return: True if there is an overlap, False otherwise
        """
        if segment.x == x and segment.y == y:
            return True
        else:
            if segment.previous is not None:
                return self.__apple_update_helper(x, y, segment.previous)
            else:
                return False

    def __grow(self, head):
        """ Add a segment of the snake
        :param head: head of the snake
        :return: None
        """
        if head.previous is not None:
            self.__grow(head.previous)
        else:
            tail = Segment(head.y-head.vector[0], head.x-head.vector[1], head.vector)
            head.previous = tail

    def __eat(self):
        """ This function is called when the snake is running over an apple.
        :return:
        """
        for apple in self.apples:
            if apple.x == self.head.x and apple.y == self.head.y:
                self.__grow(self.head)
                self.apples.remove(apple)
                self.score += 1
                n = random.randint(0, len(SOUND_EAT)-1)

                # Run the function 'playsound' on a parallel thread
                threading.Thread(target=playsound, args=(SOUND_EAT[n],), daemon=True).start()

    def collision(self, head, segment):
        if segment:
            if head.x == segment.x and head.y == segment.y:
                threading.Thread(target=playsound, args=(SOUND_GAME_OVER,), daemon=True).start()
                return True
            else:
                return self.collision(head, segment.previous)
        return False

    def rotate_head(self, k):
        if k == UP[self.language]:
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

    def play(self):
        self.__snake_update(self.head)
        self.__eat()
        self.__apple_update()


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
