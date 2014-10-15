# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = [0, HEIGHT / 2 - PAD_HEIGHT / 2]
paddle2_pos = [(WIDTH - 1) - PAD_WIDTH, HEIGHT / 2 - PAD_HEIGHT / 2]
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]


# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    # set random initial velocity of ball
    if direction == RIGHT:
        ball_vel = [random.randrange(2, 5), random.randrange(-5, -1)]
    elif direction == LEFT:
        ball_vel = [random.randrange(-5, -2), random.randrange(-5, -1)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "Black")
    
    # check whether ball touches gutters
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        spawn_ball(RIGHT)
    elif ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS - PAD_WIDTH:
        spawn_ball(LEFT)
    
    # collide and reflect off walls
    if ball_pos[0] <= BALL_RADIUS:
        ball_vel[0] = - ball_vel[0]
    elif ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS:
        ball_vel[0] = - ball_vel[0]
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] -= paddle1_vel[1]
    
    
    # draw paddles
    # left paddle (paddle1)
    canvas.draw_polygon([paddle1_pos,
                         [paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1]],
                         [paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1] + PAD_HEIGHT],
                         [paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT]], 2, 'WHITE', "WHITE")
    
    # right paddle (paddle2)
    canvas.draw_polygon([paddle2_pos,
                         [paddle2_pos[0] + PAD_WIDTH, paddle2_pos[1]],
                         [paddle2_pos[0] + PAD_WIDTH, paddle2_pos[1] + PAD_HEIGHT],
                         [paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT]], 2, 'WHITE', "WHITE")
    
    # draw scores
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] += 1   

def keyup(key):
    global paddle1_vel, paddle2_vel


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
