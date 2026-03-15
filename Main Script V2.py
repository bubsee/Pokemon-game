#libraries
import sys
from pygame import mouse
import pygame
import random

#functions
def reset_pokemon_spawn():
    global pokemon_caught, caught_time, pokemon_x, pokemon_y, pokemon_frame
    pokemon_caught = False
    caught_time = 0
    pokemon_x, pokemon_y =  random.randint(200,x-200), random.randint(200,y-200)     #choose random coordinates for it to spawn at
    while (trainer_x - 100 < pokemon_x < trainer_x + 100) and (trainer_y - 100 < pokemon_y < trainer_y + 100):  #make sure it doesnt spawn on trainer
        pokemon_x, pokemon_y = random.randint(200, x - 200), random.randint(200, y - 200)# new random position
    pokemon_frame = random.choice(pokemon_pool)  # new random pokemon

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
pokemon_width, pokemon_height = 90, 100
pokemon_x, pokemon_y = random.randint(200,x-200), random.randint(200,y-200)     #choose random coordinates for it to spawn at
while (trainer_x - 100 < pokemon_x < trainer_x + 100) and (trainer_y - 100 < pokemon_y < trainer_y + 100):  #make sure it doesnt spawn on trainer
    pokemon_x, pokemon_y = random.randint(200, x - 200), random.randint(200, y - 200)
