import pygame
import random
import sys

pygame.init()

# Dimensions
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frogger Arcade")
clock = pygame.time.Clock()

# Couleurs
DARK_BG = (15, 15, 25)
ROAD_COLOR = (30, 35, 45)
SAFE_ZONE = (0, 180, 100)
FROG_COLOR = (0, 255, 157)      # Vert néon
CAR_COLORS = [(255, 75, 75), (255, 230, 0), (0, 162, 255), (255, 150, 0)]
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Polices
font_large = pygame.font.SysFont("Arial", 42, bold=True)
font_medium = pygame.font.SysFont("Arial", 28, bold=True)
font_small = pygame.font.SysFont("Arial", 18)

def create_cars():
    cars = []
    # Créer des voies de circulation (Lignes de y = 80 à y = 480)
    for row, y in enumerate(range(100, 500, 50)):
        speed = random.choice([2, 3, 4, 5]) * random.choice([-1, 1])
        color = CAR_COLORS[row % len(CAR_COLORS)]
        # 2 à 3 voitures par voie
        for i in range(random.randint(2, 3)):
            x = (i * 200 + random.randint(0, 50)) % WIDTH
            rect = pygame.Rect(x, y + 5, 50, 35)
            cars.append({"rect": rect, "speed": speed, "color": color})
    return cars

def reset_game():
    return {
        "frog": pygame.Rect(WIDTH // 2 - 15, HEIGHT - 45, 30, 30),
        "cars": create_cars(),
        "score": 0,
        "lives": 3,
        "game_over": False,
        "victory": False
    }

game = reset_game()
high_score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game["game_over"] and not game["victory"]:
                # Déplacement case par case (Grille)
                if event.key == pygame.K_UP and game["frog"].top > 10:
                    game["frog"].y -= 50
                    game["score"] += 10
                elif event.key == pygame.K_DOWN and game["frog"].bottom < HEIGHT - 10:
                    game["frog"].y += 50
                elif event.key == pygame.K_LEFT and game["frog"].left > 10:
                    game["frog"].x -= 40
                elif event.key == pygame.K_RIGHT and game["frog"].right < WIDTH - 10:
                    game["frog"].x += 40
            else:
                if event.key == pygame.K_SPACE:
                    game = reset_game()

    screen.fill(DARK_BG)

    if not game["game_over"] and not game["victory"]:
        # Zone de départ et d'arrivée (Vertes)
        pygame.draw.rect(screen, SAFE_ZONE, (0, 0, WIDTH, 80))
        pygame.draw.rect(screen, SAFE_ZONE, (0, HEIGHT - 60, WIDTH, 60))

        # Zone de route
        pygame.draw.rect(screen, ROAD_COLOR, (0, 80, WIDTH, 460))

        # 1. Déplacement des voitures
        for car in game["cars"]:
            car["rect"].x += car["speed"]

            # Téléportation quand la voiture sort de l'écran (Boucle)
            if car["speed"] > 0 and car["rect"].left > WIDTH:
                car["rect"].right = 0
            elif car["speed"] < 0 and car["rect"].right < 0:
                car["rect"].left = WIDTH

            # Collision Voiture vs Grenouille
            if game["frog"].colliderect(car["rect"]):
                game["lives"] -= 1
                if game["lives"] <= 0:
                    game["game_over"] = True
                else:
                    # Replacer la grenouille au départ
                    game["frog"].x = WIDTH // 2 - 15
                    game["frog"].y = HEIGHT - 45

            # Dessin de la voiture
            pygame.draw.rect(screen, car["color"], car["rect"], border_radius=6)

        # 2. Victoire si la grenouille atteint l'autre côté (Haut)
        if game["frog"].top <= 80:
            game["score"] += 100
            game["frog"].x = WIDTH // 2 - 15
            game["frog"].y = HEIGHT - 45
            # Régénérer des voitures plus rapides
            game["cars"] = create_cars()

        if game["score"] > high_score:
            high_score = game["score"]

        # Dessin de la grenouille
        pygame.draw.ellipse(screen, FROG_COLOR, game["frog"])

        # Affichage du score et des vies
        score_txt = font_medium.render(f"Score: {game['score']}", True, WHITE)
        lives_txt = font_medium.render(f"Vies: {'❤️' * game['lives']}", True, WHITE)
        screen.blit(score_txt, (20, 15))
        screen.blit(lives_txt, (WIDTH - lives_txt.get_width() - 20, 15))

    else:
        # Écran Game Over
        title_txt = font_large.render("GAME OVER", True, CAR_COLORS[0])
        final_score_txt = font_medium.render(f"Score: {game['score']}", True, WHITE)
        best_score_txt = font_medium.render(f"Meilleur score: {high_score}", True, FROG_COLOR)
        replay_txt = font_small.render("Appuie sur ESPACE pour rejouer", True, GRAY)

        screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 200))
        screen.blit(final_score_txt, (WIDTH // 2 - final_score_txt.get_width() // 2, 270))
        screen.blit(best_score_txt, (WIDTH // 2 - best_score_txt.get_width() // 2, 310))
        screen.blit(replay_txt, (WIDTH // 2 - replay_txt.get_width() // 2, 390))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()