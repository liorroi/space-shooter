import os


end_windows_height = 530
WIDTH = 1020
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLUE_2 = (0, 128, 255)
# middle line setting
middle_line_width = 20
# shoot setting
shoot_delay = 100
speed = 10
# background
background_image_name = 'img\\background.png'
middle_line_color = BLACK
# player setting
start_point = (200,  500)
# button list (those in the size of windows ) setting
button_size = (100, 25)
# text button setting
text_size = 20
font = 'arial'
# background width of button area
background_button_width = 100
# button color
back_ground_button_color = BLUE_2
letter_color = BLUE
# color when click
back_ground_click_color = WHITE
letter_click_color = BLUE
# image folders
image_folder = os.path.join('img', '')
rocket_image_folder = os.path.join(image_folder, 'rocks')
bullet_image_folder = os.path.join(image_folder, 'bullets')
player_image_folder = os.path.join(image_folder, 'players')
explusion_images = os.path.join(image_folder, 'explosion')
# information setting
letter_size = 30
# its button_right point
start_information_position = (100, HEIGHT - 20)
space_between_items = 20
information_color = WHITE
# start game windows
start_game_letter_color = WHITE
play_button_position = (WIDTH / 2, HEIGHT / 2.5)
play_button_letter_size = 120
# bomb setting
bomb_frame = 50
bomb_images_size = (50, 50)
