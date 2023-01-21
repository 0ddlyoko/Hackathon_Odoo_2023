import pygame as pg

# State
# 0 = Login
# 1 = Logged
# 2 = Door
STATE = 1

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
}

font = pg.font.Font(None, 30)

texts = {
    "password": "1. It's dangerous to go alone. %s this.",
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
}

# Password
current_password = ""
max_char_in_password = 5

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
    is_on_door = False
    if is_inside("door"):
        is_on_door = True
    if is_on_door and is_mouse_down:
        STATE = 2
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
    # Draw the return button
    screen.blit(images["return"], positions["return"])
    # Check return
    is_on_return = False
    if is_inside("return"):
        is_on_return = True
    if is_on_return and is_mouse_down:
        STATE = 1
        return


def state3(is_mouse_down):
    global STATE
    is_on_window = False
    if is_inside("window"):
        is_on_window = True
    if is_on_window and is_mouse_down:
        STATE = 4
        return
    # The Game
    screen.blit(images["background"], (0, 0))

def state4(is_mouse_down):
    global STATE
    # Draw the door
    screen.blit(images["window"], positions["window_center"])
    
    screen.blit(images["return"], positions["return"])
    # Check return
    is_on_return = False
    if is_inside("return"):
        is_on_return = True
    if is_on_return and is_mouse_down:
        STATE = 1
        return

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
    if STATE == 1:
        state1(is_mouse_down)
    if STATE == 2:
        state2(is_mouse_down)
    if STATE == 1:
        state3(is_mouse_down)
    if STATE == 4:
        state4(is_mouse_down)
    # Print mouse position
    screen.blit(font.render(f"{mouse_x} - {mouse_y}", True, (255, 255, 255)), (400, 20))

    # Mise à jour de l'écran
    pg.display.flip()