pokeball_thrown = False
pokeball_height, pokeball_width = 20,20
pokeball_flip = False
pokemon_caught = False
throw_start = 0                            #tracks when the pokeball was thrown
pokeball_count = 5
caught_time = 0
pokedex_unlocked = False
pokedex_open = False
scroll_y = 0
pokemon_names = []          #list of corresponding pokemon names

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
        frame = pygame.transform.scale(frame, (pokemon_width, pokemon_height))  #pre-scale once
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

    #map screen
    if pokedex_open == False:
        dt = clock.tick_busy_loop(60)          #more precise than tick() — burns CPU but eliminates timer jitter

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                #TAB - open pokedex
                if event.key == pygame.K_TAB and pokedex_unlocked == True:
                    pokedex_open = True

                #SPACE
                #throw pokeball on single keypress, only if close enough and not already thrown
                if event.key == pygame.K_SPACE and not pokeball_thrown and not pokemon_caught and pokeball_count > 0:
                    if (pokemon_x - 100 < trainer_x < pokemon_x + 100) and (pokemon_y - 100 < trainer_y < pokemon_y + 100):
                        pokeball_thrown = True
                        throw_start = pygame.time.get_ticks()   #snapshot the time of the throw
                        pokeball_count -= 1

                if event.key == pygame.K_SPACE and pokeball_count <= 0:
                    print('not enogh pokeballs')

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

        #movement block — locked while pokeball is catching pokemon
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
                    pokeball, (pokemon_x + 30, pokemon_y + 50)
                )
        if pokemon_caught:
            if caught_time == 0:
                caught_time = pygame.time.get_ticks()      #starts timer for when to fade out 'caught' notification
            pokedex_unlocked = True

            elapsed = pygame.time.get_ticks() - caught_time      #time elapsed where 'caught' is on screen
            alpha = max(0, 300 - elapsed // 8)           #turns time elapsed into a computable transparency to be used on caught text and the pill behind it

            font = pygame.font.SysFont("couriernew", 25, bold=True)
            text = font.render("Caught!", True, (255, 255, 100))
            caught_pill = pygame.Surface((text.get_width() + 20, text.get_height() + 10), pygame.SRCALPHA)
            caught_pill.fill((0, 0, 0, 150))
            text.set_alpha(alpha)               #sets the transparency to alpha
            caught_pill.set_alpha(alpha)
            screen.blit(caught_pill, (400 - caught_pill.get_width() // 2, 20))
            screen.blit(text, (400 - text.get_width() // 2, 25))
            if alpha == 0:
                reset_pokemon_spawn()

        #SPACE hint (that says [space] to throw
        font = pygame.font.SysFont("couriernew",19, bold=True)        #font of hint
        hint = font.render("[SPACE] catch", True, (255,255,255))
        #background pill of hint
        pill = pygame.Surface((hint.get_width() + 2, hint.get_height() + 2), pygame.SRCALPHA)    #sets up the background pill (SCRALPHA makes it transparent)
        pill.fill((0, 0, 0, 150))     #colour of pill
        screen.blit(pill, (x - 150, y - 70))    #pill placement
            # then draw text on top
        screen.blit(hint, (x - 150, y - 70))


        # TAB hint (that says [space] to throw
        if pokedex_unlocked:
            tab_font = pygame.font.SysFont("couriernew", 15, bold=True)  # font of hint
            tab_hint = font.render("[TAB] pokédex", True, (255, 255, 255))
            # background pill of hint
            tab_pill = pygame.Surface((tab_hint.get_width() + 2, tab_hint.get_height() + 2),
                                  pygame.SRCALPHA)  # sets up the background pill (SCRALPHA makes it transparent)
            tab_pill.fill((0, 0, 0, 150))  # colour of pill
            screen.blit(tab_pill, (x - 150, y - 40))  # pill placement
            # then draw text on top
            screen.blit(tab_hint, (x - 150, y - 40))

        #pokeball counter top left
        pokeball_font = pygame.font.SysFont('couriernew',20, bold=True)
        pokeball_counter = font.render(f'{pokeball_count}', True, (255, 255, 255))
        if pokeball_count == 0:
            pokeball_counter = font.render(f'{pokeball_count}', True, (255, 0,0))                  #counter goes red if 0 pokeballs
        pokeball_pill = pygame.Surface((60, 20), pygame.SRCALPHA)         #pokeball counter pill dimensions
        pokeball_pill.fill((0,0,0, 150))                                       #pokemon colour
        screen.blit(pokeball_pill, (5,10))
        pokeball = pygame.transform.scale(pokeball, (30,30))          #enlarge pokeball a bit
        screen.blit(pokeball,(4,2))
        screen.blit(pokeball_counter, (35, 10))
        pokeball = pygame.transform.scale(pokeball, (pokeball_width, pokeball_height))     #change pokeball dimensions back

        # pokdex screen
    if pokedex_open == True:
        dt = clock.tick_busy_loop(60)  # more precise than tick() — burns CPU but eliminates timer jitter

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # TAB - close pokedex
                if event.key == pygame.K_TAB:
                    pokedex_open = False

            # mouse wheel scrolling
            if event.type == pygame.MOUSEWHEEL and (scroll_y + event.y * 20 <= 0 or scroll_y + event.y * 20 > 100):
                scroll_y += event.y * 20  # change scroll amount

        screen.fill((100, 30, 30))

        # draw each row of pokemon
        incrementer = 0
        for i in range(len(pokemon_pool)):
            pokemon_image = pokemon_pool[i]
            pokemon_image = pygame.transform.scale(pokemon_image, (250, 250))
            #if pokemon is not unlocked
            pokemon_image = pokemon_image.copy()
            pokemon_image.fill((0, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
            pokemon_name = font.render("?", True, (0,0,0))

            '''#if pokemon is NOT unlocked
            pokemon_name = font.render(pokemon_names[i], True, (0, 0, 0))'''

            font = pygame.font.SysFont("couriernew", 40, bold=True)
            incrementer = (incrementer +1)%3
            x_pos = incrementer * 275
            if incrementer == 1:
                y_pos = i * 100 + scroll_y  # position of each letter (moves with scroll

            screen.blit(pokemon_image, (x_pos, y_pos))
            screen.blit(pokemon_name, (x_pos + 115 , y_pos + 250))

        pygame.display.update()
        clock.tick(60)


    pygame.display.flip()

#todo 1. get catching working ✔️
#todo 2. add in a caught message (temporary banner) ✔️
#todo 3. add in a pokeball counter ✔️
#todo 4. make the 'caught' banner fade away ✔️
#todo 5. add in multiple spawning pokemon ✔️
#todo 6. make it so you can run over where the caught pokemon was again ✔️
#todo 7. add in a pokedex button ✔️
#todo 8. add in a notification explaining the pokedex after first pokemon catch
#todo 9. add stars around pokemon and catch animation (wiggle)
#todo 10. add in pokedex (with shadows for undiscovered pokemon) and names of pokemon too (scrollable and sorrtred into generations) i.e gen 1 bulbasaur charizard squirtle, gen 2...
#todo 11. add in opening screen (fades in) and a login (which tracks pokedex)