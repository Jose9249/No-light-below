import curses

class Game:
    def __init__(self, width: int, height: int, screen, player_x: int, player_y: int):
        self.width = width - 1
        self.height = height - 1
        self.screen = screen
        self.player_x = player_x
        self.player_y = player_y
        
        self.last_direction = ""
        self.blocks = set()

        self.create_world()

    def kill(self):
        self.__init__(1, 1, None, 0, 0)

    def create_world(self):
        if self.width > (curses.COLS - 1) or self.height > (curses.LINES - 1):
            exit()
            
        self.world = [[" " for i in range(self.width)] for j in range(self.height)]
        
        for x in range(self.width):
            self.world[0][x] = '#'
            self.world[self.height - 1][x] = '#'
        for y in range(self.height):
            self.world[y][0] = '#'
            self.world[y][self.width - 1] = '#'

    def draw_world(self):
        self.blocks = []
        for y, row in enumerate(self.world):
            for x, cell in enumerate(row):
                draw_y = y + 1  # desplazamiento vertical
                draw_x = x + 1  # desplazamiento horizontal

                if x == self.player_x and y == self.player_y:
                    self.screen.addch(draw_y, draw_x, '@')
                else:
                    self.screen.addch(draw_y, draw_x, cell)
                    if cell == "#":
                        self.blocks.append((y, x))
        self.screen.refresh()


    def place_block(self):
        if self.last_direction == "up":
            self.world[self.player_y - 1][self.player_x] = "#"
        elif self.last_direction == "down":
            self.world[self.player_y + 1][self.player_x] = "#"
        elif self.last_direction == "left":
            self.world[self.player_y][self.player_x - 1] = "#"
        elif self.last_direction == "right":
            self.world[self.player_y][self.player_x + 1] = "#"

    def break_block(self):
        if self.last_direction == "up":
            self.world[self.player_y - 1][self.player_x] = " "
        elif self.last_direction == "down":
            self.world[self.player_y + 1][self.player_x] = " "
        elif self.last_direction == "left":
            self.world[self.player_y][self.player_x - 1] = " "
        elif self.last_direction == "right":
            self.world[self.player_y][self.player_x + 1] = " "

    def move(self, direction: str):
        self.last_direction = f"{direction}"
        next_move = []
        collision = False

        if direction == "up":
            next_move = [self.player_y - 1, self.player_x]
        elif direction == "down":
            next_move = [self.player_y + 1, self.player_x]
        elif direction == "left":
            next_move = [self.player_y, self.player_x - 1]
        elif direction == "right":
            next_move = [self.player_y, self.player_x + 1]

        for block in self.blocks:
            if (block[0] == next_move[0]) and (block[1] == next_move[1]):
                collision = True
                break
            else:
                collision = False

        if not collision:
            match direction:
                case "up":
                    self.player_y -= 1
                case "down":
                    self.player_y += 1
                case "left":
                    self.player_x -= 1
                case "right":
                    self.player_x += 1
