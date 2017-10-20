import pygame
import sys
from timeit import default_timer as timer

screen = None
pixels = []
window_width = 1000
window_height = 1000
MAX_ITERATIONS = 255
COLOR_MAP = (
    (229, 180, 0),
    (227, 157, 0),
    (226, 134, 0),
    (225, 111, 0),
    (224, 89, 0),
    (222, 67, 0),
    (221, 45, 0),
    (220, 24, 0),
    (219, 2, 0),
    (217, 0, 18),
    (216, 0, 39),
    (215, 0, 59),
    (214, 0, 80),
    (213, 0, 100),
    (211, 0, 120),
    (210, 0, 139),
    (209, 0, 159),
    (208, 0, 178),
    (206, 0, 197),
    (195, 0, 205),
    (174, 0, 204),
    (153, 0, 203),
    (133, 0, 202),
    (113, 0, 200),
    (93, 0, 199),
    (73, 0, 198),
    (53, 0, 197),
    (34, 0, 195),
    (15, 0, 194),
    (0, 3, 193),
    (0, 21, 192),
    (0, 39, 191),
)
# x, y, r
coordinates = [-.5, 0,  1.5]
# arguments respectively mouse_down, initial_mouse_pos, current_mouse_position
mouse_data = [False, (0, 0), (0, 0)]
generating_mandelbrot = False


def main():
    global screen
    global generating_mandelbrot
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Mandelbrot Set")
    clock = pygame.time.Clock()

    while True:
        clock.tick(50)
        if not generating_mandelbrot:
            update()
            render()


# draw pixels to screen
def render():
    screen.fill((0, 0, 0))
    render_2d_array(pixels)
    render_zoom_square()
    pygame.display.flip()


def render_zoom_square():
    global mouse_data
    if mouse_data[0]:
        color = (255, 255, 255)
        initial_pos = mouse_data[1]
        current_pos = mouse_data[2]
        width = current_pos[0] - initial_pos[0]
        height = current_pos[1] - initial_pos[1]
        size = max(width, height)
        outline_width = 1
        rect = (initial_pos[0], initial_pos[1], size, size)
        pygame.draw.rect(screen, color, rect, outline_width)


def update():
    global mouse_data
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not mouse_data[0]:
                mouse_data[0] = True
                mouse_data[1] = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            zoom_in_mouse_location(mouse_data)
            mouse_data[0] = False

    update_mouse_data()


def zoom_in_mouse_location(mouse_data):
    pygame.display.set_caption("Generating...")
    r = coordinates[2]
    # adjusted x and y coordinate (top left)
    x_cor = coordinates[0] - r
    y_cor = coordinates[1] - r
    xm_init = mouse_data[1][0]
    ym_init = mouse_data[1][1]
    xm_cur = mouse_data[2][0]
    ym_cur = mouse_data[2][1]
    box_width = xm_cur - xm_init
    relative_r_difference = box_width / window_width
    delta_pixel = r / (window_width / 2)
    new_x1 = x_cor + delta_pixel * xm_init
    new_y1 = y_cor + delta_pixel * ym_init
    new_x2 = x_cor + delta_pixel * xm_cur
    new_y2 = y_cor + delta_pixel * ym_cur
    coordinates[2] = r * relative_r_difference
    coordinates[0] = (new_x1 + new_x2) / 2
    coordinates[1] = (new_y1 + new_y2) / 2
    new_set = generate_mandelbrot_set(new_x1, new_x2, new_y1, new_y2)
    pygame.display.set_caption("Mandelbrot Set\tx: {}  y: {} r: {}".format(coordinates[0], coordinates[1], coordinates[2]))
    generate_pixels_from_mandelbrot(new_set)


def update_mouse_data():
    if mouse_data[0]:
        mouse_data[2] = pygame.mouse.get_pos()


def render_2d_array(array):
    for index_y, y in enumerate(array):
        for index_x, x in enumerate(y):
            screen.set_at((index_x, index_y),x)


def generate_pixels_from_mandelbrot(mandelbrot_set):
    print("generating pixels from set")
    global pixels
    pixels = []
    for y in range(len(mandelbrot_set)):
        pixels.append([])
        for x in range(len(mandelbrot_set[0])):
            pixels[y].append(get_color_iterations(mandelbrot_set[y][x]))


def get_color_iterations(iterations):
    if 0 < iterations < MAX_ITERATIONS:
        i = iterations % 20
        return COLOR_MAP[i]
    return 0, 0, 0


def generate_mandelbrot_set(real_axis_min, real_axis_max, imaginary_axis_min, imaginary_axis_max,
                            escape_value=MAX_ITERATIONS, width=window_width, height=window_height):
    global generating_mandelbrot
    print("generating mandelbrot set")
    generating_mandelbrot = True
    start = timer()
    iterations_array = []
    real_distance = real_axis_max - real_axis_min
    real_delta = real_distance / width
    imaginary_distance = imaginary_axis_max - imaginary_axis_min
    imaginary_delta = imaginary_distance / height
    c_real_start = real_axis_min
    c_imaginary_start = imaginary_axis_min

    for y in range(height):
        print("process: "+str(((imaginary_delta * y) / imaginary_distance) * 100)+"%")
        c_imaginary = c_imaginary_start + y * imaginary_delta
        iterations_array.append([])
        for x in range(width):
            c_real = c_real_start + x * real_delta
            iterations_array[y].append(calculate_iterations(complex(c_real, c_imaginary), escape_value))

    dt = timer() - start
    print("Mandelbrot set generated in %f s" % dt)
    generating_mandelbrot = False
    return iterations_array


def calculate_iterations(c, escape_value, z=0, current_iteration=1):
        new_z = z**2 + c
        if abs(new_z) > 2:
            return current_iteration
        if current_iteration > escape_value:
            return 0
        return calculate_iterations(c, escape_value, new_z, current_iteration + 1)


x = coordinates[0]
y = coordinates[1]
r = coordinates[2]
mandelbrot = generate_mandelbrot_set(x - r, x + r, y - r, y + r)
generate_pixels_from_mandelbrot(mandelbrot)
main()
