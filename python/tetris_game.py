import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Game dimensions
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

SHAPE_COLORS = [CYAN, YELLOW, PURPLE, BLUE, ORANGE, GREEN, RED]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.fall_time = 0
        self.fall_speed = 0.5
        self.font = pygame.font.Font(None, 36)
        
        # Initialize sound (if available)
        self.rotate_sound = None
        self.clear_sound = None
        self.init_sound()

    def init_sound(self):
        if pygame.mixer.get_init():
            try:
                self.rotate_sound = pygame.mixer.Sound(os.path.join("sounds", "rotate.wav"))
                self.clear_sound = pygame.mixer.Sound(os.path.join("sounds", "clear.wav"))
            except pygame.error:
                print("Warning: Sound files not found. Game will run without sound.")

    def play_sound(self, sound):
        if sound:
            sound.play()

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = SHAPE_COLORS[SHAPES.index(shape)]
        return {
            'shape': shape,
            'color': color,
            'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
            'y': 0
        }

    def rotate_piece(self, piece):
        return list(zip(*piece[::-1]))

    def valid_move(self, piece, x, y):
        for i, row in enumerate(piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    if (x + j < 0 or x + j >= GRID_WIDTH or
                        y + i >= GRID_HEIGHT or
                        (y + i >= 0 and self.grid[y + i][x + j])):
                        return False
        return True

    def place_piece(self, piece):
        for i, row in enumerate(piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[piece['y'] + i][piece['x'] + j] = piece['color']

    def clear_lines(self):
        lines_cleared = 0
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        if lines_cleared:
            self.play_sound(self.clear_sound)
            self.score += (lines_cleared ** 2) * 100
            self.level = self.score // 1000 + 1
            self.fall_speed = max(0.1, 0.5 - (self.level - 1) * 0.05)

    def draw_grid(self):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, self.grid[i][j] or WHITE,
                                 (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0 if self.grid[i][j] else 1)

    def draw_piece(self, piece, offset_x=0, offset_y=0):
        for i, row in enumerate(piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, piece['color'],
                                     ((piece['x'] + j + offset_x) * BLOCK_SIZE,
                                      (piece['y'] + i + offset_y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

    def draw_next_piece(self):
        for i, row in enumerate(self.next_piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.next_piece['color'],
                                     (GRID_WIDTH * BLOCK_SIZE + 20 + j * BLOCK_SIZE,
                                      100 + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_info(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        next_text = self.font.render("Next:", True, WHITE)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 10))
        self.screen.blit(level_text, (GRID_WIDTH * BLOCK_SIZE + 10, 50))
        self.screen.blit(next_text, (GRID_WIDTH * BLOCK_SIZE + 10, 90))

    def run(self):
        while not self.game_over:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.valid_move(self.current_piece, self.current_piece['x'] - 1, self.current_piece['y']):
                        self.current_piece['x'] -= 1
                    if event.key == pygame.K_RIGHT and self.valid_move(self.current_piece, self.current_piece['x'] + 1, self.current_piece['y']):
                        self.current_piece['x'] += 1
                    if event.key == pygame.K_DOWN and self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                        self.current_piece['y'] += 1
                    if event.key == pygame.K_UP:
                        rotated = {'shape': self.rotate_piece(self.current_piece['shape']), 'color': self.current_piece['color'],
                                   'x': self.current_piece['x'], 'y': self.current_piece['y']}
                        if self.valid_move(rotated, rotated['x'], rotated['y']):
                            self.current_piece = rotated
                            self.play_sound(self.rotate_sound)

            if self.fall_time / 1000 > self.fall_speed:
                self.fall_time = 0
                if self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                    self.current_piece['y'] += 1
                else:
                    self.place_piece(self.current_piece)
                    self.clear_lines()
                    self.current_piece = self.next_piece
                    self.next_piece = self.new_piece()
                    if not self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y']):
                        self.game_over = True

            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_piece(self.current_piece)
            self.draw_next_piece()
            self.draw_info()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()