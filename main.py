import pygame as pg

# State
# 0 = Login
# 1 = Logged
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
    "door": pg.transform.scale(pg.image.load("images/Door.png"), (100, 50)),
}

font = pg.font.Font(None, 30)

texts = {
    "password": "1. It's dangerous to go alone. %s this.",
    "escaped": font.render("You escaped!", True, (0, 0, 0)),
}

# Position initiale de la clé et de la porte

key_x = 50
key_y = 50
door_x = 700
door_y = 500

# Variable pour stocker l'état de la clé (ramassée ou non)
key_picked_up = False

# Password
current_password = ""
max_char_in_password = 5

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
                # print(event.key, key_name)

    # Récupération de la position de la souris
    mouse_x, mouse_y = pg.mouse.get_pos()

    # Vérifie si la souris est sur la clé
    if (key_x < mouse_x < key_x + 32) and (key_y < mouse_y < key_y + 32):
        # Vérifie si le bouton est appuyé
        if is_mouse_down:
            # Ramasse la clé
            key_picked_up = True
            key_x = -100
            key_y = -100

    # UI
    # Effacement de l'écran
    screen.fill((255, 255, 255))
    if STATE == 0:
        # Check if password is correct
        if current_password == "drink":
            STATE = 1
        else:
            screen.blit(images["background_blur"], (0, 0))
            password = current_password + "_" * (max_char_in_password - len(current_password))
            password = font.render(texts["password"] % password, True, (0, 0, 0))
            temp_surface = pg.Surface((password.get_size()[0] + 20, password.get_size()[1] + 20))
            temp_surface.fill((192, 192, 192))
            temp_surface.blit(password, (10, 10))
            screen.blit(temp_surface, (200, 300))
    if STATE == 1:
        screen.blit(images["background"], (0, 0))

        # Dessin de la clé et de la porte
        if not key_picked_up:
            screen.blit(images["key"], (key_x, key_y))
        screen.blit(images["door"], (door_x, door_y))

        # Vérifie si la clé est ramassée et si la souris est sur la porte
        if key_picked_up and (door_x < mouse_x < door_x + 64) and (door_y < mouse_y < door_y + 64):
            # Affiche un message de victoire
            screen.blit(texts["escaped"], (350, 300))

    # Mise à jour de l'écran
    pg.display.flip()
