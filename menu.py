import sys
import random

import pygame
import pygame.mixer

from classes.constants import WIDTH, HEIGHT, BLACK, WHITE, RED
from settings import get_fullscreen, set_fullscreen


def animate_screen():
    for i in range(0, 20):
        screen.blit(mainmenu_img, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)
        screen.blit(mainmenu_img, (random.randint(-5, 5), random.randint(-5, 5)))
        pygame.display.flip()
        pygame.time.wait(10)


def apply_display_mode(fullscreen):
    global screen
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT - 80))


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

logo_img = pygame.image.load('images/ch.png').convert_alpha()
logo_x = (WIDTH - logo_img.get_width()) // 2
logo_y = 50

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
    screen.blit(mainmenu_img, (0, 0))
    screen.blit(logo_img, (logo_x, logo_y))

    font = pygame.font.SysFont('Comic Sans MS', 40)
    
    # Play button
    text = font.render("Play", True, WHITE)
    pygame.draw.rect(screen, BLACK, play_button_rect, border_radius=10)
    if selected_button == 0:
        pygame.draw.rect(screen, RED, play_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = play_button_rect.center
    screen.blit(text, text_rect)
    
    # Options button
    text = font.render("Options", True, WHITE)
    pygame.draw.rect(screen, BLACK, options_button_rect, border_radius=10)
    if selected_button == 1:
        pygame.draw.rect(screen, RED, options_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = options_button_rect.center
    screen.blit(text, text_rect)
    
    # Exit button
    text = font.render("Exit", True, WHITE)
    pygame.draw.rect(screen, BLACK, quit_button_rect, border_radius=10)
    if selected_button == 2:
        pygame.draw.rect(screen, RED, quit_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = quit_button_rect.center
    screen.blit(text, text_rect)


def draw_options_menu():
    global is_fullscreen
    screen.blit(mainmenu_img, (0, 0))
    
    font_title = pygame.font.SysFont('Comic Sans MS', 50)
    font = pygame.font.SysFont('Comic Sans MS', 35)
    
    # Title
    title_text = font_title.render("Options", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_text, title_rect)
    
    # Screen mode option
    mode_text = "Fullscreen" if is_fullscreen else "Windowed"
    screen_mode_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 50)
    pygame.draw.rect(screen, BLACK, screen_mode_rect, border_radius=10)
    if selected_button == 0:
        pygame.draw.rect(screen, RED, screen_mode_rect, border_radius=10, width=4)
    
    mode_label = font.render(f"Screen: {mode_text}", True, WHITE)
    mode_label_rect = mode_label.get_rect(center=screen_mode_rect.center)
    screen.blit(mode_label, mode_label_rect)
    
    # Menu button (bottom-right corner)
    menu_button_rect = pygame.Rect(WIDTH - 160, HEIGHT - 70, 140, 50)
    pygame.draw.rect(screen, BLACK, menu_button_rect, border_radius=10)
    if selected_button == 1:
        pygame.draw.rect(screen, RED, menu_button_rect, border_radius=10, width=4)
    
    menu_text = font.render("Menu", True, WHITE)
    menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
    screen.blit(menu_text, menu_text_rect)
    
    return screen_mode_rect, menu_button_rect


while show_menu:
    if not in_options:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_button_rect.collidepoint(x, y):
                    explosion_sound.play()
                    animate_screen()
                    show_menu = False
                    import main
                    main.main()
                    break
                elif options_button_rect.collidepoint(x, y):
                    in_options = True
                    selected_button = 0
                elif quit_button_rect.collidepoint(x, y):
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

        draw_main_menu()
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