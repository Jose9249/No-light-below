import curses
import random
import math
from collections import namedtuple

# 📐 Estructuras básicas
Point = namedtuple('Point', ['x', 'y'])

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersects(self, other):
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)

# 🎯 Constantes de dungeon
NUMBER_OF_POINTS = 10000
ROOM_MAX_SIZE = 20
ROOM_MIN_SIZE = 10
ROOM_MIN_DISTANCE = 2

# 💾 Listas globales
points = []
tree = []
rooms = []

# 🧱 Dibujo de la dungeon
def draw_dungeon(stdscr, width, height):
    stdscr.clear()

    xs = set()
    ys = set()
    points.clear()
    tree.clear()
    rooms.clear()

    for _ in range(NUMBER_OF_POINTS):
        margin = ROOM_MAX_SIZE + ROOM_MIN_DISTANCE + 2
        x = random.randint(margin, width - margin - 1)
        y = random.randint(margin, height - margin - 1)

        p = Point(x, y)

        w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)

        ra = Rectangle(p.x - w // 2, p.y - h // 2, w, h)

        if any(ra.intersects(rb) for rb in rooms):
            continue

        ra.x += ROOM_MIN_DISTANCE
        ra.y += ROOM_MIN_DISTANCE
        ra.width -= 2 * ROOM_MIN_DISTANCE
        ra.height -= 2 * ROOM_MIN_DISTANCE

        if (ra.x in xs or ra.x + ra.width // 2 in xs or ra.x + ra.width in xs or
            ra.y in ys or ra.y + ra.height // 2 in ys or ra.y + ra.height in ys):
            continue

        d = 0
        xs.update([ra.x + d, ra.x + ra.width // 2 + d, ra.x + ra.width + d])
        ys.update([ra.y + d, ra.y + ra.height // 2 + d, ra.y + ra.height + d])

        rooms.append(ra)
        points.append(p)

        for dx in range(ra.width):
            for dy in range(ra.height):
                try:
                    stdscr.addch(ra.y + dy, ra.x + dx, '#')
                except curses.error:
                    pass

    if points:
        tree.append(points.pop(0))

        while points:
            a, b = None, None
            min_distance = float('inf')

            for p1 in tree:
                for p2 in points:
                    dx = p2.x - p1.x
                    dy = p2.y - p1.y
                    dist = math.hypot(dx, dy)
                    if dist < min_distance:
                        min_distance = dist
                        a, b = p1, p2

            if a is None or b is None:
                raise RuntimeError("error ?")

            points.remove(b)
            tree.append(b)

            # Pasillos en L
            for y in range(min(a.y, b.y), max(a.y, b.y) + 1):
                try:
                    stdscr.addch(y, a.x, '+')
                except curses.error:
                    pass
            for x in range(min(a.x, b.x), max(a.x, b.x) + 1):
                try:
                    stdscr.addch(b.y, x, '+')
                except curses.error:
                    pass

    # Relleno de habitaciones
    for room in rooms:
        for dx in range(1, room.width - ROOM_MIN_DISTANCE // 2):
            for dy in range(1, room.height - ROOM_MIN_DISTANCE // 2):
                try:
                    stdscr.addch(room.y + dy, room.x + dx, '.')
                except curses.error:
                    pass

    stdscr.refresh()

# 🚪 Main loop de curses
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    height, width = stdscr.getmaxyx()
    draw_dungeon(stdscr, width, height)
    stdscr.addstr(0, 0, "PRESS ANY KEY TO REGEN | Q to QUIT")

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key != -1:
            draw_dungeon(stdscr, width, height)

# 🧠 Launch the madness
if __name__ == '__main__':
    curses.wrapper(main)
