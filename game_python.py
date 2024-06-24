import pygame
import sys
import time
from dfs_solver import DFSSolver

pygame.init()

# Parámetros de la pantalla
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Juego de Tablero')

# Variables de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)  # Color gris

# Tamaño de cada celda
cell_size = 50

# Diccionario para almacenar elementos del tablero y sus propiedades
elements = {}
selected_element = None

def read_level_from_txt(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    rows = len(lines)
    cols = len(lines[0].strip())
    elements.clear()

    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char == '.':
                continue
            create_element(char, x, y)

    return rows, cols

def create_element(letter, x, y):
    if letter not in elements:
        elements[letter] = []
    elements[letter].append((x, y))

def determine_orientation(element):
    positions = element
    if len(positions) == 1:
        return 'obstacle'
    elif len(set(x for x, y in positions)) == 1:
        return 'vertical'
    else:
        return 'horizontal'

def get_game_state():
    state = {
        'A': elements["A"],
        'goal': elements.get('0', []),
        'obstacles': {k: v[:] for k, v in elements.items() if k not in ('A', '0')}
    }
    return state

def get_obstacle_at_position(position):
    x, y = position
    for letter, positions in elements.items():
        if letter not in ('A', '0'):
            if (x, y) in positions:
                return letter
    return None

def is_position_free(x, y, exclude_letter=None):
    for letter, positions in elements.items():
        if letter != exclude_letter:
            if (x, y) in positions:
                return False
    return True

def move_obstacle_until_free(obstacle_letter, new_pos, rows, cols):
    positions = elements[obstacle_letter]
    orientation = determine_orientation(positions)

    while not is_position_free(*new_pos, exclude_letter='A'):
        moved = False
        for x, y in positions:
            if orientation == 'vertical':
                possible_moves = [(x, y - 1), (x, y + 1)]
            elif orientation == 'horizontal':
                possible_moves = [(x - 1, y), (x + 1, y)]

            for move in possible_moves:
                if is_position_free(*move, exclude_letter=obstacle_letter):
                    elements[obstacle_letter].remove((x, y))
                    elements[obstacle_letter].append(move)
                    moved = True
                    break
            if moved:
                break

        if not moved:
            return False  # No se pudo mover el obstáculo

    return True  # Obstáculo movido exitosamente

def move_element(letter, key, rows, cols):
    if letter not in elements:
        return False

    positions = elements[letter]
    orientation = determine_orientation(positions)
    new_positions = []

    for x, y in positions:
        if orientation == 'vertical':
            if key == "UP":
                new_pos = (x, y - 1)
            elif key == "DOWN":
                new_pos = (x, y + 1)
            else:
                continue
        elif orientation == 'horizontal':
            if key == "LEFT":
                new_pos = (x - 1, y)
            elif key == "RIGHT":
                new_pos = (x + 1, y)
            else:
                continue

        if isinstance(new_pos, tuple):
            if new_pos[0] < 0 or new_pos[0] >= cols or new_pos[1] < 0 or new_pos[1] >= rows:
                return False  # Movimiento fuera de los límites del tablero

            if not is_position_free(*new_pos, exclude_letter=letter):
                if letter == 'A':
                    obstacle_letter = get_obstacle_at_position(new_pos)
                    if obstacle_letter:
                        if not move_obstacle_until_free(obstacle_letter, new_pos, rows, cols):
                            return False  # No se pudo mover el obstáculo

            new_positions.append(new_pos)

    if len(new_positions) == len(positions):
        elements[letter] = new_positions
        return True

    return False

def move_along_path(path, rows, cols):
    for direction, position in path:
        if direction:
            success = move_element('A', direction, rows, cols)
            if not success:
                print(f"Failed to move 'A' {direction} to {position}")
                break
            print(f"Moving 'A' {direction} to {position}")
            print(f"Current game state: {elements}")
            time.sleep(0.5)  # Delay para ver el movimiento en la consola

# Leer el nivel desde el archivo txt
rows, cols = read_level_from_txt('nivel.txt')

# Ejemplo de actualización del estado después de mover al jugador
game_state = get_game_state()
print("Estado inicial del juego:", game_state)

# Aplicar la solución al juego
solver = DFSSolver(game_state, rows, cols)
path, obstacles_encountered = solver.solve()

if path:
    print("Ruta encontrada:")
    print("Path to goal:", path)
    print("Obstacles encountered:", obstacles_encountered)
    move_along_path(path, rows, cols)
else:
    print("No se encontró solución.")

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK, rect, 1)

    for letter, positions in elements.items():
        if letter == 'A':
            color = RED
        elif letter == '0':
            color = GREEN
        elif letter == 'B':
            color = GRAY
        else:
            color = BLUE

        for pos in positions:
            x, y = pos
            orientation = determine_orientation(positions)
            if len(letter) == 1:
                element_rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            elif orientation == 'vertical':
                element_rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size * len(positions))
            elif orientation == 'horizontal':
                element_rect = pygame.Rect(x * cell_size, y * cell_size, cell_size * len(positions), cell_size)
            else:
                continue

            pygame.draw.rect(screen, color, element_rect)
            font = pygame.font.Font(None, 36)
            text = font.render(letter, True, WHITE)
            screen.blit(text, (element_rect.x + 10, element_rect.y + 5))

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
sys.exit()
