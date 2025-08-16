from tkinter import *
from random import randint
#-----------------------------
class Snake:
    def __init__(self):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.square = []
        
        for i in range(0, BODY_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.square.append(square)

class Food:
    def __init__(self):
        x = randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]
    
    if direction == "up":
        y -= SPACE_SIZE

    elif direction == "down":
        y += SPACE_SIZE
    
    elif direction == "left":
        x -= SPACE_SIZE

    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.square.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score:{score}")
        canvas.delete("food")
        food = Food()
    
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.square[-1])
        del snake.square[-1]


    if check_game_over(snake):
        game_over()
    
    else:
        window.after(SLOWNESS, next_turn, snake, food)


def change_direction(new_dir):
    global direction

    if new_dir == "left":
        if direction != "right":
            direction = new_dir

    elif new_dir == "right":
        if direction != "left":
            direction = new_dir

    elif new_dir == "up":
        if direction != "down":
            direction = new_dir

    elif new_dir == "down":
        if direction != "up":
            direction = new_dir

def check_game_over(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x > GAME_WIDTH:
        return True
    
    if y < 0 or y > GAME_HEIGHT:
        return True
    
    for sq in snake.coordinates[1:]:
        if x == sq[0] and y == sq[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=("Terminal", 30),
                       text="GAME OVER!", fill="red", tag="gameover")

def restart_program():
    global score, direction, snake, food
    canvas.delete(ALL)
    score = 0
    direction = "down"
    label.config(text=f"Score:{score}")
    snake = Snake()
    food = Food()
    next_turn(snake, food)

#-----------------------------
GAME_WIDTH = 500
GAME_HEIGHT = 500
SPACE_SIZE = 50
SLOWNESS = 200
BODY_SIZE = 2
SNAKE_COLOR = "blue"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"
score = 0
direction = "down"
#-----------------------------
window = Tk()
window.title("Snake Game")
window.resizable(False,False)

label = Label(window, text=f"Score:{score}", font=("Roman", 30))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

restart = Button(window, text="RESTART", fg="red", command= restart_program)
restart.pack()

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()
