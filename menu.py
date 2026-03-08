import sys
import random

import pygame
import pygame.mixer

from classes.constants import WIDTH, HEIGHT, BLACK, WHITE, RED
from settings import get_fullscreen, set_fullscreen, get_high_score


def get_screen_size():
    if is_fullscreen:
        return screen.get_width(), screen.get_height()
    return WIDTH, HEIGHT - 80


def scale_pos(x, y):
    screen_w, screen_h = get_screen_size()
    return int(x * screen_w / WIDTH), int(y * screen_h / HEIGHT)


def scale_rect(rect):
    screen_w, screen_h = get_screen_size()
    return pygame.Rect(
        int(rect.x * screen_w / WIDTH),
        int(rect.y * screen_h / HEIGHT),
        int(rect.width * screen_w / WIDTH),
        int(rect.height * screen_h / HEIGHT)
    )


def animate_screen():
    screen_w, screen_h = get_screen_size()
    scaled_bg = pygame.transform.scale(mainmenu_img, (screen_w, screen_h))
    for i in range(0, 20):
        screen.blit(scaled_bg, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)
        screen.blit(scaled_bg, (random.randint(-5, 5), random.randint(-5, 5)))
        pygame.display.flip()
        pygame.time.wait(10)


def apply_display_mode(fullscreen):
    global screen, mainmenu_img_scaled
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT - 80))
    screen_w, screen_h = screen.get_width(), screen.get_height()
    mainmenu_img_scaled = pygame.transform.scale(mainmenu_img, (screen_w, screen_h))


pygame.mixer.init()
pygame.init()
pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)
pygame.mixer.set_num_channels(20)
for i in range(20):
    channel = pygame.mixer.Channel(i)
    channel.set_volume(0.25)

is_fullscreen = get_fullscreen()
if is_fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT - 80))

pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

mainmenu_img = pygame.image.load('images/mainmenu.jpg').convert()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

screen_w, screen_h = screen.get_width(), screen.get_height()
mainmenu_img_scaled = pygame.transform.scale(mainmenu_img, (screen_w, screen_h))

logo_img = pygame.image.load('images/ch.png').convert_alpha()

play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 205, 50)
options_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 25, 205, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 205, 50)

pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.play(-1)
explosion_sound = pygame.mixer.Sound('game_sounds/explosions/explosion1.wav')
explosion_sound.set_volume(0.25)
selected_button = 0
show_menu = True
in_options = False

joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()


