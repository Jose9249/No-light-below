from menus import *
from game import Game
from inventario import Inventory
import curses
import pygame.mixer

opciones = ["New Game", "Continue", "Settings", "Licences", "Quit"]
opciones_index = 0
opciones_pausa = ["Resume", "Save", "Quit"]
opciones_pausa_index = 0
opciones_inventario_index = 0

inventory = Inventory()
inventory.add("sword", 1)
inventory.add("food", 5)

def main(screen) -> None:
    global opciones_index, opciones_pausa_index, opciones_inventario_index

    pygame.mixer.init()

    curses.cbreak() # Hace que al pulsar una tecla, el programa la registre inmediatamente en vez de esperar a que hagas enter.
    curses.noecho() # Hace que no se vean en pantalla las teclas que pulses
    curses.curs_set(0)
    curses.start_color()
    screen.keypad(True)  # Enable special keys (arrows, etc.)
    screen.timeout(100)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) # Inicializar el color con codigo 1, texto blanco y fondo negro
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    width = curses.COLS - 1
    height = curses.LINES - 1

    dibujar_menu(screen, width + 1, height + 1, opciones_index)

    seleccion = pygame.mixer.Sound("audio/seleccion.mp3")
    seleccion.set_volume(1)
    pause = pygame.mixer.Sound("audio/pause.mp3")
    pause.set_volume(1)
    unpause = pygame.mixer.Sound("audio/unpause.mp3")
    unpause.set_volume(1)

    # Ventanas (0:Menu 1:Juego 2:Juego Pausado 3:Menu de mundos)
    menu_index = 0

    run = True
    while run:
        screen.border(0)
        screen.refresh()
        curses.napms(5) # Espera en milisegundos

        key = screen.getch() # Espera a que presiones una tecla
        if menu_index == 0:
            if key == 10 or key == 13: # Enter
                seleccion.play()
                if opciones_index == 4:
                    run = False
                elif opciones_index == 0:
                    menu_index = 1
                    screen.clear()
                    game = Game(curses.COLS - 1, curses.LINES - 1, screen, 10 , 10)
                    game.draw_world()
            elif key == 9: # Tab
                seleccion.play()
                if opciones_index < 4:
                    opciones_index += 1
                else:
                    opciones_index = 0
                dibujar_menu(screen, width + 1, height + 1, opciones_index)
            elif key == curses.KEY_UP:
                seleccion.play()
                opciones_index -= 1
                if opciones_index < 0:
                    opciones_index = 4
                dibujar_menu(screen, width + 1, height + 1, opciones_index)
            elif key == curses.KEY_DOWN:
                seleccion.play()
                if opciones_index < 4:
                    opciones_index += 1
                else:
                    opciones_index = 0
                dibujar_menu(screen, width + 1, height + 1, opciones_index)

        elif menu_index == 1:
            if key == 27: # ESC
                pause.play()
                menu_index = 2
                dibujar_pausa(screen, width + 1, height + 1, opciones_pausa_index)

            elif key == ord("w") or key == ord("W"):
                game.move("up")
                screen.clear()
                game.draw_world()
            elif key == ord("s") or key == ord("S"):
                game.move("down")
                screen.clear()
                game.draw_world()
            elif key == ord("a") or key == ord("A"):
                game.move("left")
                screen.clear()
                game.draw_world()
            elif key == ord("d") or key == ord("D"):
                game.move("right")
                screen.clear()
                game.draw_world()
            elif key == ord("j") or key == ord("J"):
                game.place_block()
                screen.clear()
                game.draw_world()
            elif key == ord("k") or key == ord("K"):
                game.break_block()
                screen.clear()
                game.draw_world()
            elif key == ord("e") or key == ord("E"):
                dibujar_inventario(screen, game, inventory.get_item_list(), inventory, seleccion, opciones_inventario_index)
                screen.clear()
                game.draw_world()

        elif menu_index == 2:
            if key == 27: # ESC
                unpause.play()
                menu_index = 1
                screen.clear()
                game.draw_world()
                screen.refresh()
            elif key == 10 or key == 13: # Enter
                if opciones_pausa_index == 2:
                    seleccion.play()
                    menu_index = 0
                    opciones_pausa_index = 0
                    opciones_index = 0
                    dibujar_menu(screen, width + 1, height + 1, opciones_index)
                elif opciones_pausa_index == 0:
                    unpause.play()
                    menu_index = 1
                    screen.clear()
                    game.draw_world()
                    screen.refresh()
            elif key == 9: # Tab
                seleccion.play()
                if opciones_pausa_index < 2:
                    opciones_pausa_index += 1
                else:
                    opciones_pausa_index = 0
                dibujar_pausa(screen, width + 1, height + 1, opciones_pausa_index)
            elif key == curses.KEY_UP:
                seleccion.play()
                opciones_pausa_index -= 1
                if opciones_pausa_index < 0:
                    opciones_pausa_index = 2
                dibujar_pausa(screen, width + 1, height + 1, opciones_pausa_index)
            elif key == curses.KEY_DOWN:
                seleccion.play()
                if opciones_pausa_index < 2:
                    opciones_pausa_index += 1
                else:
                    opciones_pausa_index = 0
                dibujar_pausa(screen, width + 1, height + 1, opciones_pausa_index)

    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin() # Restores the terminal to its original operating mode.

if __name__ == "__main__":
    curses.wrapper(main)
