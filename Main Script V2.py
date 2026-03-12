#libraries
import sys
from pygame import mouse
import pygame
import random

#variables
x, y = 800, 700
tile_width = x/2
tile_height = y/2
clicked = False
trainer_x, trainer_y = 375.0, 300.0       #trainer start coordinates
trainer_speed = 0.3                        #walk speed (pixels per ms)
trainer_width, trainer_height = 120,140    #trainer proportions
trainer_frame_width, trainer_frame_height = 121, 126      #actual frame size (sprites don't start at 0,0)
trainer_frame_offset_x, trainer_frame_offset_y = 177, 45  #black padding offset in sprite sheet
facing = 'down'
animation_speed = 0.005                    #animation speed (frames per ms)
frame_index = 0.0                          #initialise frame index
pokemon_frame_offset_y = 0
pokemon_frame_offset_x = 0
pokemon_frame_width = 210
pokemon_frame_height = 228
pokemon_x, pokemon_y = random.randint(200,x-200), random.randint(200,y-200)     #choose random coordinates for it to spawn at
while (trainer_x - 100 < pokemon_x < trainer_x + 100) and (trainer_y - 100 < pokemon_y < trainer_y + 100):  #make sure it doesnt spawn on trainer
    pokemon_x, pokemon_y = random.randint(200, x - 200), random.randint(200, y - 200)
pokeball_thrown = False
pokeball_height, pokeball_width = 40,40
pokeball_flip = False
pokemon_caught = False
throw_start = 0                            #tracks when the pokeball was thrown

#initialisation
pygame.init()
pygame.display.set_caption('Pokemon game')
screen = pygame.display.set_mode((x, y))
font = pygame.font.SysFont(name="Arcade Classic", size=90)
clock = pygame.time.Clock()               #clock for delta time

#load images
    #map
background = pygame.image.load("maps/grassy.jpg")
background = pygame.transform.scale(background, (tile_width, tile_height))
    #sprite
trainer_sheet = pygame.image.load("images/trainer_sheet.png").convert_alpha()
animations = {'down':[],'left':[],'right':[],'up':[]}
direction_rows = {0:'down', 1:'left', 2:'right', 3:'up'}
for row in range(4):
    direction = direction_rows[row]
    for col in range(4):
        frame = trainer_sheet.subsurface(pygame.Rect(
            trainer_frame_offset_x + col * trainer_frame_width,
            trainer_frame_offset_y + row * trainer_frame_height,
            trainer_frame_width,
            trainer_frame_height
                                ))

        frame = pygame.transform.scale(frame, (trainer_width, trainer_height))  #pre-scale once
        animations[direction].append(frame)
    #pokemon
pokemon_sheet = pygame.image.load("images/3d_starter_sheet.png").convert_alpha()        #load in the image into a variable
pokemon_pool = []
for row in range(4):
    for col in range(6):
        frame = pokemon_sheet.subsurface(pygame.Rect(
            pokemon_frame_offset_x + col * pokemon_frame_width,
            pokemon_frame_offset_y + row * pokemon_frame_height,
            pokemon_frame_width, pokemon_frame_height
        ))
        frame = pygame.transform.scale(frame, (trainer_width, trainer_height))  #pre-scale once
        pokemon_pool.append(frame)              #add each respective pokemon starter image to the pool
pokemon_frame = random.choice(pokemon_pool)  # choose a random pokemon to appear (from pool)
if random.randint(0, 1):
    pokeball_flip = True
    pokemon_frame = pygame.transform.flip(pokemon_frame, True, False)  # horizontal flip only
    #pokeball
pokeball = pygame.image.load("images/pokeball.png").convert_alpha()
pokeball = pygame.transform.scale(pokeball, (pokeball_width, pokeball_height))

