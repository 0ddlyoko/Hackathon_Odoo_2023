import pygame as pg

# State
# 0 = Login
# 1 = Logged
# 2 = Door
# 3 = Window
# 4 = Bench
# 5 = Door => Cadena
# 6 = Nama
# 7 = END
STATE = 0

# Initialisation de PyGame
pg.init()

# Dimension de la fenêtre
screen_size = (800, 800)

# Création de la fenêtre
screen = pg.display.set_mode(screen_size)

# Chargement des images, font, texts etc
background_img = pg.transform.scale(pg.image.load("images/Background.png"), screen_size)
images = {
    "background": background_img,
    "background_blur": pg.transform.scale(pg.transform.scale(background_img, (60, 60)), screen_size),
    "key": pg.transform.scale(pg.image.load("images/Key.png"), (100, 50)),
    "door": pg.transform.scale(pg.image.load("images/Door.png"), (700, 700)),
    "window": pg.transform.scale(pg.image.load("images/Window.png"), (700, 700)),
    "return": pg.transform.scale(pg.image.load("images/Return.png"), (70, 50)),
    "bench": pg.transform.scale(pg.image.load("images/Bench.png"), (700, 700)),
    "nama": pg.transform.scale(pg.image.load("images/Nama.jpg"), (700, 700)),
    "cadena_small": pg.transform.scale(pg.image.load("images/Cadena.png"), (40, 40)),
    "cadena_big": pg.transform.scale(pg.image.load("images/Cadena.png"), (700, 700)),
    "cadena_up": pg.transform.scale(pg.image.load("images/CadenaUp.png"), (50, 50)),
    "cadena_down": pg.transform.scale(pg.image.load("images/CadenaDown.png"), (50, 50)),
}

font = pg.font.Font(None, 30)

texts = {
    "password": "2. It's dangerous to go alone. %s this.",
    "escaped": font.render("You escaped!", True, (0, 0, 0)),
}

# Position initiale de la clé et de la porte
positions = {
    "key": (50, 70),
    "door": [(500, 430), (600, 640)],
    "door_center": (50, 50),
    "window": [(145,125), (280, 290)],
    "window_center":(50,50),
    "return": [(700, 25), (770, 75)],
    "bench": [(278, 379), (572, 600)],
    "bench_center": (50,50),
    "nama": [(230, 220), (318, 306)],
    "nama_center": (50,50),
    "cadena_small": [(275, 430), (315, 470)],
    "cadena_big": (50, 50),
    "cadena_up": [
        [(260, 440), (310, 490)],
        [(330, 440), (380, 490)],
        [(400, 440), (450, 490)],
        [(470, 440), (520, 490)],
    ],
    "cadena_letter": [
        [(278, 535), (328, 585)],
        [(348, 535), (398, 585)],
        [(418, 535), (468, 585)],
        [(488, 535), (538, 585)],
    ],
    "cadena_down": [
        [(260, 600), (310, 650)],
        [(330, 600), (380, 650)],
        [(400, 600), (450, 650)],
        [(470, 600), (520, 650)],
    ],
}

# Password
current_password = ""
max_char_in_password = 5

# Cadena Password
cadena_current_password = "ABCD"
cadena_final_password = "JINX"

mouse_x, mouse_y = 0, 0


def is_inside(element):
    pos = positions[element]
    return (pos[0][0] <= mouse_x <= pos[1][0]) and (pos[0][1] <= mouse_y <= pos[1][1])


def state0(is_mouse_down):
    global STATE
    # Check if password is correct
    if current_password == "drink":
        STATE = 1
        return

    password = current_password + "_" * (max_char_in_password - len(current_password))
    password = font.render(texts["password"] % password, True, (0, 0, 0))
    temp_surface = pg.Surface((password.get_size()[0] + 20, password.get_size()[1] + 20))
    temp_surface.fill((192, 192, 192))
    temp_surface.blit(password, (10, 10))
    screen.blit(temp_surface, (200, 300))


def state1(is_mouse_down):
    global STATE
    # Check if on door
    if is_inside("door") and is_mouse_down:
        STATE = 2
        return
    if is_inside("window") and is_mouse_down:
        STATE = 3
        return
    # The Game
    screen.blit(images["background"], (0, 0))

    # # Dessin de la clé et de la porte
    # if not key_picked_up:
    #     screen.blit(images["key"], positions["key"])


def state2(is_mouse_down):
    global STATE
    # Draw the door
    screen.blit(images["door"], positions["door_center"])
    # Draw the cadena
    screen.blit(images["cadena_small"], positions["cadena_small"][0])
    # Draw the return button
    screen.blit(images["return"], positions["return"])
    # Check return
    if is_inside("return") and is_mouse_down:
        STATE = 1
        return
    # Check cadena
    is_on_cadena = False
    if (positions["cadena_small"][0][0] <= mouse_x <= positions["cadena_small"][1][0]) and (positions["cadena_small"][0][1] <= mouse_y <= positions["cadena_small"][1][1]):
        is_on_cadena = True
    if is_inside("cadena_small") and is_mouse_down:
        STATE = 5
        return


