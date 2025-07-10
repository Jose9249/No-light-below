from pyfiglet import figlet_format
import curses.textpad
import curses

def dibujar_menu(screen, width, height, opciones_index) -> None:
    screen.clear()
    text = figlet_format("No Light Below")
    lines = text.splitlines()

    rect_height = 14
    rect_width = 15

    top = (height - rect_height) // 2
    left = (width - rect_width) // 2
    bottom = top + rect_height
    right = left + rect_width

    start_y = 4
    for i, line in enumerate(lines):
        start_x = (width - len(line)) // 2
        screen.addstr(start_y + i, start_x - 3, line, curses.color_pair(2))

    screen.addstr(1, 2, "Use arrow keys to pick, 'enter' to select.")
    screen.addstr(8, start_x + 65, "v0.0.1")
    screen.addstr(11, (width - len("By Firewall Games")) // 2, "By Firewall Games")

    curses.textpad.rectangle(screen, top, left, bottom, right)
    screen.addstr(top + 3, (width - len("New Game") - 2) // 2, "  New Game  ", curses.A_REVERSE if opciones_index == 0 else 0)
    screen.addstr(top + 5, (width - len("Continue") - 2) // 2, "  Continue  ", curses.A_REVERSE if opciones_index == 1 else 0)
    screen.addstr(top + 7, (width - len("Settings") - 2) // 2, "  Settings  ", curses.A_REVERSE if opciones_index == 2 else 0)
    screen.addstr(top + 9, (width - len("Licenses") - 2) // 2, "  Licenses  ", curses.A_REVERSE if opciones_index == 3 else 0)
    screen.addstr(top + 11, (width - len("    Quit    ") + 1) // 2, "    Quit    ", curses.A_REVERSE if opciones_index == 4 else 0)

    screen.addstr(height - 4, (width - len("© 2025 No Light Below.")) // 2, "© 2025 No Light Below.")
    screen.addstr(height - 3, (width - len("All Rights Reserved")) // 2, "All Rights Reserved")

    screen.refresh()
    
def dibujar_pausa(screen, width, height, opciones_pausa_index) -> None:
    screen.clear()

    rect_height = 10
    rect_width = 13

    top = (height - rect_height) // 2
    left = (width - rect_width) // 2
    bottom = top + rect_height
    right = left + rect_width

    screen.addstr(1, 2, "Use arrow keys to pick, 'enter' to select.")

    screen.addstr(top - 3, (width - len("PAUSE")) // 2, "PAUSE", curses.A_UNDERLINE)

    curses.textpad.rectangle(screen, top, left, bottom, right)
    screen.addstr(top + 3, (width - len("  Resume  ") + 1) // 2, "  Resume  ", curses.A_REVERSE if opciones_pausa_index == 0 else 0)
    screen.addstr(top + 5, (width - len("   Save   ") + 1) // 2, "   Save   ", curses.A_REVERSE if opciones_pausa_index == 1 else 0)
    screen.addstr(top + 7, (width - len("   Quit   ") + 1) // 2, "   Quit   ", curses.A_REVERSE if opciones_pausa_index == 2 else 0)

    screen.refresh()

def dibujar_inventario(screen, game, items, inventory, seleccion, opciones_inventario_index) -> None:
    screen.bkgd(" ", curses.color_pair(3))
    screen.clear()

    screen_height, screen_width = screen.getmaxyx()

    screen.refresh()

    window_height = len(items) * 2 + 3
    window_width = max(len(item) for item in items) + 6
    window_start_y = (screen_height - window_height) // 2
    window_start_x = (screen_width - window_width) // 2

    screen.border(0)
    game.draw_world()

    screen.addstr(window_start_y - 3, window_start_x + (window_width - len("Inventario")) // 2, "Inventario", curses.color_pair(3) | curses.A_UNDERLINE)

    run = True
    while run:
        inventory_screen = curses.newwin(window_height, window_width, window_start_y, window_start_x)
        inventory_screen.bkgd(" ", curses.color_pair(3))
        inventory_screen.attron(curses.color_pair(4))
        inventory_screen.box()
        inventory_screen.attroff(curses.color_pair(4))

        for i, item in enumerate(items):
            y = 2 + i * 2  # salto de línea entre items
            if i == opciones_inventario_index:
                inventory_screen.addstr(y, 2, item, curses.color_pair(3) | curses.A_REVERSE)
            else:
                inventory_screen.addstr(y, 2, item, curses.color_pair(3))

        inventory_screen.refresh()

        key = screen.getch()
        if key == 27:  # ESC
            run = False        
        elif key == 9:  # TAB
            seleccion.play()
            if opciones_inventario_index < len(items) - 1:
                opciones_inventario_index += 1
            else:
                opciones_inventario_index = 0
            items = inventory.get_item_list()

        elif key == curses.KEY_UP:
            seleccion.play()
            opciones_inventario_index -= 1
            if opciones_inventario_index < 0:
                opciones_inventario_index = len(items) - 1

        elif key == curses.KEY_DOWN:
            seleccion.play()
            if opciones_inventario_index < len(items) - 1:
                opciones_inventario_index += 1
            else:
                opciones_inventario_index = 0
