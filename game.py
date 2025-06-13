import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 60

# Define colors
COLORS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'purple': (128, 0, 128)
}


class Dot:
    def __init__(self, color_name, position, radius=30):
        self.color_name = color_name
        self.color = COLORS[color_name]
        self.position = position
        self.radius = radius
        self.clicked = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)
        if self.clicked:
            pygame.draw.circle(surface, (255, 255, 255), self.position, self.radius, 3)

    def is_clicked(self, mouse_pos):
        dx = self.position[0] - mouse_pos[0]
        dy = self.position[1] - mouse_pos[1]
        return (dx ** 2 + dy ** 2) ** 0.5 <= self.radius


class DotMatchGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎯 Match the Dots!")
        self.clock = pygame.time.Clock()
        self.score = 0
        self.dots = []
        self.clicked_dots = []
        self.generate_dots()

    def generate_dots(self):
        self.clicked_dots.clear()
        positions = [(150, 200), (300, 200), (450, 200)]
        # Choose a color to duplicate and a third different color
        matching_color = random.choice(list(COLORS.keys()))
        other_color = random.choice([c for c in COLORS.keys() if c != matching_color])
        color_choices = [matching_color, matching_color, other_color]
        random.shuffle(color_choices)
        self.dots = [Dot(color, pos) for color, pos in zip(color_choices, positions)]

    def draw_screen(self):
        self.screen.fill((240, 240, 240))  # neutral background
        for dot in self.dots:
            dot.draw(self.screen)
        self.display_score()
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

    def handle_click(self, mouse_pos):
        for dot in self.dots:
            if dot.is_clicked(mouse_pos) and dot not in self.clicked_dots:
                dot.clicked = True
                self.clicked_dots.append(dot)
                break

        if len(self.clicked_dots) == 2:
            color1 = self.clicked_dots[0].color_name
            color2 = self.clicked_dots[1].color_name
            if color1 == color2:
                self.score += 1
                print("✅ Correct match!")
            else:
                print("❌ Wrong match!")
            # Reset for next round
            pygame.time.delay(500)
            self.generate_dots()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.draw_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
        pygame.quit()
        sys.exit()


# Main
if __name__ == "__main__":
    game = DotMatchGame()
    game.run()
