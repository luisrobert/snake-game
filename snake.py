import pygame
import sys
import random

# Definir constantes
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20
FPS = 10

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# Inicializar el mixer de Pygame para sonidos
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("sounds/eat.wav")
die_sound = pygame.mixer.Sound("sounds/die.wav")
pygame.mixer.music.load("sounds/arcade.mp3")

class Snake:
    def __init__(self):
        self.positions = [(100, 100), (80, 100), (60, 100)]
        self.direction = (1, 0)
        self.grow = False

    def update(self):
        if self.grow:
            self.positions = [self.get_next_position()] + self.positions
            self.grow = False
        else:
            self.positions = [self.get_next_position()] + self.positions[:-1]

    def get_next_position(self):
        current_head = self.positions[0]
        x, y = self.direction
        return (current_head[0] + (x * CELL_SIZE), current_head[1] + (y * CELL_SIZE))

    def change_direction(self, direction):
        self.direction = direction

    def grow_snake(self):
        self.grow = True

    def check_collision(self):
        head = self.positions[0]
        return (head in self.positions[1:] or
                head[0] < 0 or head[0] >= SCREEN_WIDTH or
                head[1] < 0 or head[1] >= SCREEN_HEIGHT)

    def draw(self, surface):
        for position in self.positions:
            pygame.draw.rect(surface, GREEN, pygame.Rect(position[0], position[1], CELL_SIZE, CELL_SIZE))

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                    self.snake.change_direction((1, 0))

    def run(self):
        pygame.mixer.music.play(-1)  # Reproduce la música de fondo en bucle
        while True:
            self.handle_keys()
            self.snake.update()

            if self.snake.positions[0] == self.food.position:
                self.snake.grow_snake()
                self.food.position = self.food.random_position()
                self.score += 1
                eat_sound.play()  # Reproduce el sonido al comer

            screen.fill(BLACK)
            self.snake.draw(screen)
            self.food.draw(screen)
            self.draw_score(screen)
            pygame.display.update()

            if self.snake.check_collision():
                die_sound.play()  # Reproduce el sonido al morir
                self.game_over()

            clock.tick(FPS)

    def draw_score(self, surface):
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 10))

    def game_over(self):
        game_over_text = font.render("Game Over", True, WHITE)
        replay_text = font.render("Press R to Replay or Q to Quit", True, WHITE)
        pygame.mixer.music.stop()
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 40))
        screen.blit(replay_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        pygame.mixer.music.play(-1)

if __name__ == "__main__":
    game = Game()
    game.run()
