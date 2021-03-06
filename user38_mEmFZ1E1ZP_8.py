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
score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    # set random initial velocity of ball
    if direction == RIGHT:
        ball_vel = [random.randrange(2, 3), random.randrange(-2, -1)]
    elif direction == LEFT:
        ball_vel = [random.randrange(-3, -2), random.randrange(-2, -1)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    paddle1_pos = [0, HEIGHT / 2 - PAD_HEIGHT / 2]
    paddle2_pos = [(WIDTH - 1) - PAD_WIDTH, HEIGHT / 2 - PAD_HEIGHT / 2]
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
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # check whether the ball touches the paddles or the gutters
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH and ball_pos[1] >= paddle1_pos[1] and ball_pos[1] <= paddle1_pos[1] + PAD_HEIGHT:
        ball_vel[0] = - ball_vel[0] * 1.1 # reflect ball and increase speed by 10%
    elif ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS - PAD_WIDTH and ball_pos[1] >= paddle2_pos[1] and ball_pos[1] <= paddle2_pos[1] + PAD_HEIGHT:
        ball_vel[0] = - ball_vel[0] * 1.1 # reflect ball and increase speed by 10%
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        score2 += 1
        spawn_ball(RIGHT)
    elif ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS - PAD_WIDTH:
        score1 += 1
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
    # left paddle (paddle1)
    if paddle1_pos[1] + paddle1_vel[1] >= 0 and paddle1_pos[1] + paddle1_vel[1] <= HEIGHT - PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel[1]
    
        
    # right paddle (paddle2)
    if paddle2_pos[1] + paddle2_vel[1] >= 0 and paddle2_pos[1] + paddle2_vel[1] <= HEIGHT - PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel[1]
    
    
    # draw paddles
    # left paddle (paddle1)
    canvas.draw_polygon([paddle1_pos,
                         [paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1]],
                         [paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1] + PAD_HEIGHT],
                         [paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT]], 1, 'WHITE', "WHITE")
    
    # right paddle (paddle2)
    canvas.draw_polygon([paddle2_pos,
                         [paddle2_pos[0] + PAD_WIDTH, paddle2_pos[1]],
                         [paddle2_pos[0] + PAD_WIDTH, paddle2_pos[1] + PAD_HEIGHT],
                         [paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT]], 1, 'WHITE', "WHITE")
    
    # draw scores
    canvas.draw_text(str(score1), (150, 75), 50, "White")
    canvas.draw_text(str(score2), (450, 75), 50, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= 6
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += 6 
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= 6
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += 6

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0   
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 75)


# start frame
new_game()
frame.start()