def state3(is_mouse_down):
    global STATE
    # Draw the door
    screen.blit(images["window"], positions["window_center"])
    
    screen.blit(images["return"], positions["return"])
    # Check return
    if is_inside("return") and is_mouse_down:
        STATE = 1
        return

    if is_inside("bench") and is_mouse_down:
        STATE = 4
        return
    
    if is_inside("nama") and is_mouse_down:
        STATE = 6
        return


def state4(is_mouse_down):
    global STATE
    screen.blit(images["bench"], positions["bench_center"])

    screen.blit(images["return"], positions["return"])
    # Check return
    if is_inside("return") and is_mouse_down:
        STATE = 3
        return


def state5(is_mouse_down):
    global STATE, cadena_current_password
    # Draw the door
    screen.blit(images["door"], positions["door_center"])
    # Draw the cadenas
    screen.blit(images["cadena_small"], positions["cadena_small"][0])
    screen.blit(images["cadena_big"], positions["cadena_big"])
    # Draw the return button
    screen.blit(images["return"], positions["return"])
    # Draw up buttons
    for up in positions["cadena_up"]:
        screen.blit(images["cadena_up"], up[0])
    # Draw letters
    for count, letter in enumerate(cadena_current_password):
        screen.blit(font.render(letter, True, (0, 0, 0)), positions["cadena_letter"][count])
    # Draw down buttons
    for up in positions["cadena_down"]:
        screen.blit(images["cadena_down"], up[0])
    if is_mouse_down:
        if cadena_current_password == cadena_final_password:
            STATE = 7
            return
        # Check return
        is_on_return = False
        if is_inside("return"):
            STATE = 2
            return
        # Check letter up
        for count, up_pos in enumerate(positions["cadena_up"]):
            is_up = False
            if (up_pos[0][0] <= mouse_x <= up_pos[1][0]) and (up_pos[0][1] <= mouse_y <= up_pos[1][1]):
                is_up = True
            if is_up:
                # Increase this letter
                letter = ord(cadena_current_password[count]) + 1
                if letter == 91:
                    letter = 65  # 'A'
                old_password_lst = list(cadena_current_password)
                old_password_lst[count] = chr(letter)
                cadena_current_password = ''.join(old_password_lst)
        # Check letter down
        for count, down_pos in enumerate(positions["cadena_down"]):
            is_down = False
            if (down_pos[0][0] <= mouse_x <= down_pos[1][0]) and (down_pos[0][1] <= mouse_y <= down_pos[1][1]):
                is_down = True
            if is_down:
                # Increase this letter
                letter = ord(cadena_current_password[count]) - 1
                if letter == 64:
                    letter = 90  # 'Z'
                old_password_lst = list(cadena_current_password)
                old_password_lst[count] = chr(letter)
                cadena_current_password = ''.join(old_password_lst)


def state6(is_mouse_down):
    global STATE
    # Draw the door
    screen.blit(images["nama"], positions["nama_center"])
    # Draw the return button
    screen.blit(images["return"], positions["return"])
    # Check return
    if is_inside("return") and is_mouse_down:
        STATE = 3
        return


def state7(is_mouse_down):
    print("END :D")
    pass


# Boucle principale
while True:
    # Event
    is_mouse_down = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            is_mouse_down = True
        if event.type == pg.KEYDOWN:
            if event.key == 8:
                # Return pressed
                if len(current_password) == 0:
                    continue
                current_password = current_password[:-1]
                # print("Return")
            elif 97 <= event.key <= 122:
                # a => z
                key_name = pg.key.name(event.key)
                if len(current_password) == max_char_in_password:
                    continue
                current_password += chr(event.key)

    # Mouse position
    mouse_x, mouse_y = pg.mouse.get_pos()

    # Check if mouse is on the key
    # if (positions["key"][0] < mouse_x < positions["key"][0] + 32) and (positions["key"][1] < mouse_y < positions["key"][1] + 32):
    #     # Vérifie si le bouton est appuyé
    #     if is_mouse_down:
    #         # Ramasse la clé
    #         key_picked_up = True

    # UI
    # Reset screen (+ blur image)
    screen.blit(images["background_blur"], (0, 0))

    if STATE == 0:
        state0(is_mouse_down)
    elif STATE == 1:
        state1(is_mouse_down)
    elif STATE == 2:
        state2(is_mouse_down)
    elif STATE == 3:
        state3(is_mouse_down)
    elif STATE == 4:
        state4(is_mouse_down)
    elif STATE == 5:
        state5(is_mouse_down)
    elif STATE == 6:
        state6(is_mouse_down)
    elif STATE == 7:
        state7(is_mouse_down)
    # Print mouse position
    screen.blit(font.render(f"{mouse_x} - {mouse_y}", True, (255, 255, 255)), (400, 20))

    # Mise à jour de l'écran
    pg.display.flip()
