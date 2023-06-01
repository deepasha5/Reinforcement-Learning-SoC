# Program in Python to create a Snake Game

from tkinter import *
import random
import numpy as np
import sys

# Initialising Dimensions of Game
WIDTH = 500
HEIGHT = 500
SPEED = 200
SPACE_SIZE = 20
BODY_SIZE = 2
SNAKE = "#00FF00"
FOOD = "#FFFFFF"
BACKGROUND = "#000000"

directions={
	0: "up",
	1: "right",
	2: "down",
	3: "left"
}

num_episodes = 3
total_actions = 4 # up:0, right:1, down:2, left:3
total_states = 4 #snake direction : up, right , down , left 
#rewards : eat apple =10 
#		 : comes close to apple  =1
#		 : goes away from apple  = -1
#		 : dies  = -100

target_policy =np.random.dirichlet(np.ones(total_actions), size=total_states )
behavior_policy = np.random.dirichlet(np.ones(total_actions), size=total_states) 
#print(behavior_policy)
value = np.random.rand(total_states, total_actions)
C = np.zeros((total_states, total_actions) , np.float64)

def algo(snake, food ):
	

	for i_episode in range(1, num_episodes+1):
		
		if i_episode % 1000 == 0:
			print("\rEpisode {}/{}.".format(i_episode, num_episodes), end="")
			sys.stdout.flush()

		episode = []
		state = np.random.choice(total_states)
		for t in range(100):
			
			probs = behavior_policy[state]
			action = np.random.choice(np.arange(len(probs)), p=probs)
			next_state = get_nextstate(state, action)
			reward= get_reward(next_state, snake, food)
			change_direction(directions[action])
			next_turn(snake, food)
			wait()
			episode.append((state, action, reward))
			
			state = next_state
        
		G = 0.0
		W = 1.0
		discount_factor= 1
		for t in range(len(episode))[::-1]:
			state, action, reward = episode[t]
			G = discount_factor * G + reward
			C[state][action] += W
			value[state][action] += (W / C[state][action]) * (G - value[state][action])
			# if action !=  np.argmax(target_policy(state)):
			# 	break
			W = W * target_policy[state][action]/behavior_policy[state][action]
			if W ==0:
				break
		#return value, target_policy
	
	print(target_policy)
	

def wait():
	
	count=0
	while(count !=10000000):
		count= count+1
	return	

def get_reward(nextstate, snake, food):
	x, y = snake.coordinates[0]
	if check_collisions(snake):
		return -100
	elif x == food.coordinates[0] and y == food.coordinates[1]:
		return 10
	elif(nextstate ==0 & x == food.coordinates[0] & food.coordinates[1]-y ==1 ):
		return 1
	elif(nextstate ==2 & x == food.coordinates[0] & food.coordinates[1]-y ==-1 ):
		return 1
	elif(nextstate ==1 & x -food.coordinates[0]==-1 & food.coordinates[1]==y ):
		return 1
	elif(nextstate ==3 & x -food.coordinates[0]== 1 & food.coordinates[1]==y ):
		return 1
	else :
		return -1
	
	


def get_nextstate(state, action):
    nextstate =0
    if action == 3:
        if state != 1:
            nextstate = action
    elif action == 1:
        if state != 3:
            nextstate = action
    elif action == 0:
        if state != 2:
            nextstate = action
    elif action == 2:
        if state != 0:
           nextstate = action
    return nextstate

# Class to design the snake
class Snake:

	def __init__(self):
		self.body_size = BODY_SIZE
		self.coordinates = []
		self.squares = []

		for i in range(0, BODY_SIZE):
			self.coordinates.append([0, 0])

		for x, y in self.coordinates:
			square = canvas.create_rectangle(
				x, y, x + SPACE_SIZE, y + SPACE_SIZE,
					fill=SNAKE, tag="snake")
			self.squares.append(square)

# Class to design the food
class Food:

	def __init__(self):

		x = random.randint(0,
				(WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
		y = random.randint(0,
				(HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

		self.coordinates = [x, y]

		canvas.create_oval(x, y, x + SPACE_SIZE, y +
						SPACE_SIZE, fill=FOOD, tag="food")

# Function to check the next move of snake
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

	snake.coordinates.insert(0, (x, y))

	square = canvas.create_rectangle(
		x, y, x + SPACE_SIZE,
				y + SPACE_SIZE, fill=SNAKE)

	snake.squares.insert(0, square)

	if x == food.coordinates[0] and y == food.coordinates[1]:

		global score

		score += 1

		label.config(text="Points:{}".format(score))

		canvas.delete("food")

		food = Food()

	else:

		del snake.coordinates[-1]

		canvas.delete(snake.squares[-1])

		del snake.squares[-1]

	if check_collisions(snake):
		game_over()

	else:
		window.after(SPEED, next_turn, snake, food)

# Function to control direction of snake
def change_direction(new_direction):

	global direction

	if new_direction == 'left':
		if direction != 'right':
			direction = new_direction
	elif new_direction == 'right':
		if direction != 'left':
			direction = new_direction
	elif new_direction == 'up':
		if direction != 'down':
			direction = new_direction
	elif new_direction == 'down':
		if direction != 'up':
			direction = new_direction

# function to check snake's collision and position
def check_collisions(snake):

	x, y = snake.coordinates[0]

	if x < 0 or x >= WIDTH:
		return True
	elif y < 0 or y >= HEIGHT:
		return True

	for body_part in snake.coordinates[1:]:
		if x == body_part[0] and y == body_part[1]:
			return True

	return False

# Function to control everything
def game_over():

	canvas.delete(ALL)
	canvas.create_text(canvas.winfo_width()/2,
					canvas.winfo_height()/2,
					font=('consolas', 70),
					text="GAME OVER", fill="red",
					tag="gameover")

# Giving title to the gaming window


window = Tk()
window.title("GFG Snake game ")


score = 0
direction = 'down'

# Display of Points Scored in Game

label = Label(window, text="Points:{}".format(score),
			font=('consolas', 20))
label.pack()

canvas = Canvas(window, bg=BACKGROUND,
				height=HEIGHT, width=WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# window.bind('<Left>',
# 			lambda event: change_direction('left'))
# window.bind('<Right>',
# 			lambda event: change_direction('right'))
# window.bind('<Up>',
# 			lambda event: change_direction('up'))
# window.bind('<Down>',
# 			lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)
algo(snake, food)

window.mainloop()



