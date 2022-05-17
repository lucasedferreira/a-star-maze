import numpy as np
from collections import defaultdict
import os
import time

WALKABLE = ['.', 'C', 'E']
START = "S"
END = "E"


def solve(file):
  maze = parse_maze(file)
  start = get_position(maze, START)
  end = get_position(maze, END)

  graph = build_graph(maze, start)
  path = find_shortest_path(graph, np.array2string(start), np.array2string(end))
  print_solution(maze, path)


def build_graph(maze, start):
  graph = defaultdict(list)
  set_paths(graph, start, maze, visited=[])
  return graph

def set_paths(graph, position, maze, visited):
  neighbours = get_available_paths(position, maze)
  for neighbour in neighbours:
    string_position = np.array2string(position)
    string_neighbour = np.array2string(neighbour)

    if(string_neighbour not in visited):
      graph[string_position].append(string_neighbour)
      graph[string_neighbour].append(string_position)

      visited = np.append(visited, string_neighbour)
      set_paths(graph, neighbour, maze, visited)

  return graph

def get_available_paths(position, maze):
  available_neighbours = np.empty((0, 2), int)

  neighbours = get_neightbours(position, maze)
  for neighbour in neighbours:
    if neighbour.any() and maze[neighbour[0], neighbour[1]] in WALKABLE:
      available_neighbours = np.append(available_neighbours, [neighbour], axis=0)

  return available_neighbours

def get_neightbours(position, maze):
  [line, column] = position
  up = right = down = left = np.array([])

  if line > 0:
    up = np.array([line-1, column])

  columns_length = len(maze[0])
  if column < columns_length:
    right = np.array([line, column+1])

  lines_length = len(maze)
  if line < lines_length:
    down = np.array([line+1, column])

  if column > 0:
    left = np.array([line, column-1])

  return [up, right, down, left]

def parse_maze(file):
  lines = file.read().splitlines()
  linesAndColumns = map(lambda line: list(line), lines)
  mazeInArray = np.array(list(linesAndColumns))
  return mazeInArray

def get_position(maze, string):
  found_positions = np.argwhere(maze == string)

  if(len(found_positions) == 0):
    raise Exception("No provided {}".format(string))

  if(len(found_positions) > 1):
    raise Exception("More than one {} was provided".format(string))

  return found_positions[0]

def find_shortest_path(graph, start, goal):
  explored = []
  queue = [[start]]

  if start == goal:
    raise Exception("Same node")

  while queue:
    path = queue.pop(0)
    node = path[-1]

    if node not in explored:
      neighbours = graph[node]

      for neighbour in neighbours:
        new_path = list(path)
        new_path.append(neighbour)
        queue.append(new_path)

        if neighbour == goal:
          return new_path
      explored.append(node)

  raise Exception("There's no connecting path")

def print_solution(maze, path):
  update_maze(maze)

  for index, currentPosition in enumerate(path):
    belch = False

    if(index > 0):
      previousPosition = np.fromstring(path[index-1][1:-1], dtype=int, sep=' ')
      maze[previousPosition[0], previousPosition[1]] = '▓'

    currentPosition = np.fromstring(currentPosition[1:-1], dtype=int, sep=' ')
    if(maze[currentPosition[0], currentPosition[1]] == 'C'):
      belch = True
    maze[currentPosition[0], currentPosition[1]] = 'ö'

    update_maze(maze)

    sleep = .3
    if(belch):
      print("*som de arroto*")
      sleep = 3
    time.sleep(sleep)

def update_maze(maze):
  clear = lambda: os.system('clear')
  clear()
  print('\n'.join([''.join(['{}'.format(item) for item in row]) for row in maze]))


if __name__ == "__main__":
  file = open("maze-2.txt", "r")
  solve(file)
  print(file.read())
