import math

import pygame as pg

# State
# 0 = Login
# 1 = Main
# 2 = Door
# 3 = Window
# 4 = Bench
# 5 = Door => Cadena
# 6 = Nama
# 7 = END
# 8 = Main (2)
# 9 = Roof
# 10 = Main (2) => Journal
# 11 = Clock
# 12 = Cactus Paper
STATE = 1

# Initialisation de PyGame
pg.init()

# Dimension de la fenêtre
screen_size = (800, 800)
center = (400, 400)

# Création de la fenêtre
screen = pg.display.set_mode(screen_size)

# Chargement des images, font, texts etc
images = {
    "background": pg.transform.scale(pg.image.load("images/Background.png"), screen_size),
    "background_blur": pg.transform.scale(pg.transform.scale(pg.image.load("images/Background.png"), (60, 60)), screen_size),
    "background_2": pg.transform.scale(pg.image.load("images/Background_2.png"), screen_size),
    "background_2blur": pg.transform.scale(pg.transform.scale(pg.image.load("images/Background_2.png"), (60, 60)), screen_size),
    "background_roof": pg.transform.scale(pg.image.load("images/Roof_2.png"), screen_size),
    "key": pg.transform.scale(pg.image.load("images/Key.png"), (100, 50)),
    "door": pg.transform.scale(pg.image.load("images/Door.png"), (700, 700)),
    "window": pg.transform.scale(pg.image.load("images/Window.png"), (700, 700)),
    "return": pg.transform.scale(pg.image.load("images/Return.png"), (70, 50)),
    "bench": pg.transform.scale(pg.image.load("images/Bench.png"), (700, 700)),
    "nama": pg.transform.scale(pg.image.load("images/Nama.jpg"), (700, 700)),
    "cadena_small": pg.transform.scale(pg.image.load("images/Cadena.png"), (40, 40)),
    "cadena_big": pg.transform.scale(pg.image.load("images/Cadena.png"), (700, 700)),
    "arrow_up": pg.transform.scale(pg.image.load("images/Arrow_Up.png"), (50, 50)),
    "arrow_down": pg.transform.scale(pg.image.load("images/Arrow_Down.png"), (50, 50)),
    "arrow_left": pg.transform.scale(pg.image.load("images/Arrow_Left.png"), (50, 50)),
    "arrow_right": pg.transform.scale(pg.image.load("images/Arrow_Right.png"), (50, 50)),
    "journal": pg.transform.scale(pg.image.load("images/Journal.jpg"), (700, 700)),
    "clock": pg.transform.scale(pg.image.load("images/Clock.jpg"), (700, 700)),
    "cactus_paper": pg.transform.scale(pg.image.load("images/CactusPaper.png"), (700, 700)),
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
    "window": [(145, 125), (280, 290)],
    "window_center": (50, 50),
    "return": [(700, 25), (770, 75)],
    "bench": [(278, 379), (572, 600)],
    "bench_center": (50, 50),
    "nama": [(230, 220), (318, 306)],
    "nama_center": (50, 50),
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
    "arrow_right": [(700, 25), (770, 75)],
    "arrow_left": [(30, 25), (100, 75)],
    "state_8_door": [(260, 330), (350, 500)],
    "roof": [(440, 250), (580, 410)],
    "roof_key": [(640, 490), (800, 660)],
    "state_8_box": [(150, 470), (280, 560)],
    "journal": [(450, 520), (530, 580)],
    "journal_big": (50, 50),
    "clock": [(360, 250), (400, 330)],
    "clock_big": (49, 52),
    "clock_message": (330, 280),
    "cactus_paper": [(590, 530), (650, 720)],
    "cactus_paper_big": (50, 50),
}

# Password
current_password = ""
max_char_in_password = 5

# Cadena Password
cadena_current_password = "AAAA"
cadena_final_password = "JINX"

# Keys
has_first_key = False
is_second_box_locked = True
has_second_key = False

mouse_x, mouse_y = 0, 0
message_to_display = ""


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
    global STATE, message_to_display
    screen.blit(images["background"], (0, 0))
    screen.blit(images["arrow_right"], positions["arrow_right"])
    screen.blit(images["arrow_left"], positions["arrow_left"])
    if is_mouse_down:
        if is_inside("door"):
            STATE = 2
            return
        if is_inside("window"):
            STATE = 3
            return
        if is_inside("arrow_right"):
            STATE = 8
            return
        if is_inside("arrow_left"):
            STATE = 8
            return
        if is_inside("roof"):
            STATE = 9
            return
        if is_inside("clock"):
            STATE = 11
            return
        if is_inside("cactus_paper"):
            clicked_on_cactus = True


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
    if is_mouse_down:
        if is_inside("cadena_small"):
            STATE = 5
            return


def state3(is_mouse_down):
    global STATE
    # Draw the door
    screen.blit(images["window"], positions["window_center"])
    
    screen.blit(images["return"], positions["return"])
    if is_mouse_down:
        # Check return
        if is_inside("return"):
            STATE = 1
            return
        if is_inside("bench"):
            STATE = 4
            return
        if is_inside("nama"):
            STATE = 6
            return