#event loop
while True:
    dt = clock.tick_busy_loop(60)          #more precise than tick() — burns CPU but eliminates timer jitter

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            #throw pokeball on single keypress, only if close enough and not already thrown
            if event.key == pygame.K_SPACE and not pokeball_thrown and not pokemon_caught:
                if (pokemon_x - 100 < trainer_x < pokemon_x + 100) and (pokemon_y - 100 < trainer_y < pokemon_y + 100):
                    pokeball_thrown = True
                    throw_start = pygame.time.get_ticks()   #snapshot the time of the throw
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = True
                mx, my = mouse.get_pos()

    keys = pygame.key.get_pressed()
    moving = False

    #resolve the throw after 1.5s — decide if caught or not
    if pokeball_thrown and pygame.time.get_ticks() - throw_start > 1500:
        pokeball_thrown = False
        pokemon_caught = random.choice([True, False])   #50/50 catch chance

    #movement block — locked while pokeball is in the air
    if not pokeball_thrown:
        if keys[pygame.K_LEFT] and trainer_x > 0 and not(pokemon_x < trainer_x < pokemon_x + 80 and pokemon_y - 80 < trainer_y < pokemon_y + 80):
            trainer_x -= trainer_speed * dt
            facing = 'left'
            moving = True

        if keys[pygame.K_RIGHT] and trainer_x < x - trainer_width and not(pokemon_x - 80 < trainer_x < pokemon_x and pokemon_y - 80 < trainer_y < pokemon_y + 80):
            trainer_x += trainer_speed * dt
            facing = 'right'
            moving = True

        if keys[pygame.K_UP] and trainer_y > 0 and not(pokemon_y  < trainer_y < pokemon_y + 80 and pokemon_x-40 < trainer_x < pokemon_x + 40):
            trainer_y -= trainer_speed * dt
            facing = 'up'
            moving = True

        if keys[pygame.K_DOWN] and trainer_y < y - trainer_height and not(pokemon_y - 80 < trainer_y < pokemon_y and pokemon_x-40 < trainer_x < pokemon_x + 40):
            trainer_y += trainer_speed * dt
            facing = 'down'
            moving = True

    #animation block
    if moving:
        frame_index = (frame_index + animation_speed * dt) % 4
    else:
        frame_index = 0.0

    screen.fill((40, 80, 40))

    #upon mouse click...
    if clicked:
        print(mx, my)
        clicked = False

    #print the map background
    for row in range(2):
        for col in range(2):
            screen.blit(background, (col * tile_width, row * tile_height))

    #print the trainer — round coords to avoid jitter
    trainer_frame = animations[facing][int(frame_index)]
    screen.blit(
        trainer_frame,
        (round(trainer_x),
         round(trainer_y))
    )
    if not pokemon_caught:
        #print the pokemon — swaps to pokeball while thrown, disappears if caught
        if not pokeball_thrown:
            screen.blit(
                pokemon_frame,
                (pokemon_x, pokemon_y))
        else:
            #print(pokeball)
            screen.blit(
                pokeball, (pokemon_x + 40, pokemon_y + 80)
            )
    if pokemon_caught:
        # print caught notification at top of screen
        text = font.render("Caught!", True, (255, 255, 255))  # text in notification
        caught_pill = pygame.Surface((text.get_width() + 20, text.get_height() + 10),
                                     pygame.SRCALPHA)  # notification background
        caught_pill.fill((0, 0, 0, 150))
        screen.blit(caught_pill, (400 - caught_pill.get_width() // 2, 20))
        screen.blit(text, (400 - text.get_width() // 2, 25))


    #the hint (that says [space] to throw
    font = pygame.font.SysFont("couriernew",20, bold=True)        #font of hint
    hint = font.render("[SPACE] to catch", True, (255,255,255))
    #background pill of hint
    pill = pygame.Surface((hint.get_width() + 2, hint.get_height() + 2), pygame.SRCALPHA)    #sets up the background pill (SCRALPHA makes it transparent)
    pill.fill((0, 0, 0, 150))     #colour of pill
    screen.blit(pill, (x - 200, y - 50))    #pill placement
        # then draw text on top
    screen.blit(hint, (x - 200, y - 50))

    pygame.display.flip()

#todo 1. get catching working ✔️
#todo 2. add in a caught message (temporary banner) ✔️
#todo 3. add in a pokeball counter
#todo 4. add in multiple spawning pokemon
#todo 5. add in a pokedex (with shadows for undiscovered pokemon) and names of pokemon too
