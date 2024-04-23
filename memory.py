import pygame
import random
import csv

# Initialize Pygame
pygame.init()

# Set up display
CARD_WIDTH, CARD_HEIGHT = 64, 64
ROWS, COLS = 4, 4
WIDTH, HEIGHT = CARD_WIDTH * ROWS, CARD_HEIGHT * COLS
FPS = 30

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

# Load card names from CSV
def load_card_names(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for row in reader]

# Images
card_names = load_card_names('_cards.csv')  # Update the path to your CSV file
card_images = []
card_back = pygame.image.load("card_back.png").convert_alpha()
card_back = pygame.transform.scale(card_back, (CARD_WIDTH, CARD_HEIGHT))

for name in card_names:
    img = pygame.image.load(name).convert_alpha()
    img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
    card_images.append(img)

# Game variables
grid = []
flipped_cards = []
temp_flipped_cards = []
matched_pairs = 0

# Create game grid
def create_grid():
    global grid
    cards = list(range(len(card_images))) * 2  # Ensure there is a pair for each card
    random.shuffle(cards)
    grid = [cards[i:i + COLS] for i in range(0, len(cards), COLS)]

# Draw cards
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            card_pos = (row, col)
            card_index = grid[row][col]
            if card_pos in flipped_cards or card_pos in temp_flipped_cards:
                screen.blit(card_images[card_index], (col * CARD_WIDTH, row * CARD_HEIGHT))
            else:
                screen.blit(card_back, (col * CARD_WIDTH, row * CARD_HEIGHT))
    pygame.display.flip()

# Check for card click
def check_card_click(pos):
    global flipped_cards, temp_flipped_cards, matched_pairs
    x, y = pos
    col, row = x // CARD_WIDTH, y // CARD_HEIGHT
    card_pos = (row, col)

    if card_pos not in flipped_cards and card_pos not in temp_flipped_cards:
        temp_flipped_cards.append(card_pos)

        if len(temp_flipped_cards) == 2:
            first_card_index = grid[temp_flipped_cards[0][0]][temp_flipped_cards[0][1]]
            second_card_index = grid[temp_flipped_cards[1][0]][temp_flipped_cards[1][1]]
            draw_grid()
            pygame.time.wait(1000)

            if first_card_index == second_card_index:
                matched_pairs += 1
                flipped_cards.extend(temp_flipped_cards)
            temp_flipped_cards = []

# Main game loop
def main():
    running = True
    create_grid()
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if matched_pairs < (ROWS * COLS) // 2:
                    check_card_click(pygame.mouse.get_pos())

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
