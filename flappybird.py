import pygame, sys, random 



icon= pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png'))
pygame.display.set_icon(icon)

pygame.init()
pygame.display.set_caption('Flappy Bird')

def draw_floor():
        screen.blit(floor_surface,(floor_x_pos,725))
        screen.blit(floor_surface,(floor_x_pos + 576,725))

def create_pipe():
        random_pipe_pos = random.choice(pipe_height)
        bottom_pipe = pipe_surface.get_rect(midtop = (1000,random_pipe_pos))
        top_pipe = pipe_surface.get_rect(midbottom = (1000,random_pipe_pos - 280))
        return bottom_pipe,top_pipe

def move_pipes(pipes):
        for pipe in pipes:
                pipe.centerx -= 6

        return pipes

def draw_pipes(pipes):
        for pipe in pipes:
                if pipe.bottom >= 725:
                        screen.blit(pipe_surface,pipe)
                else:
                        flip_pipe = pygame.transform.flip(pipe_surface,False,True)
                        screen.blit(flip_pipe,pipe)

def check_collision(pipes):
        for pipe in pipes:
                if bird_rect.colliderect(pipe):
                        death_sound.play()
                        return False

        if bird_rect.top <= -10 or bird_rect.bottom >= 800:
                death_sound.play()
                return False

        return True

def rotate_bird(bird):
        new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
        return new_bird

def bird_animation():
        new_bird = bird_frames[bird_index]
        new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
        return new_bird,new_bird_rect

def score_display(game_state):
        if game_state == 'main_game':
                score_surface = game_font.render(str(int(score)),True,(255,255,255))
                score_rect = score_surface.get_rect(center = (288,100))
                screen.blit(score_surface,score_rect)
        

        if game_state == 'game_over':
                high_score_surface = game_font.render(str(int(high_score)),True,(255,255,255))
                high_score_rect = high_score_surface.get_rect(center = (288,100))
                screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
        if score > high_score:
                high_score = score
        return high_score

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((576,800))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

# Game Variables
gravity = 0.24
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/background-night.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,400))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,600,800,500,750]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (300,300))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and game_active:
                                bird_movement = 0
                                bird_movement -= 8
                                flap_sound.play()
                        if event.key == pygame.K_SPACE and game_active == False:
                                game_active = True
                                pipe_list.clear()
                                bird_rect.center = (100,512)
                                score = 0

                if event.type == SPAWNPIPE:
                        pipe_list.extend(create_pipe())

                if event.type == BIRDFLAP:
                        if bird_index < 2:
                                bird_index += 1
                        else:
                                bird_index = 0

                        bird_surface,bird_rect = bird_animation()

        screen.blit(bg_surface,(0,0))
        over = 0
        if game_active:
                bird_movement += gravity
                rotated_bird = rotate_bird(bird_surface)
                bird_rect.centery += bird_movement
                screen.blit(rotated_bird,bird_rect)
                game_active = check_collision(pipe_list)

                pipe_list = move_pipes(pipe_list)
                draw_pipes(pipe_list)
                
                score += 0.01
                score_display('main_game')
                score_sound_countdown -= 1
                if score_sound_countdown <= 0:
                        score_sound.play()
                        score_sound_countdown = 100
                over = 0
        else:
                screen.blit(game_over_surface,game_over_rect)
                high_score = update_score(score, high_score)
                score_display('game_over')
                over = 1


        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -576:
                floor_x_pos = 0
        

        pygame.display.update()
        if not(over):
                clock.tick(60)     
                              
