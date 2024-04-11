import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
CARD_WIDTH, CARD_HEIGHT = 64, 64
ROWS, COLS = 4, 4
WIDTH, HEIGHT = CARD_WIDTH*ROWS, CARD_HEIGHT*COLS
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory")

# Fonts
font = pygame.font.SysFont(None, 40)

# Images
card_images = []
for i in range(1, (ROWS * COLS) // 2 + 1):
    img = pygame.image.load(f"card_clubs_0{i}.png").convert()
    img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
    card_images.append(img)

# Game variables
grid = []
flipped_cards = []
matched_pairs = 0

# Create game grid
def create_grid():
    global grid
    cards = list(range((ROWS * COLS) // 2)) * 2
    random.shuffle(cards)
    grid = [cards[i:i+COLS] for i in range(0, len(cards), COLS)]

# Draw cards
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            card = grid[row][col]
            if (row, col) in flipped_cards or matched_pairs == (ROWS * COLS) // 2:
                screen.blit(card_images[card], (col * CARD_WIDTH, row * CARD_HEIGHT))
            else:
                pygame.draw.rect(screen, GRAY, (col * CARD_WIDTH, row * CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT))
    pygame.display.flip()

# Check for card click
def check_card_click(pos):
    global flipped_cards
    row, col = pos[1] // CARD_HEIGHT, pos[0] // CARD_WIDTH
    if (row, col) not in flipped_cards:
        flipped_cards.append((row, col))
        if len(flipped_cards) == 2:
            pygame.time.wait(500)
            if grid[flipped_cards[0][0]][flipped_cards[0][1]] == grid[flipped_cards[1][0]][flipped_cards[1][1]]:
                global matched_pairs
                matched_pairs += 1
            else:
                flipped_cards.pop()
                flipped_cards.pop()

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
                if matched_pairs != (ROWS * COLS) // 2:
                    pos = pygame.mouse.get_pos()
                    check_card_click(pos)

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