def state4(is_mouse_down):
    global STATE
    screen.blit(images["bench"], positions["bench_center"])
    screen.blit(images["return"], positions["return"])

    if is_mouse_down:
        if is_inside("return"):
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
        screen.blit(images["arrow_up"], up[0])
    # Draw letters
    for count, letter in enumerate(cadena_current_password):
        screen.blit(font.render(letter, True, (0, 0, 0)), positions["cadena_letter"][count])
    # Draw down buttons
    for up in positions["cadena_down"]:
        screen.blit(images["arrow_down"], up[0])
    if is_mouse_down:
        if cadena_current_password == cadena_final_password:
            STATE = 7
            return
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
    global STATE, message_to_display
    message_to_display = "I wonder what he is watching"
    # Draw the door
    screen.blit(images["nama"], positions["nama_center"])
    # Draw the return button
    screen.blit(images["return"], positions["return"])
    if is_mouse_down:
        # Check return
        if is_inside("return"):
            STATE = 3
            message_to_display = ""
            return


def state7(is_mouse_down):
    print("END :D")
    pass


def state8(is_mouse_down):
    global STATE, message_to_display, has_first_key, has_second_key, is_second_box_locked
    screen.blit(images["background_2"], (0, 0))
    screen.blit(images["arrow_left"], positions["arrow_left"])
    screen.blit(images["arrow_right"], positions["arrow_right"])
    if not is_inside("state_8_door") and not is_inside("state_8_box"):
        message_to_display = ""
    if is_mouse_down:
        if is_inside("arrow_left"):
            STATE = 1
            return
        if is_inside("arrow_right"):
            STATE = 1
            return
        if is_inside("state_8_door"):
            message_to_display = "There is nothing there"
            return
        if is_inside("state_8_box"):
            if has_second_key:
                message_to_display = "There is nothing more there"
            elif not has_first_key:
                message_to_display = "It's locked"
            elif is_second_box_locked:
                is_second_box_locked = False
                message_to_display = "It's now unlocked!"
            else:
                # TODO Add puzzle
                has_second_key = True
                message_to_display = "You got a key!"
        if is_inside("journal"):
            STATE = 10
            return


def state9(is_mouse_down):
    global STATE, has_first_key, message_to_display
    screen.blit(images["background_roof"], (0, 0))
    screen.blit(images["return"], positions["return"])
    if not is_inside("roof_key"):
        message_to_display = ""
    if is_mouse_down:
        # Check return
        if is_inside("return"):
            STATE = 1
            return
        if is_inside("roof_key"):
            if has_first_key:
                message_to_display = "There is nothing more!"
            else:
                has_first_key = True
                message_to_display = "You got a key!"


def state10(is_mouse_down):
    global STATE
    screen.blit(images["background_2blur"], (0, 0))
    screen.blit(images["journal"], positions["journal_big"])
    screen.blit(images["return"], positions["return"])
    if is_mouse_down:
        # Check return
        if is_inside("return"):
            STATE = 8
            return


minute_hand_angle = math.radians(180)
hour_hand_angle = math.radians(90)
correct_clock_answer = (118, 153)
has_correct_clock = False
def state11(is_mouse_down):
    global STATE, minute_hand_angle, hour_hand_angle, has_correct_clock, message_to_display
    screen.blit(images["background_blur"], (0, 0))
    screen.blit(images["return"], positions["return"])
    screen.blit(images["clock"], positions["clock_big"])
    pg.draw.line(screen, (0, 0, 0), center, (400 + math.cos(minute_hand_angle) * 250, 400 + math.sin(minute_hand_angle) * 250), 4)
    pg.draw.line(screen, (0, 0, 0), center, (400 + math.cos(hour_hand_angle) * 200, 400 + math.sin(hour_hand_angle) * 200), 4)
    if has_correct_clock:
        message_to_display = "After setting correctly the time, a message appears"
        screen.blit(font.render("1. Multijoueur", True, (0, 0, 0)), positions["clock_message"])

    if is_mouse_down:
        # Check return
        if is_inside("return"):
            STATE = 1
            return
        if not has_correct_clock:
            angle = math.atan2(mouse_y - 400, mouse_x - 400)
            if pg.mouse.get_pressed()[0]:
                hour_hand_angle = angle
            elif pg.mouse.get_pressed()[2]:
                minute_hand_angle = angle
            hour = int(math.degrees(hour_hand_angle))
            minute = int(math.degrees(minute_hand_angle))
            if correct_clock_answer[0] - 10 <= hour <= correct_clock_answer[0] + 10 and correct_clock_answer[1] - 10 <= minute <= correct_clock_answer[1] + 10:
                has_correct_clock = True


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
    elif STATE == 8:
        state8(is_mouse_down)
    elif STATE == 9:
        state9(is_mouse_down)
    elif STATE == 10:
        state10(is_mouse_down)
    elif STATE == 11:
        state11(is_mouse_down)
    elif STATE == 12:
        state12(is_mouse_down)
    # Print text or position
    display_message = message_to_display if message_to_display != "" else f"{mouse_x} - {mouse_y}"
    font_message = font.render(display_message, True, (255, 255, 255))
    screen.blit(font_message, (400 - (font_message.get_size()[0] / 2), 20))

    # Mise à jour de l'écran
    pg.display.flip()
