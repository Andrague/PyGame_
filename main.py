import pygame
clock= pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((600,333))
pygame.display.set_caption("PyGame")
icon= pygame.image.load("images/icon.png").convert_alpha()
pygame.display.set_icon(icon)
pygame.mixer.music.load('sounds/66dc9666f919d55.mp3')

myfont= pygame.font.Font('fonts/Caprasimo-Regular.ttf',40)
text_surface=myfont.render('PyGame',True,'red')

bg=pygame.image.load('images/imgonline-com-ua-Resize-mRTByt2Zmx.jpg').convert()
walk_right=[pygame.image.load('images/right/walk_right1.png').convert_alpha(),
            pygame.image.load('images/right/walk_right2.png').convert_alpha(),
            pygame.image.load('images/right/walk_right3.png').convert_alpha(),
            pygame.image.load('images/right/walk_right4.png').convert_alpha()]
walk_left=[
    pygame.image.load('images/left/walk_left1.png').convert_alpha(),
    pygame.image.load('images/left/walk_left2.png').convert_alpha(),
    pygame.image.load('images/left/walk_left3.png').convert_alpha(),
    pygame.image.load('images/left/walk_left4.png').convert_alpha(),

]
ghost=pygame.image.load('images/ghost.png').convert_alpha()
ghost_list_in_game=[]
player_anim_count=0
bg_x=0

bg_sound=pygame.mixer.Sound('sounds/retro-160315.mp3')
bg_sound.play(loops=-1)
bg_s=0
player_speed=5
player_x=150
player_y=240

is_jump=False
jump_count=8
game_play=True
running= True
label=pygame.font.Font('fonts/Caprasimo-Regular.ttf',40)
score_font=pygame.font.Font('fonts/Caprasimo-Regular.ttf',10)
lose_label=label.render('You lose!',False,(193,196,199))
restart_label=label.render('Restart',False,(115,132,148))
restart_label_rect=restart_label.get_rect(topleft=(180,200))
ghost_timer= pygame.USEREVENT+1
bullets_count=score_font.render('Bullets:',False,(0,0,0))
bullet=pygame.image.load('images/bullet.png').convert_alpha()
bullets=[]
bullets_left=10
score=10
ingame_label = pygame.font.Font('fonts/RobotoCondensed-Bold.ttf', 30)
pygame.time.set_timer(ghost_timer,3000)
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
while running:
    screen.blit(bg, (bg_x,0))
    screen.blit(bg, (bg_x+600,0))
    if game_play:
        player_rect=walk_left[0].get_rect(topleft=(player_x,player_y))
        if ghost_list_in_game:
            for (i,el) in enumerate(ghost_list_in_game):
                screen.blit(ghost,el)
                el.x-=10
                if el.x<-10:
                    ghost_list_in_game.pop(i)
                if player_rect.colliderect(el):
                    game_play=False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x,player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump=True
        else:
            if jump_count>=-8:
                if jump_count>0:
                    player_y-=(jump_count**2)/2
                else:
                    player_y+= (jump_count ** 2) / 2
                jump_count-=1
            else:
                is_jump=False
                jump_count=8
        if keys[pygame.K_LEFT] and player_x>-30:
            player_x-=player_speed
        elif keys[pygame.K_RIGHT] and player_x<550:
            player_x += player_speed


        if player_anim_count==3:
            player_anim_count=0
        else:
            player_anim_count+=1

        bg_x-=2
        if bg_x==-600:
            bg_x=0
        screen.blit(bullets_count, (10,40))
        draw_text(screen, str(score), 18,60,40)
        if bullets:
            for (i,el) in enumerate (bullets):
                screen.blit(bullet,(el.x,el.y))
                el.x+=4

                if el.x>630:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index,ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)
                            score-=1

    else:
        screen.fill((87,89,88))
        bg_sound.stop()
        screen.blit(lose_label,(180,100))
        screen.blit(restart_label, restart_label_rect)
        mouse=pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            game_play=True
            player_x=150
            ghost_list_in_game.clear()
            bullets.clear()
            bg_sound.play(-1)
            bullets_left = 10
            score = 10

    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type== ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(620,240)))
        if game_play and event.type==pygame.KEYUP and event.key==pygame.K_q and bullets_left>0:
            bullets.append(bullet.get_rect(topleft=(player_x+30,player_y+10)))
            bullets_left-=1

    clock.tick(10)

