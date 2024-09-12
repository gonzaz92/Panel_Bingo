import pygame
import win32console
import win32gui

ventana = win32console.GetConsoleWindow()
win32gui.ShowWindow(ventana,0)

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
    texto.append([str(i), str((i-1)//10), str((i-1)%10), False]) 

# Definir márgenes
margen_x = 20
margen_y = 20

def centrar_texto(screen, tex, fila, columna, cell_width, cell_height, margen_x, margen_y, color_fondo):
    text_surface = font.render(tex, True, color_texto, color_fondo)
    text_rect = text_surface.get_rect()

    # Calcula la posición basada en fila y columna con márgenes
    x_pos = int(columna) * cell_width + margen_x
    y_pos = int(fila) * cell_height + margen_y

    # Ajusta la posición para centrar el texto en esa posición
    x_pos += (cell_width - text_rect.width) // 2
    y_pos += (cell_height - text_rect.height) // 2

    # Blit del texto centrado
    screen.blit(text_surface, (x_pos, y_pos))

fullscreen = False
color_fondo = color_fondo_normal 

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
                for i in range(len(texto)):
                    texto[i][3] = False  # Resetea el estado de clic de todas las celdas
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Verifica clic en cada celda
            for tex, fila, columna, clicked in texto:
                cell_width = (screen_width - 2 * margen_x) // num_columnas
                cell_height = (screen_height - 2 * margen_y) // num_filas
                x_pos = int(columna) * cell_width + margen_x
                y_pos = int(fila) * cell_height + margen_y

                if x_pos <= mouse_x <= x_pos + cell_width and y_pos <= mouse_y <= y_pos + cell_height:
                    texto[int(fila) * num_columnas + int(columna)][3] = not clicked  # Cambiar estado

    screen.fill(color_fondo)  # Rellena la pantalla con el color de fondo actualizado

    # tamaño actual de la ventana
    screen_width, screen_height = screen.get_size()

    # número de filas y columnas basado en el texto
    num_filas = 9
    num_columnas = 10

    # Calcula el ancho y alto de cada celda
    cell_width = (screen_width - 2 * margen_x) // num_columnas
    cell_height = (screen_height - 2 * margen_y) // num_filas

    for tex, fila, columna, clicked in texto:
        color_fondo = color_fondo_clicked if clicked else color_fondo_normal
        centrar_texto(screen, tex, int(fila), int(columna), cell_width, cell_height, margen_x, margen_y, color_fondo)

    pygame.display.flip()

    dt = clock.tick(60)

pygame.quit()
