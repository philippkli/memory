import pygame
import random
import csv
import sys
from button import Button

# Initialize Pygame
pygame.init()

# Set up display
FPS = 30
screen_width = 512
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Memory Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load card names from CSV
def load_card_names(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        card_list = [row[0] for row in reader]
        random.shuffle(card_list)
        return card_list

# Main menu using Button class
def main_menu():
    button_width = 200
    button_height = 50
    # Center the buttons horizontally
    x_position = (screen_width - button_width) / 2

    # Define buttons with new centered positions
    play_4x4_button = Button(x_position, 150, button_width, button_height, WHITE, BLUE, 'Play 4x4', 22)
    play_8x8_button = Button(x_position, 225, button_width, button_height, WHITE, BLUE, 'Play 8x8', 22)
    exit_button = Button(x_position, 300, button_width, button_height, WHITE, RED, 'Exit', 22)
    
    while True:
        screen.fill(GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_4x4_button.is_pressed(event.pos, pygame.mouse.get_pressed()):
                    return 4
                elif play_8x8_button.is_pressed(event.pos, pygame.mouse.get_pressed()):
                    return 6
                elif exit_button.is_pressed(event.pos, pygame.mouse.get_pressed()):
                    pygame.quit()
                    sys.exit()

        # Draw buttons on the screen centered
        screen.blit(play_4x4_button.image, (play_4x4_button.x, play_4x4_button.y))
        screen.blit(play_8x8_button.image, (play_8x8_button.x, play_8x8_button.y))
        screen.blit(exit_button.image, (exit_button.x, exit_button.y))

        pygame.display.update()

# Main game function
def main(grid_size):
    CARD_WIDTH, CARD_HEIGHT = 64, 64
    ROWS, COLS = grid_size, grid_size
    WIDTH, HEIGHT = CARD_WIDTH * COLS, CARD_HEIGHT * ROWS
    screen = pygame.display.set_mode((512, 512))

    card_names = load_card_names('_cards.csv')[:grid_size**2//2]
    card_images = []
    card_back = pygame.image.load("card_back.png").convert_alpha()
    card_back = pygame.transform.scale(card_back, (CARD_WIDTH, CARD_HEIGHT))

    for name in card_names:
        img = pygame.image.load(name).convert_alpha()
        img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
        card_images.append(img)

    grid = []
    flipped_cards = []
    temp_flipped_cards = []
    matched_pairs = 0

    def create_grid():
        nonlocal grid
        cards = list(range(len(card_names))) * 2
        random.shuffle(cards)
        grid = [cards[i:i + COLS] for i in range(0, len(cards), COLS)]

    def draw_grid():
        for row in range(ROWS):
            for col in range(COLS):
                card_pos = (row, col)
                card_index = grid[row][col]
                if card_pos in flipped_cards or card_pos in temp_flipped_cards:
                    screen.blit(card_images[card_index], (col * CARD_WIDTH, row * CARD_HEIGHT))
                else:
                    screen.blit(card_back, (col * CARD_WIDTH, row * CARD_HEIGHT))
        pygame.display.update()

    def check_card_click(pos):
        nonlocal flipped_cards, temp_flipped_cards, matched_pairs
        x, y = pos
        col, row = x // CARD_WIDTH, y // CARD_HEIGHT
        card_pos = (row, col)

        if card_pos not in flipped_cards and card_pos not in temp_flipped_cards:
            temp_flipped_cards.append(card_pos)
            draw_grid()

            if len(temp_flipped_cards) == 2:
                pygame.time.delay(1000)
                first_card_index = grid[temp_flipped_cards[0][0]][temp_flipped_cards[0][1]]
                second_card_index = grid[temp_flipped_cards[1][0]][temp_flipped_cards[1][1]]

                if first_card_index == second_card_index:
                    matched_pairs += 1
                    flipped_cards.extend(temp_flipped_cards)
                temp_flipped_cards = []
                draw_grid()

    create_grid()
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if matched_pairs < len(card_names):
                    check_card_click(pygame.mouse.get_pos())

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    grid_size = main_menu()
    main(grid_size)
