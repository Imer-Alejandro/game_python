import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Juego de Tablero')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Tamaño del personaje y celdas del tablero
cell_size = 50
rows, cols = 4, 6

# Calcular desplazamiento para centrar el tablero
board_width = cols * cell_size
board_height = rows * cell_size
offset_x = (width - board_width) // 2
offset_y = (height - board_height) // 2

# Configurar el reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()

# Diccionario para almacenar elementos del tablero
elements = {}

def create_element(letter, x, y, orientation):
    elements[letter] = {
        'x': x,
        'y': y,
        'orientation': orientation,
        'letter': letter
    }

def draw_board():
    screen.fill(WHITE)
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(offset_x + col * cell_size, offset_y + row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Dibujar bordes con números y letras
    font = pygame.font.Font(None, 36)
    for row in range(rows):
        text = font.render(str(row), True, BLACK)
        screen.blit(text, (offset_x - 30, offset_y + row * cell_size + 5))
    for col in range(cols):
        text = font.render(chr(65 + col), True, BLACK)
        screen.blit(text, (offset_x + col * cell_size + 15, offset_y - 40))

    pygame.display.flip()

def draw_elements():
    for element in elements.values():
        x = element['x']
        y = element['y']
        orientation = element['orientation']
        letter = element['letter']
        color = RED if letter == 'X' else BLUE
        
        if orientation == 'horizontal':
            element_rect = pygame.Rect(offset_x + x * cell_size, offset_y + y * cell_size, cell_size * 2, cell_size)
        elif orientation == 'vertical':
            element_rect = pygame.Rect(offset_x + x * cell_size, offset_y + y * cell_size, cell_size, cell_size * 2)
        elif orientation == 'up':
            element_rect = pygame.Rect(offset_x + x * cell_size, offset_y + y * cell_size - cell_size, cell_size, cell_size * 2)
        elif orientation == 'down':
            element_rect = pygame.Rect(offset_x + x * cell_size, offset_y + y * cell_size, cell_size, cell_size * 2)
        elif orientation == 'left':
            element_rect = pygame.Rect(offset_x + x * cell_size - cell_size, offset_y + y * cell_size, cell_size * 2, cell_size)

        # Dibujar borde blanco
        border_rect = element_rect.inflate(4, 4)
        pygame.draw.rect(screen, WHITE, border_rect)
        
        # Dibujar el personaje
        pygame.draw.rect(screen, color, element_rect)
        
        font = pygame.font.Font(None, 36)
        text = font.render(letter, True, WHITE)
        screen.blit(text, (element_rect.x + 10, element_rect.y + 5))
    pygame.display.flip()

# Crear el personaje y obstáculos
create_element('X', 3, 3, 'horizontal')  # Personaje principal
create_element('A', 0, 0, 'horizontal')  # Obstáculo A
create_element('B', 5, 1, 'vertical')    # Obstáculo B
create_element('F', 4, 0, 'horizontal')  # f
create_element('H', 3, 0, 'vertical') 
create_element('R', 2, 0, 'vertical') 
create_element('T', 1, 2, 'horizontal') 
create_element('P', 0, 2, 'vertical') 

# Elemento seleccionado inicialmente (por defecto el personaje 'X')
selected_element = 'X'

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            # Seleccionar el elemento por su letra
            if event.unicode.upper() in elements:
                selected_element = event.unicode.upper()

            element = elements[selected_element]
            element_x = element['x']
            element_y = element['y']
            orientation = element['orientation']

            # Cambiar la orientación del personaje principal 'X' con Ctrl + flecha
            if selected_element == 'X' and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                if event.key == pygame.K_UP:
                    elements['X']['orientation'] = 'up'
                elif event.key == pygame.K_DOWN:
                    elements['X']['orientation'] = 'down'
                elif event.key == pygame.K_LEFT:
                    elements['X']['orientation'] = 'left'
                elif event.key == pygame.K_RIGHT:
                    elements['X']['orientation'] = 'horizontal'
            else:
                # Mover el elemento basado en la tecla presionada y la orientación
                if orientation == 'horizontal':
                    if event.key == pygame.K_LEFT and element_x > 0:
                        if not any(el['x'] == element_x - 1 and el['y'] == element_y for el in elements.values()):
                            element_x -= 1
                    elif event.key == pygame.K_RIGHT and element_x < cols - 2:
                        if not any(el['x'] == element_x + 1 and el['y'] == element_y for el in elements.values()):
                            element_x += 1
                elif orientation == 'vertical':
                    if event.key == pygame.K_UP and element_y > 0:
                        if not any(el['x'] == element_x and el['y'] == element_y - 1 for el in elements.values()):
                            element_y -= 1
                    elif event.key == pygame.K_DOWN and element_y < rows - 2:
                        if not any(el['x'] == element_x and el['y'] == element_y + 1 for el in elements.values()):
                            element_y += 1
                elif orientation == 'up':
                    if event.key == pygame.K_UP and element_y > 1:
                        if not any(el['x'] == element_x and el['y'] == element_y - 1 for el in elements.values()):
                            element_y -= 1
                    elif event.key == pygame.K_DOWN and element_y < rows - 1:
                        if not any(el['x'] == element_x and el['y'] == element_y + 1 for el in elements.values()):
                            element_y += 1
                elif orientation == 'down':
                    if event.key == pygame.K_DOWN and element_y < rows - 1:
                        if not any(el['x'] == element_x and el['y'] == element_y + 1 for el in elements.values()):
                            element_y += 1
                    elif event.key == pygame.K_UP and element_y > 1:
                        if not any(el['x'] == element_x and el['y'] == element_y - 1 for el in elements.values()):
                            element_y -= 1
                elif orientation == 'left':
                    if event.key == pygame.K_LEFT and element_x > 1:
                        if not any(el['x'] == element_x - 1 and el['y'] == element_y for el in elements.values()):
                            element_x -= 1
                    elif event.key == pygame.K_RIGHT and element_x < cols - 1:
                        if not any(el['x'] == element_x + 1 and el['y'] == element_y for el in elements.values()):
                            element_x += 1

                # Actualizar la nueva posición del elemento seleccionado
                element['x'] = element_x
                element['y'] = element_y

    draw_board()
    draw_elements()
    clock.tick(11)
 