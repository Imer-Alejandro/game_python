import pygame
import sys
import time

#intrucciones 

#el juego consiste en una representacion de lo pedido de un rompecabeza moviendo elementos que ocuoan 2 posisciones 
#para mover un elementos se presiona primero la letra de ese elemento luego con las teclas de movimineto se puede desplazar
#los obstaculos solo se mueven en la orientacion definida y no pueden atravezarce entre ellos 
# el perosnaje puede moverse igual, se presiona su letra y se desplaza, puede cambiar su orientacion, se presiona control + la tecla de la nueva orientacion 
#el personaje y los demas elementos no pueden atravezarse, por esto se deven mover en posisiones vacias para ir abriendo los espacios 
#el temporizador indica el tiempo limite que se tiene para ir moviendo elementos y abriendo camino al personaje para llegar al punto objetivo antes que este termine
#si se llega antes se imprime ganaste y si no se imprime perdiste y en ambos casos se cierra la consola

pygame.init()

# parametros de la pantalla 
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Juego de Tablero')

# variablres del juego globales
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# variables del tablero y los elementos del personaje
cell_size = 50
rows, cols = 4, 6

# central el tablero
board_width = cols * cell_size
board_height = rows * cell_size
offset_x = (width - board_width) // 2
offset_y = (height - board_height) // 2

# variable del reloj del juego
clock = pygame.time.Clock()

# Diccionario para almacenar elementos del tablero y crearlos como objetos parametrizables
elements = {}
# funcion para crrear elementos  del juego definiendo su poccion incial letra de nombre y orientacion fija
def create_element(letter, x, y, orientation):
    elements[letter] = {
        'x': x,
        'y': y,
        'orientation': orientation,
        'letter': letter
    }

#dibuajar la tabla apartir de la matriz indicada con las filas y columnas 
#esto con el objetivo de saber la posision de cada elemento y no permitir su colision 
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

#dibujar elementos en pantalla 
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

        # Dibujar borde blanco a los elementos de obstaculos y personaje
        border_rect = element_rect.inflate(4, 4)
        pygame.draw.rect(screen, WHITE, border_rect)
        
        # Dibujar el personaje
        pygame.draw.rect(screen, color, element_rect)
        
        font = pygame.font.Font(None, 36)
        text = font.render(letter, True, WHITE)
        screen.blit(text, (element_rect.x + 10, element_rect.y + 5))

def draw_timer_and_goal(time_left):
    font = pygame.font.Font(None, 30)
    timer_text = font.render(f'Tiempo restante: {time_left}', True, RED)
    screen.blit(timer_text, (width // 2 - timer_text.get_width() // 2, 20))
    goal_text = font.render('Objetivo posición: (0,A)', True, BLACK)
    screen.blit(goal_text, (width // 2 - goal_text.get_width() // 2, 70))

# Crear los elementos y el perosnaje 
create_element('X', 3, 3, 'horizontal')  
create_element('A', 0, 0, 'horizontal') 
create_element('B', 5, 1, 'vertical')    
create_element('F', 4, 0, 'horizontal') 
create_element('H', 3, 0, 'vertical') 
create_element('R', 2, 0, 'vertical') 
create_element('T', 1, 2, 'horizontal') 
create_element('P', 0, 2, 'vertical') 

# Elemento seleccionado inicialmente (por defecto el personaje 'X')
selected_element = 'X'

# deginir el tiempo inicial del cronomietro 
start_time = time.time()
time_limit = 30  


while True:
    current_time = time.time()
    elapsed_time = current_time - start_time
    time_left = int(time_limit - elapsed_time)
    
    #si el tiempo llega a cero cerrar pantallla y asumir que perdio 
    if time_left <= 0:
        pygame.quit()
        print("Perdiste")
        sys.exit()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #condiciones para detectar el cambio de personaje indicando su letra para aplicar el movimiento a este
        #teniendo en cuenta que los elementos ostaculos solo se pueden mover en la orientacion definida 
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            # Seleccionar el elemento por su letra
            if event.unicode.upper() in elements:
                selected_element = event.unicode.upper()

            element = elements[selected_element]
            element_x = element['x']
            element_y = element['y']
            orientation = element['orientation']

            # validar el cambio de orientacion del personaje principal que puede cambiarla con Ctrl + flecha
            #esto solo aplica al perosonaje, al cambiar su orientacion solo se desplazara en esa orientacion hasta cambiarla otra vez 
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
                #mover los elementos en el tablero segun las teclas de direcion y validando su orientacion fija en los obtaculos 
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

                # Actualizar las pocicicones de los elementos 
                element['x'] = element_x
                element['y'] = element_y

    #si el jugado llega a la posision objetivo antes que termine el tiempo del cronometro imprimir ganaste y cerrar el juego
    if elements['X']['x'] == 0 and elements['X']['y'] == 0 and time_left != 0:
        pygame.quit()
        print("Ganaste")
        sys.exit()

    # dibujando todos los elementos del ecenario la tabla y los personajes en la ventana de la consola
    draw_board()
    draw_elements()
    #definiendo el temporizador del cronometro inicialisando el conteo
    draw_timer_and_goal(time_left)
    #actualizando la ventana de la consola para debujar cambio en cada frame 
    pygame.display.flip()
    clock.tick(11)
