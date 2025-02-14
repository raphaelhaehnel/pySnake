# PySnake

Implementation of the basic game "Snake" in Python.
Libraries used for the implementation:
- `OpenCV`: For drawing the game elements
- `Numpy`: Computations for the graphic interface
- `Playsound`: For the sound effects

## Usage
Run the file `main.py`.
1) Choose the game dimensions x, y by modifying the line `snake = Snake(x, y, 3)`
1) Choose the snake starting size s by modifying the line `snake = Snake(15, 15, s)`
2) Choose the window dimension `res` by modifying the line `myWindow = Window(snake, res=20, speed=8)`
2) Choose the snake speed `speed` by modifying the line `myWindow = Window(snake, res=20, speed=8)`

## Environment
- Operating system: Windows 10/11
- Python version: 3.10.5

## Files explanation
- `main.py`: Runs the application
- `snake.py`: Class representing the game
- `window.py`: Class representing the graphic interface
- `blend_images.py`: Helper function for drawing the snake

 ## Game screenshots
 
![snapshot](https://user-images.githubusercontent.com/69756617/205866905-6cc1a561-7e55-4888-9d7c-f5a802dc5bb9.PNG)

![snapshot2](https://github.com/user-attachments/assets/f64462c9-9238-4f2a-8435-aefdd404d453)
