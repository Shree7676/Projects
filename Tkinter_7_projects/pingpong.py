import tkinter as tk
import random

WIDTH = 500
HEIGHT = 400

win = tk.Tk()
win.title("Ping Pong Game")

#create canvas
canvas = tk.Canvas(win, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()


# paddle dimensions
paddle_width = 100
paddle_height = 10
paddle_color = "white"

# ball dimensions
ball_radius = 10
ball_color = "red"

# create paddles
paddle_left = canvas.create_rectangle(0, 0, paddle_width, paddle_height, fill=paddle_color)
# paddle_right = canvas.create_rectangle(0, 0, paddle_width, paddle_height, fill=paddle_color)

# paddle_left = canvas.create_rectangle(0, HEIGHT - paddle_height, paddle_width, HEIGHT, fill=paddle_color)
paddle_right = canvas.create_rectangle(WIDTH - paddle_width, HEIGHT - paddle_height, WIDTH, HEIGHT, fill=paddle_color)
# create ball
ball = canvas.create_oval(0, 0, ball_radius*2, ball_radius*2, fill=ball_color)

# function to move the paddles
def move_paddles(event):
    if event.keysym == "Left":
        canvas.move(paddle_left, -20, 0)
    elif event.keysym == "Right":
        canvas.move(paddle_left, 20, 0)
    elif event.keysym == "a":
        canvas.move(paddle_right, -20, 0)
    elif event.keysym == "d":
        canvas.move(paddle_right, 20, 0)

# function to move the ball
def move_ball():
    global ball_speed_x, ball_speed_y
    
    # get the current position of the ball
    x1, y1, x2, y2 = canvas.coords(ball)
    
    # check if the ball hits the paddle
    if y2 >= HEIGHT - paddle_height and y2 <= HEIGHT and ball_speed_y > 0:
        # check if the ball hits the left paddle
        if x2 >= canvas.coords(paddle_left)[0] and x1 <= canvas.coords(paddle_left)[2]:
            ball_speed_y = -ball_speed_y
        # check if the ball hits the right paddle
        elif x2 >= canvas.coords(paddle_right)[0] and x1 <= canvas.coords(paddle_right)[2]:
            ball_speed_y = -ball_speed_y
    
    # check if the ball hits the wall
    if x1 <= 0 or x2 >= WIDTH:
        ball_speed_x = -ball_speed_x
    if y1 <= 0:
        ball_speed_y = -ball_speed_y
    
    # move the ball
    canvas.move(ball, ball_speed_x, ball_speed_y)
    
    # call the function again after a short delay
    win.after(50, move_ball)


# bind movement of the paddles to keyboard events
win.bind("<Left>", move_paddles)
win.bind("<Right>", move_paddles)
win.bind("<a>", move_paddles)
win.bind("<d>", move_paddles)

# start moving the ball
ball_speed_x = 5
ball_speed_y = 5
move_ball()

# start the game loop
win.mainloop()
