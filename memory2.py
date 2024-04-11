import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
grid_size = 4
tile_size = 100
grid = []
revealed_tiles = []
matched_tiles = []
images = []

# Load images
for i in range(1, (grid_size ** 2) // 2 + 1):
    images.append(pygame.image.load(f"card_clubs_0{i}.png"))

# Create grid
for row in range(grid_size):
    for col in range(grid_size):
        grid.append(pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size))

# Duplicate images
images *= 2
random.shuffle(images)

# Game loop
running = True
first_click = None
second_click = None

while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and len(revealed_tiles) < 2:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, tile in enumerate(grid):
                if tile.collidepoint(mouse_x, mouse_y) and i not in revealed_tiles + matched_tiles:
                    if first_click is None:
                        first_click = i
                        revealed_tiles.append(i)
                    elif second_click is None and i != first_click:
                        second_click = i
                        revealed_tiles.append(i)

    # Draw tiles
    for i, tile in enumerate(grid):
        if i in matched_tiles:
            pygame.draw.rect(screen, GRAY, tile)
        elif i in revealed_tiles:
            screen.blit(pygame.transform.scale(images[i], (tile_size, tile_size)), (tile.x, tile.y))
        else:
            pygame.draw.rect(screen, BLACK, tile)

    # Check for matching tiles
    if len(revealed_tiles) == 2:
        if images[first_click] == images[second_click]:
            matched_tiles.extend(revealed_tiles)
        time.sleep(0.5)
        revealed_tiles.clear()
        first_click = None
        second_click = None

    # Check for game over
    if len(matched_tiles) == len(grid):
        text = font.render("Congratulations! You won!", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
