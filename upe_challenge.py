import requests
import time

def outOfBounds(x, y, maze_size):
	if x < 0 or y < 0 or x >= maze_size[0] or y >= maze_size[1]:
		return True
	return False

def dfs(row, col, maze_size, EXPLORED, PATHS, token_url):

	# check surrounding location
	deadend1 = False
	deadend2 = False
	deadend3 = False
	deadend4 = False
 
	EXPLORED.append([row, col])

	#DOWN ########################################
	if [row, col + 1] in EXPLORED or outOfBounds(row, col + 1, maze_size):
		deadend4 = True
	else:
		neighbor_info = requests.post(token_url, data={"action": "DOWN"}).json()["result"]
		if neighbor_info == "SUCCESS":
			PATHS.append("UP")
			return dfs(row, col + 1, maze_size, EXPLORED, PATHS, token_url)
		elif neighbor_info == "END":
			return True
		else:
			deadend4 = True

	#RIGHT ########################################

	if [row + 1, col] in EXPLORED or outOfBounds(row + 1, col, maze_size):
		deadend1 = True
	else:
		neighbor_info = requests.post(token_url, data={"action": "RIGHT"}).json()["result"]
		if neighbor_info == "SUCCESS":
			PATHS.append("LEFT")
			return dfs(row + 1, col, maze_size, EXPLORED, PATHS, token_url)
		elif neighbor_info == "END":
			return True
		else:
			deadend1 = True

	#UP ########################################
	if [row, col - 1] in EXPLORED or outOfBounds(row, col - 1, maze_size):
		deadend3 = True
	else:
		neighbor_info = requests.post(token_url, data={"action": "UP"}).json()["result"]
		if neighbor_info == "SUCCESS":
			PATHS.append("DOWN")
			return dfs(row, col - 1, maze_size, EXPLORED, PATHS, token_url)
		elif neighbor_info == "END":
			return True
		else:
			deadend3 = True

	#LEFT ########################################
	if [row - 1, col] in EXPLORED or outOfBounds(row - 1, col, maze_size):
		deadend2 = True
	else:
		neighbor_info = requests.post(token_url, data={"action": "LEFT"}).json()["result"]
		if neighbor_info == "SUCCESS":
			PATHS.append("RIGHT")
			return dfs(row - 1, col, maze_size, EXPLORED, PATHS, token_url)
		elif neighbor_info == "END":
			return True
		else:
			deadend2 = True

	# backtrack if deadend
	if deadend1 and deadend2 and deadend3 and deadend4:
		if PATHS:
			requests.post(token_url, data={"action": PATHS[-1]})

			if PATHS[-1] == "DOWN":
				return dfs(row, col+1, maze_size, EXPLORED, PATHS[:-1], token_url)

			elif PATHS[-1] == "UP":
				return dfs(row, col-1, maze_size, EXPLORED, PATHS[:-1], token_url)

			elif PATHS[-1] == "LEFT":
				return dfs(row-1, col, maze_size, EXPLORED, PATHS[:-1], token_url)

			elif PATHS[-1] == "RIGHT":
				return dfs(row+1, col, maze_size, EXPLORED, PATHS[:-1], token_url)

	return dfs(row, col, maze_size, EXPLORED, PATHS, token_url)


def main():
	base_url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com"

	# get token
	post_url = base_url + "/session"
	token = requests.post(post_url, data={"uid": "904581627"}).json()["token"] 
	token_url = base_url + "/game?token=" + token

	# go through levels
	for i in range(12):
		start = time.time()
		maze_info = requests.get(token_url)
		print maze_info.text
		cur_location = maze_info.json()["current_location"]
		maze_size = maze_info.json()["maze_size"]

		EXPLORED = []
		PATHS = []
		dfs(cur_location[0], cur_location[1], maze_size, EXPLORED, PATHS, token_url)
		print EXPLORED
		del EXPLORED[:]

		end = time.time()
		print (end - start)

	maze_info = requests.get(token_url)
	print maze_info.text


if __name__ == "__main__":
    main()







