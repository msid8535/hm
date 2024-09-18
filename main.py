import pygame
import sqlite3
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

from game import Game

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
init_color = pygame.Color(124, 156, 0)
green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)
init_image = pygame.image.load('images/snake.png')
volume_on = pygame.image.load('images/volume_on.png')

db = sqlite3.connect('snake.db')
cursor = db.cursor()
game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((game.settings.width * 25, game.settings.height * 15))
pygame.display.set_caption('Gluttonous')

crash_sound = pygame.mixer.Sound('./sound/crash.wav')


def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, color=black):
    large_text = pygame.font.SysFont('comicsansms', 50)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()


def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont('comicsansms', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


def quitgame():
    pygame.quit()
    quit()

def do_nothing():
    pass

def crash():
    pygame.mixer.Sound.play(crash_sound)
    message_display('Game Over', game.settings.width / 2 * 25, game.settings.height / 3 * 15, black)
    time.sleep(1)
    highscore('game_over')


def initial_interface():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        screen.fill(init_color)
        screen.blit(init_image, (game.settings.width*0.45, game.settings.height * 0.8))
        
        button('Start', 50, 350, 110, 40, green, bright_green, username)
        button('Quit', 530, 350, 110, 40, red, bright_red, quitgame)
        button('Ranks', 270, 350, 150, 40, yellow, bright_yellow, highscore, 'home_page')

        pygame.display.update()
        pygame.time.Clock().tick(15)

def username():
    base_font = pygame.font.SysFont('comicsansms', 32)
    small_font = pygame.font.SysFont('comicsansms', 18)
    user_text = []
    input_rect = pygame.Rect(120, 180, 140, 50)
    color = pygame.Color((117, 116, 116))
    active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                    if user_text == []:
                        user_text.append('_')
                    else:
                        pass
            
            if active == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(user_text) > 1:
                            user_text.pop(-2)
                        else:
                            pass
                    elif event.unicode.isalnum():
                        user_text.insert(-1, event.unicode)
                    else:
                        pass


        screen.fill((pygame.Color(204, 228, 227)))

        if active:
            color = black

        pygame.draw.rect(screen, color, input_rect, 2)

        user_string = ''.join(user_text)
        text_surface = base_font.render('Please enter username:', True, (0, 0, 0))
        text_surface2 = small_font.render('(username must be letters and numbers only)', True, (128, 127, 127))
        text_surface1 =  base_font.render(user_string, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect.x, input_rect.y - 90))
        screen.blit(text_surface2, (input_rect.x, input_rect.y - 40))
        screen.blit(text_surface1, (input_rect.x + 5, input_rect.y + 5))

        input_rect.w = max(400, text_surface1.get_width() + 10)
        if user_string[:-1] != '':
            button("Play!", 440, 270, 80, 40, blue, bright_blue, game_loop, user_string[:-1])
        else:
            button("Play!", 440, 270, 80, 40, (128, 127, 127), (128, 127, 127), do_nothing)

        pygame.display.flip()
        fpsClock.tick(15)

def highscore(source):
    player = cursor.execute("SELECT username FROM games ORDER BY pk DESC LIMIT 1").fetchone()
    top3 = cursor.execute("SELECT * FROM games ORDER BY score DESC LIMIT 3").fetchall()
    db.commit()

    base_font = pygame.font.SysFont('comicsansms', 32)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        
        screen.fill((253, 236, 166))
        
        pygame.draw.rect(screen, black, pygame.Rect(50, 160, 600, 50), 2)
        pygame.draw.rect(screen, yellow, (52, 162, 596, 48 )) #colour

        pygame.draw.rect(screen, black, pygame.Rect(50, 210, 300, 50), 2)
        pygame.draw.rect(screen, black, pygame.Rect(350, 210, 300, 50), 2)
        pygame.draw.rect(screen, black, pygame.Rect(50, 260, 300, 50), 2)
        pygame.draw.rect(screen, black, pygame.Rect(350, 260, 300, 50), 2)
        pygame.draw.rect(screen, black, pygame.Rect(50, 310, 300, 50), 2)
        pygame.draw.rect(screen, black, pygame.Rect(350, 310, 300, 50), 2)

        highscore = base_font.render('Highscore: '+ str(top3[0][1]), True, black)
        heading =  base_font.render('Top 3', True, black)
        first_n = base_font.render(str(top3[0][0]), True, black)
        first_s = base_font.render(str(top3[0][1]), True, black)
        second_n = base_font.render(str(top3[1][0]), True, black)
        second_s = base_font.render(str(top3[1][1]), True, black)
        third_n = base_font.render(str(top3[2][0]), True, black)
        third_s = base_font.render(str(top3[2][1]), True, black)
        screen.blit(highscore, (50, 100))
        screen.blit(heading, (300, 165))
        screen.blit(first_n, (70, 215))
        screen.blit(first_s, (475, 215))
        screen.blit(second_n, (70, 265))
        screen.blit(second_s, (475, 265))
        screen.blit(third_n, (70, 315))
        screen.blit(third_s, (475, 315))
        
        if source == 'home_page':
            button('Back', 530, 30, 110, 40, blue, bright_blue, initial_interface)
        elif source == 'game_over':
            button('Home', 50, 30, 110, 40, blue, bright_blue, initial_interface)
            button('Quit', 530, 30, 110, 40, red, bright_red, quitgame)
            button('Play Again', 270, 30, 150, 40, green, bright_green, game_loop, player[0])

        pygame.display.flip()
        fpsClock.tick(15)

def game_loop(player, fps=10):
    font = pygame.font.SysFont(None, 25)
    start_time = pygame.time.get_ticks()
    game.restart_game()

    game_audio = pygame.mixer.Sound('./sound/game_audio.mp3')
    pygame.mixer.Sound.play(game_audio, 1000)
        

    while not game.game_end():
        
        counting_time = pygame.time.get_ticks() - start_time
        # change milliseconds into minutes, seconds, milliseconds
        counting_minutes = str(counting_time//60000).zfill(2)
        counting_seconds = str( (counting_time%60000)//1000 ).zfill(2)
        counting_string = "%s:%s" % (counting_minutes, counting_seconds)
        counting_text = font.render(str(counting_string), 1, black)

        pygame.event.pump()

        move = human_move()
        fps = 5

        game.do_move(move)
        screen.fill((242, 242, 242))


        for width in range (0, game.settings.width * 25, 28):
            for height in range (0, game.settings.height * 15, 28):
                pygame.draw.rect(screen, white,(width, height,14,14))
        for width in range (14, game.settings.width * 25, 28):
            for height in range (14, game.settings.height * 15, 28):
                pygame.draw.rect(screen, white,(width,height,14,14))

        pygame.draw.line(screen, black, (0,0), (game.settings.width * 25, 0), 2)
        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(black, screen)
        screen.blit(counting_text, (650, 2))

        pygame.display.flip()

        fpsClock.tick(fps)

    cursor.execute("INSERT INTO games('username', 'score') VALUES(?, ?)",(player, game.snake.score,))
    db.commit()

    pygame.mixer.Sound.set_volume(game_audio, 0)
    crash()


def human_move():
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move


if __name__ == "__main__":
    initial_interface()
