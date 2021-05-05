import pygame
import math
from numba import jit

WIDTH, HEIGHT = 750, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mandelbrot set")

RE_START = -2.25
RE_END = 0.75
IM_START = -1.25
IM_END = 1.25

MAX_ITER = 128
ZOOM_ITER = 1

def mandelbrot(c, max_iter):
    z = 0
    n = 0 
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n+=1
    if n == max_iter: 
        return 0
    return n

def pixel(surface, color, pos):
    pygame.draw.line(screen, color, pos, pos)

def draw_mandelbrot():
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            c = complex(RE_START + (x/WIDTH)*(RE_END - RE_START), IM_START + (y/HEIGHT)*(IM_END - IM_START))
            iter = jitted_mandelbrot(c, MAX_ITER)

            color1 = int(iter*3)%255
            color2 = 100%(iter*2+1)%255
            color3 = 100%(iter*4+1)%255

            pixel(screen, (color1, color2, color3), (x, y))
    pygame.display.update()

def draw_mandelbrot_zoomed(mouse_pos, re_start, re_end, im_start, im_end, zoom_iter, max_iter):
    re_part = re_start + (mouse_pos[0]/WIDTH)*(re_end - re_start)
    im_part = im_start + (mouse_pos[1]/HEIGHT)*(im_end - im_start)

    re_start_n = re_part - 0.5 / (zoom_iter**zoom_iter)
    re_end_n = re_part + 0.5 / (zoom_iter**zoom_iter)
    im_start_n = im_part - 0.4 / (zoom_iter**zoom_iter)
    im_end_n =  im_part + 0.4 / (zoom_iter**zoom_iter)

    zoom_iter += 1
    
    for i in range(0, WIDTH):
        for j in range(0, HEIGHT):
            c = complex(re_start_n + (i/WIDTH)*(re_end_n - re_start_n), im_start_n + (j/HEIGHT)*(im_end_n - im_start_n))
            
            iter = jitted_mandelbrot(c, max_iter)

            color1 = int(iter*3)%255
            color2 = 100%(iter*2+1)%255
            color3 = 100%(iter*4+1)%255
            pixel(screen, (color1, color2, color3), (i, j))
    pygame.display.update()
    max_iter *=2
    return re_start_n, re_end_n, im_start_n, im_end_n, zoom_iter, max_iter


jitted_drawmandelbrot = jit()(draw_mandelbrot_zoomed)
jitted_mandelbrot = jit()(mandelbrot)
    

def main():
    run = True

    re_start = RE_START
    re_end = RE_END
    im_start = IM_START
    im_end = IM_END
    zoom_iter = ZOOM_ITER
    max_iter = MAX_ITER

    draw_mandelbrot()
    while run:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_r:
                draw_mandelbrot()
                re_start = RE_START
                re_end = RE_END
                im_start = IM_START
                im_end = IM_END
                zoom_iter = ZOOM_ITER
                max_iter = MAX_ITER
        if event.type == pygame.MOUSEBUTTONDOWN:          
            mouse_pos = pygame.mouse.get_pos()
            
            re_start, re_end, im_start, im_end, zoom_iter, max_iter = jitted_drawmandelbrot(mouse_pos, re_start, re_end, im_start, im_end, zoom_iter, max_iter)

if __name__ == "__main__":
    main()