def draw_main_menu():
    screen_w, screen_h = get_screen_size()
    screen.blit(mainmenu_img_scaled, (0, 0))
    
    scale_x = screen_w / WIDTH
    scale_y = screen_h / HEIGHT
    
    scaled_logo = pygame.transform.scale(logo_img, (int(logo_img.get_width() * scale_x), int(logo_img.get_height() * scale_y)))
    logo_x = (screen_w - scaled_logo.get_width()) // 2
    logo_y = int(50 * scale_y)
    screen.blit(scaled_logo, (logo_x, logo_y))

    font_size = int(40 * min(scale_x, scale_y))
    font = pygame.font.SysFont('Comic Sans MS', font_size)
    
    play_scaled = scale_rect(play_button_rect)
    options_scaled = scale_rect(options_button_rect)
    quit_scaled = scale_rect(quit_button_rect)
    
    text = font.render("Play", True, WHITE)
    pygame.draw.rect(screen, BLACK, play_scaled, border_radius=10)
    if selected_button == 0:
        pygame.draw.rect(screen, RED, play_scaled, border_radius=10, width=4)
    text_rect = text.get_rect(center=play_scaled.center)
    screen.blit(text, text_rect)
    
    text = font.render("Options", True, WHITE)
    pygame.draw.rect(screen, BLACK, options_scaled, border_radius=10)
    if selected_button == 1:
        pygame.draw.rect(screen, RED, options_scaled, border_radius=10, width=4)
    text_rect = text.get_rect(center=options_scaled.center)
    screen.blit(text, text_rect)
    
    text = font.render("Exit", True, WHITE)
    pygame.draw.rect(screen, BLACK, quit_scaled, border_radius=10)
    if selected_button == 2:
        pygame.draw.rect(screen, RED, quit_scaled, border_radius=10, width=4)
    text_rect = text.get_rect(center=quit_scaled.center)
    screen.blit(text, text_rect)
    
    high_score = get_high_score()
    if high_score is not None:
        hs_font_size = int(28 * min(scale_x, scale_y))
        hs_font = pygame.font.SysFont('Comic Sans MS', hs_font_size)
        hs_text = hs_font.render(f"High Score: {high_score}", True, (255, 215, 0))
        hs_rect = hs_text.get_rect(center=(screen_w // 2, quit_scaled.bottom + int(40 * scale_y)))
        screen.blit(hs_text, hs_rect)
    
    return play_scaled, options_scaled, quit_scaled


def draw_options_menu():
    global is_fullscreen
    screen_w, screen_h = get_screen_size()
    screen.blit(mainmenu_img_scaled, (0, 0))
    
    scale_x = screen_w / WIDTH
    scale_y = screen_h / HEIGHT
    
    font_title_size = int(50 * min(scale_x, scale_y))
    font_size = int(35 * min(scale_x, scale_y))
    font_title = pygame.font.SysFont('Comic Sans MS', font_title_size)
    font = pygame.font.SysFont('Comic Sans MS', font_size)
    
    title_text = font_title.render("Options", True, WHITE)
    title_rect = title_text.get_rect(center=(screen_w // 2, int(100 * scale_y)))
    screen.blit(title_text, title_rect)
    
    mode_text = "Fullscreen" if is_fullscreen else "Windowed"
    screen_mode_rect_base = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 50)
    screen_mode_rect = scale_rect(screen_mode_rect_base)
    pygame.draw.rect(screen, BLACK, screen_mode_rect, border_radius=10)
    if selected_button == 0:
        pygame.draw.rect(screen, RED, screen_mode_rect, border_radius=10, width=4)
    
    mode_label = font.render(f"Screen: {mode_text}", True, WHITE)
    mode_label_rect = mode_label.get_rect(center=screen_mode_rect.center)
    screen.blit(mode_label, mode_label_rect)
    
    menu_button_rect_base = pygame.Rect(WIDTH - 160, HEIGHT - 70, 140, 50)
    menu_button_rect = scale_rect(menu_button_rect_base)
    pygame.draw.rect(screen, BLACK, menu_button_rect, border_radius=10)
    if selected_button == 1:
        pygame.draw.rect(screen, RED, menu_button_rect, border_radius=10, width=4)
    
    menu_text = font.render("Menu", True, WHITE)
    menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
    screen.blit(menu_text, menu_text_rect)
    
    return screen_mode_rect, menu_button_rect


while show_menu:
    if not in_options:
        play_scaled, options_scaled, quit_scaled = draw_main_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_scaled.collidepoint(x, y):
                    explosion_sound.play()
                    animate_screen()
                    show_menu = False
                    import main
                    main.main()
                    break
                elif options_scaled.collidepoint(x, y):
                    in_options = True
                    selected_button = 0
                elif quit_scaled.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_button = (selected_button - 1) % 3
                elif event.key == pygame.K_DOWN:
                    selected_button = (selected_button + 1) % 3
                elif event.key == pygame.K_RETURN:
                    if selected_button == 0:
                        explosion_sound.play()
                        animate_screen()
                        show_menu = False
                        screen.fill(BLACK)
                        import main
                        main.main()
                        break
                    elif selected_button == 1:
                        in_options = True
                        selected_button = 0
                    elif selected_button == 2:
                        pygame.quit()
                        sys.exit()

            if joystick:
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        if selected_button == 0:
                            explosion_sound.play()
                            animate_screen()
                            show_menu = False
                            screen.fill(BLACK)
                            import main
                            main.main()
                            break
                        elif selected_button == 1:
                            in_options = True
                            selected_button = 0
                        elif selected_button == 2:
                            pygame.quit()
                            sys.exit()
                elif event.type == pygame.JOYHATMOTION:
                    if event.value[1] == 1:
                        selected_button = (selected_button - 1) % 3
                    elif event.value[1] == -1:
                        selected_button = (selected_button + 1) % 3

    else:
        screen_mode_rect, menu_button_rect = draw_options_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if screen_mode_rect.collidepoint(x, y):
                    is_fullscreen = not is_fullscreen
                    set_fullscreen(is_fullscreen)
                    apply_display_mode(is_fullscreen)
                elif menu_button_rect.collidepoint(x, y):
                    in_options = False
                    selected_button = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_button = (selected_button - 1) % 2
                elif event.key == pygame.K_DOWN:
                    selected_button = (selected_button + 1) % 2
                elif event.key == pygame.K_RETURN:
                    if selected_button == 0:
                        is_fullscreen = not is_fullscreen
                        set_fullscreen(is_fullscreen)
                        apply_display_mode(is_fullscreen)
                    elif selected_button == 1:
                        in_options = False
                        selected_button = 0
                elif event.key == pygame.K_ESCAPE:
                    in_options = False
                    selected_button = 0

            if joystick:
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        if selected_button == 0:
                            is_fullscreen = not is_fullscreen
                            set_fullscreen(is_fullscreen)
                            apply_display_mode(is_fullscreen)
                        elif selected_button == 1:
                            in_options = False
                            selected_button = 0
                    elif event.button == 1:
                        in_options = False
                        selected_button = 0
                elif event.type == pygame.JOYHATMOTION:
                    if event.value[1] == 1:
                        selected_button = (selected_button - 1) % 2
                    elif event.value[1] == -1:
                        selected_button = (selected_button + 1) % 2

    pygame.display.flip()
    clock.tick(60)

pygame.quit()