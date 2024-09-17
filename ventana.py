import pygame
import win32console
import win32gui
from random import randint

# Ocultar la consola
ventana = win32console.GetConsoleWindow()
win32gui.ShowWindow(ventana, 0)

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Bingo Brochero")
clock = pygame.time.Clock()
running = True
color_texto = (0, 0, 0)
color_fondo_normal = (255, 255, 255)
color_fondo_clicked = (0, 255, 0)
font = pygame.font.SysFont("Calibri Bold", 80)

# Crear una lista para almacenar el estado de cada celda
texto = []
for i in range(1, 91):
    texto.append([str(i), str((i-1)//10+1), str((i-1)%10), False])

# Definir márgenes
margen_x = 20
margen_y_superior = 20
margen_y_inferior = 80

# Número de filas y columnas
num_filas = 9
num_columnas = 10

def centrar_texto(screen, tex, fila, columna, cell_width, cell_height, margen_x, margen_y_superior, margen_y_inferior, color_fondo):
    text_surface = font.render(tex, True, color_texto, color_fondo)
    text_rect = text_surface.get_rect()

    # Calcula la posición basada en fila y columna con márgenes
    x_pos = int(columna) * cell_width + margen_x
    y_pos = int(fila) * cell_height + margen_y_superior

    # Ajusta la posición para centrar el texto en esa posición
    x_pos += (cell_width - text_rect.width) // 2
    y_pos += (cell_height - text_rect.height) // 2

    # Blit del texto centrado
    screen.blit(text_surface, (x_pos, y_pos))

fullscreen = False

color_circulo = 'red'
posicion = pygame.Vector2(200, 50)

random_number = None
used_numbers = set()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE and not fullscreen:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            elif event.key == pygame.K_r:
                color_fondo = color_fondo_normal  # Actualiza el color de fondo al blanco
                used_numbers.clear()
                for i in range(len(texto)):
                    texto[i][3] = False  # Resetea el estado de clic de todas las celdas
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Verifica clic en el círculo
            distance = pygame.Vector2(mouse_x, mouse_y).distance_to(posicion)
            if distance <= 40:
                if len(used_numbers) < 90:
                    while True:
                        new_number = randint(1, 90)
                        if new_number not in used_numbers:
                            random_number = new_number
                            used_numbers.add(new_number)
                            break
                else:
                    random_number = "No más números disponibles"
                # Cambia el color del círculo
                color_circulo = "green" if color_circulo == "red" else "red"

            # Verifica clic en cada celda
            for tex, fila, columna, clicked in texto:
                cell_width = (screen_width - 2 * margen_x) // num_columnas
                cell_height = (screen_height - (margen_y_superior + margen_y_inferior)) // num_filas
                x_pos = int(columna) * cell_width + margen_x
                y_pos = int(fila) * cell_height + margen_y_superior

                if x_pos <= mouse_x <= x_pos + cell_width and y_pos <= mouse_y <= y_pos + cell_height:
                    texto[(int(fila)-1) * num_columnas + int(columna)][3] = not clicked  # Cambiar estado

    # Tamaño actual de la ventana
    screen_width, screen_height = screen.get_size()

    # Calcula el ancho y alto de cada celda
    cell_width = (screen_width - 2 * margen_x) // num_columnas
    cell_height = (screen_height - (margen_y_superior + margen_y_inferior)) // num_filas

    screen.fill(color_fondo_normal)  # Rellena la pantalla con el color de fondo normal

    # Dibuja el círculo
    pygame.draw.circle(screen, color_circulo, posicion, 40)

    # Dibuja las celdas
    for tex, fila, columna, clicked in texto:
        color_fondo = color_fondo_clicked if clicked else color_fondo_normal
        centrar_texto(screen, tex, int(fila), int(columna), cell_width, cell_height, margen_x, margen_y_superior, margen_y_inferior, color_fondo)

    # Muestra el número aleatorio junto al círculo
    if random_number is not None:
        number_surface = font.render(str(random_number), True, (0, 0, 0))
        screen.blit(number_surface, (posicion.x + 50, posicion.y - 25))  # Ajusta la posición debajo del círculo
    
    pygame.display.flip()

    dt = clock.tick(60)

pygame.quit()
