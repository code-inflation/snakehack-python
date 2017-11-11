import bottle
import os
import random
from enum import Enum

class Status(Enum):
    EMPTY = 0
    SNAKE = 1
    PSNAKE = 2
    FOOD = 9

def print_grid(grid):
    for row in grid:
        print([cell.value for cell in row])


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'snakehack-python'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # generate empty grid
    grid = [[Status.EMPTY for _ in range(data['width'])] for _ in range(data['height'])]
    #print_grid(grid)

    # fill grid
    for snake in data['snakes']:
        for coords in snake['coords']:
            #print(coords[0])
            #print(coords[1])
            grid[coords[1]][coords[0]] = Status.SNAKE

            snake_head = coords[0]



    for food in data['food']:
        print(food[0])
        print(food[1])
        grid[food[1]][food[0]] = Status.FOOD


    print_grid(grid)

    directions = ['up', 'down', 'left', 'right']

    return {
        'move': 'up',
        'taunt': 'snakehack-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
