import pygame
import time
import random
import os   

pygame.font.init()

WIDTH, HEIGHT = 1000, 780
Window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodgy Dodge")

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

BG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "DK.jpg")), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
player_velocity = 14
Font = pygame.font.SysFont("comicsans", 30)

debris_width = 10
debris_height = 20
debris_velocity = 6

player_img = pygame.image.load(os.path.join(ASSETS_PATH, "player.png"))
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

debris_img = pygame.image.load(os.path.join(ASSETS_PATH, "rock..webp"))
debris_img = pygame.transform.scale(debris_img, (debris_width, debris_height))


def draw(PLAYER, Elapsed_Time, debris):
    Window.blit(BG, (0, 0))
    Window.blit(player_img, (PLAYER.x, PLAYER.y))

    for debri in debris:
        Window.blit(debris_img, (debri.x, debri.y))

    time_font = Font.render(f"Time: {round(Elapsed_Time)}s", 1, "white")
    Window.blit(time_font, (10, 10))
    pygame.display.update()


def main():
    run = True

    PLAYER = pygame.Rect(0, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    CLOCK = pygame.time.Clock()
    Start_Time = time.time()
    Elapsed_Time = 0

    debris_add_increment = 2000
    debris_count = 0
    debris = []
    hit = False

    while run:
        debris_count += CLOCK.tick(60)
        Elapsed_Time = time.time() - Start_Time

        if debris_count > debris_add_increment:
            for _ in range(3):
                debris_x = random.randint(0, WIDTH - debris_width)
                debri = pygame.Rect(debris_x, -debris_height, debris_width, debris_height)
                debris.append(debri)

            debris_add_increment = max(200, debris_add_increment - 50)
            debris_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        for debri in debris[:]:
            debri.y += debris_velocity
            if debri.y > HEIGHT:
                debris.remove(debri)
            elif debri.y + debris_height >= PLAYER.y and debri.colliderect(PLAYER):
                debris.remove(debri)
                hit = True
                break

        if hit:
            lost_text = Font.render("You lost oh noooooo!", 1, "red")
            Window.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(7000)
            break

        draw(PLAYER, Elapsed_Time, debris)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and PLAYER.x - player_velocity >= 0:
            PLAYER.x -= player_velocity
        if keys[pygame.K_d] and PLAYER.x + player_velocity + PLAYER_WIDTH <= WIDTH:
            PLAYER.x += player_velocity

    pygame.quit()


if __name__ == "__main__":
    main()
