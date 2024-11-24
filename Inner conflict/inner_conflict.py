import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Inner Conflict")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SHADOW_COLOR = (50, 50, 50)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player Attributes
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100]
player_speed = 4  # Player speed for dodging

# Shadow Enemy Attributes
shadow_size = 50
shadow_speed = 3  # Shadow speed
shadows = []  # List of shadows

# Projectiles
projectile_speed = 5
projectiles = []

# Health Bar
max_health = 100
current_health = max_health

# Fonts
font = pygame.font.Font(None, 36)

# Story Elements
level = 0
story_texts = [
    "You wake up in darkness. The silence whispers your fears.",
    "Each step forward reveals shadows of your doubt. They are closing in.",
    "The shadows grow stronger and more persistent. Can you fight them?",
    "You've faced your fears. Will you stand strong or fall to the darkness?",
    "It's time for the final battle. Confront the darkness within you. This is your inner demon."
]

# Backgrounds
background_images = [
    pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)),
    pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)),
    pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)),
    pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)),
    pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Boss battle background
]

# Fill backgrounds with colors to simulate different levels
background_images[0].fill((0, 0, 0))  # Black for the first level
background_images[1].fill((50, 50, 50))  # Dark gray for level 2
background_images[2].fill((100, 0, 0))  # Dark red for level 3
background_images[3].fill((0, 0, 100))  # Dark blue for level 4
background_images[4].fill((0, 0, 0))  # Dark purple for boss level

# Music
background_music = [
    "Inner conflict/assets/assets/music/Day-of-Chaos(chosic.com).mp3",
    "Inner conflict/assets/assets/music/Demented-Nightmare-MP3(chosic.com).mp3",
    
]

# Load First Music Track
pygame.mixer.music.load(background_music[0])
pygame.mixer.music.play(-1)  # Loop the music

# Story Function (Displays the story text)
def display_story(text):
    screen.fill(BLACK)
    lines = text.split('. ')
    y_offset = SCREEN_HEIGHT // 2 - len(lines) * 20
    for line in lines:
        story_render = font.render(line, True, WHITE)
        screen.blit(story_render, (SCREEN_WIDTH // 2 - story_render.get_width() // 2, y_offset))
        y_offset += 40
    pygame.display.flip()
    pygame.time.delay(3000)  # Pause for 3 seconds to let the player read

# Spawn Shadows Function
def spawn_shadows(level):
    shadows.clear()
    num_shadows = level + 3  # Add more shadows per level
    for _ in range(num_shadows):
        shadow_pos = [random.randint(0, SCREEN_WIDTH - shadow_size), random.randint(0, SCREEN_HEIGHT // 2)]
        shadows.append({"pos": shadow_pos, "speed": shadow_speed})

# Player Shooting Function
def shoot_projectile():
    projectile_pos = [player_pos[0] + player_size // 2, player_pos[1]]
    projectiles.append({"pos": projectile_pos, "speed": projectile_speed})

# Function to move shadows
def move_shadows():
    global current_health
    for shadow in shadows:
        shadow_x, shadow_y = shadow["pos"]

        # Calculate direction to follow player
        direction_x = player_pos[0] - shadow_x
        direction_y = player_pos[1] - shadow_y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if distance != 0:
            shadow["pos"][0] += (direction_x / distance) * shadow_speed
            shadow["pos"][1] += (direction_y / distance) * shadow_speed

        # Collision detection with player
        shadow_rect = pygame.Rect(shadow_x, shadow_y, shadow_size, shadow_size)
        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
        if player_rect.colliderect(shadow_rect):
            current_health -= 5  # Decrease health when shadow touches player

# Function to move projectiles and check for collisions with shadows
def move_projectiles():
    global current_health
    for projectile in projectiles[:]:
        # Move projectile up the screen
        projectile["pos"][1] -= projectile_speed
        projectile_rect = pygame.Rect(projectile["pos"][0], projectile["pos"][1], 10, 20)

        # Check for collision with shadows
        for shadow in shadows[:]:
            shadow_rect = pygame.Rect(shadow["pos"][0], shadow["pos"][1], shadow_size, shadow_size)
            if projectile_rect.colliderect(shadow_rect):
                shadows.remove(shadow)  # Remove shadow if hit by projectile
                projectiles.remove(projectile)  # Remove projectile if it hits a shadow
                break  # Exit the loop once the collision is handled

        # Remove projectile if it goes off-screen
        if projectile_rect.bottom < 0:
            projectiles.remove(projectile)

# Game Over Function
def game_over():
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, RED)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    main()
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    sys.exit()

# Level Completion Function
def level_complete():
    display_story("Level Complete! Press any key to proceed to the next level.")
    # Wait for user input to move to the next level
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                return

# Game Loop (Main Game Play)
def game_loop():
    global current_health, level, player_pos, shadows, shadow_speed, shadow_count, projectiles

    for level in range(len(story_texts) - 1):  # Excluding boss level
        # Display Story
        display_story(story_texts[level])

        # Change Music and Background for each level
        if level < len(background_images) - 1:
            pygame.mixer.music.load(background_music[level])
            pygame.mixer.music.play(-1)

        # Spawn Shadows
        spawn_shadows(level)

        running = True
        while running:
            screen.blit(background_images[level], (0, 0))

            # Handle Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        shoot_projectile()

            # Move Shadows
            move_shadows()

            # Move Projectiles
            move_projectiles()

            # Player Controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= player_speed
            if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size:
                player_pos[0] += player_speed
            if keys[pygame.K_UP] and player_pos[1] > 0:
                player_pos[1] -= player_speed
            if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - player_size:
                player_pos[1] += player_speed

            # Draw Player
            player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
            pygame.draw.rect(screen, WHITE, player_rect)

            # Draw Shadows
            for shadow in shadows:
                shadow_rect = pygame.Rect(shadow["pos"][0], shadow["pos"][1], shadow_size, shadow_size)
                pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect)

            # Draw Projectiles
            for projectile in projectiles:
                pygame.draw.rect(screen, RED, pygame.Rect(projectile["pos"][0], projectile["pos"][1], 10, 20))

            # Draw Health Bar
            pygame.draw.rect(screen, WHITE, pygame.Rect(10, 10, current_health * 2, 25))

            # Check for Game Over
            if current_health <= 0:
                game_over()

            # Check for Level Completion
            if len(shadows) == 0:
                level_complete()

            # Update the screen
            pygame.display.flip()
            clock.tick(FPS)

# Main Function to Start the Game
def main():
    game_loop()

if __name__ == "__main__":
    main()
