import pygame
import random
import time

# Initialize pygame
pygame.init()

# Size of Game Screen
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Escape!")

# Colors 
BACKGROUND_COLOR = (0, 0, 0)    # Black
PLAYER_COLOR = (0, 255, 255)    # Neon Blue
BLOCK_COLOR = (255, 0, 0)       # Bright Red
TEXT_COLOR = (255, 255, 255)    # White

# Fonts
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 50)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 60)

    def update(self, keys):
        speed = 5
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += speed

# Enemy class
class Block(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLOCK_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            return True  # Block passed player
        return False  # Block did not pass

# Function to run the game
def run_game():
    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    # Initial speed of blocks
    block_speed = 3

    # Add multiple blocks
    for _ in range(6):
        block = Block(block_speed)
        all_sprites.add(block)
        blocks.add(block)

    clock = pygame.time.Clock()
    score = 0
    running = True
    game_over = False
    start_time = time.time()

    while running:
        clock.tick(30)
        screen.fill(BACKGROUND_COLOR)

        if game_over:
            # Display Game Over and Final Score
            text = game_over_font.render("Game Over!", True, TEXT_COLOR)
            score_text = font.render(f"Your Final Score: {score}", True, TEXT_COLOR)
            replay_text = font.render("Press 'R' to Restart", True, TEXT_COLOR)

            screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2 - 80))
            screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2 - 40))
            screen.blit(replay_text, (WIDTH // 2 - 100, HEIGHT // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return True  # Restart the game

        else:
            # Increase speed every 20 seconds
            elapsed_time = time.time() - start_time
            if elapsed_time > 20:
                block_speed += 1  # Increase block speed
                start_time = time.time()  # Reset timer

                # Update all block speeds
                for block in blocks:
                    block.speed = block_speed

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            player.update(keys)

            # Update blocks and check if they passed the player
            for block in blocks:
                if block.update():  # If block passed the player
                    score += 1  # Increase score

            # Collision detection
            if pygame.sprite.spritecollide(player, blocks, False):
                game_over = True

            # Draw everything
            all_sprites.draw(screen)
            score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
            screen.blit(score_text, (10, 10))  # Score at the top left

            pygame.display.flip()

    return False  # Exit the game

# Main loop
while True:
    if not run_game():
        break

# Quit pygame
pygame.quit()
