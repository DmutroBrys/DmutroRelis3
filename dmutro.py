import pygame
import random
from pygame import image, transform, mixer

class Game:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.win_sound = mixer.Sound('positive-notification-new-level-152480.mp3')
        self.hit_sound = mixer.Sound('udar-po-litsu-24272.mp3')

        self.WIDTH, self.HEIGHT = 500, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Catch the Enemies")

        self.backgrounds = [
            transform.scale(image.load('fon3.jpg'), (self.WIDTH, self.HEIGHT)),
            transform.scale(image.load('fon1.jpg'), (self.WIDTH, self.HEIGHT)),
            transform.scale(image.load('fon2.jpg'), (self.WIDTH, self.HEIGHT)),
            transform.scale(image.load('fon4.jpg'), (self.WIDTH, self.HEIGHT))
        ]

        self.COLORS = {
            "WHITE": (255, 255, 255),
            "RED": (255, 0, 0),
            "GREEN": (0, 255, 0),
            "BLUE": (0, 0, 255),
            "BLACK": (0, 0, 0),
            "PURPLE": (128, 0, 128),
            "YELLOW": (255, 255, 0),
            "ORANGE": (255, 165, 0),
            "CYAN": (0, 255, 255),
            "GOLD": (255, 215, 0)
        }

        self.player_size = 70
        self.player_speed = 5
        self.enemy_size = 50
        self.player_image = transform.scale(image.load('player.jpg'), (self.player_size, self.player_size))
        self.enemy_image1 = transform.scale(image.load('enemy1.jpg'), (self.enemy_size, self.enemy_size))
        self.enemy_image2 = transform.scale(image.load('enemy2.jpg'), (self.enemy_size, self.enemy_size))
        self.speed_low_image = transform.scale(image.load('enemylow.jpg'), (50, 50))
        self.speed_speed_image = transform.scale(image.load('enemyspeed.jpg'), (30, 30))
        self.speed_big_image = transform.scale(image.load('enemybig.png'), (50, 50))
        self.speed_small_image = transform.scale(image.load('enemysmall.png'), (30, 30))

        self.enemy_speed = 5
        self.bonus_size = 30
        self.bonus_speed = 5
        self.clock = pygame.time.Clock()
        self.running = False
        self.score = 0

        self.restart_game()

    def restart_game(self):
        self.player_x = self.WIDTH // 2 - self.player_size // 2
        self.player_y = self.HEIGHT - self.player_size - 10
        self.enemies = []
        self.bonuses = []
        self.maluses = []
        self.speed_boosts = []
        self.speed_lows = []
        self.score = 0
        self.player_size = 50
        self.player_speed = 5
        self.running = True

    def draw_text(self, text, size, x, y, color=None):
        if color is None:
            color = self.COLORS["BLACK"]
        font = pygame.font.Font(None, size)
        render = font.render(text, True, color)
        self.screen.blit(render, (x, y))

    def start_menu(self):
        menu_running = True
        while menu_running:
            self.screen.blit(self.backgrounds[2], (0, 0))
            self.draw_text("Catch the Enemies", 50, self.WIDTH // 2 - 150, self.HEIGHT // 2 - 50)
            self.draw_text("Press Space to Start", 36, self.WIDTH // 2 - 140, self.HEIGHT // 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.restart_game()
                        menu_running = False

            pygame.display.update()

    def run(self):
        self.start_menu()

        while self.running:
            self.screen.blit(self.backgrounds[0], (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and self.player_x > 0:
                self.player_x -= self.player_speed
            if keys[pygame.K_d] and self.player_x < self.WIDTH - self.player_size:
                self.player_x += self.player_speed
            if keys[pygame.K_w] and self.player_y > 0:
                self.player_y -= self.player_speed
            if keys[pygame.K_s] and self.player_y < self.HEIGHT - self.player_size:
                self.player_y += self.player_speed

            # Enemy and bonus creation
            if random.randint(1, 30) == 1:
                self.enemies.append(self.create_enemy())
            if random.randint(1, 100) == 1:
                self.bonuses.append(self.create_bonus())
            if random.randint(1, 100) == 1:
                self.maluses.append(self.create_malus())
            if random.randint(1, 100) == 1:
                self.speed_boosts.append(self.create_speed_boost())
            if random.randint(1, 100) == 1:
                self.speed_lows.append(self.create_speed_low())

            self.update_enemies()
            self.update_bonuses()
            self.update_maluses()
            self.update_speed_boosts()
            self.update_speed_lows()

            self.screen.blit(self.player_image, (self.player_x, self.player_y))
            self.display_score()

            if self.score >= 30:  # Win condition
                self.game_won()

            pygame.display.update()
            self.clock.tick(30)

        pygame.quit()

    def create_enemy(self):
        x = random.randint(0, self.WIDTH - self.enemy_size)
        y = -self.enemy_size
        color = random.choice([self.COLORS["RED"], self.COLORS["GREEN"]])
        return [x, y, color]

    def create_bonus(self):
        x = random.randint(0, self.WIDTH - self.bonus_size)
        y = -self.bonus_size
        return [x, y]

    def create_malus(self):
        x = random.randint(0, self.WIDTH - self.bonus_size)
        y = -self.bonus_size
        return [x, y]

    def create_speed_boost(self):
        x = random.randint(0, self.WIDTH - self.bonus_size)
        y = -self.bonus_size
        return [x, y]

    def create_speed_low(self):
        x = random.randint(0, self.WIDTH - self.bonus_size)
        y = -self.bonus_size
        return [x, y]

    def update_enemies(self):
        for enemy in self.enemies[:]:
            enemy[1] += self.enemy_speed
            if (self.player_x < enemy[0] < self.player_x + self.player_size or
                self.player_x < enemy[0] + self.enemy_size < self.player_x + self.player_size) and \
               (self.player_y < enemy[1] < self.player_y + self.player_size or
                self.player_y < enemy[1] + self.enemy_size < self.player_y + self.player_size):
                self.enemies.remove(enemy)
                self.score += 1
            if enemy[1] > self.HEIGHT:
                if enemy[2] == self.COLORS["RED"]:
                    self.game_over()
                else:
                    self.enemies.remove(enemy)

            if enemy[2] == self.COLORS["GREEN"]:
                self.screen.blit(self.enemy_image2, (enemy[0], enemy[1]))
            else:
                self.screen.blit(self.enemy_image1, (enemy[0], enemy[1]))

    def update_bonuses(self):
        for bonus in self.bonuses[:]:
            bonus[1] += self.bonus_speed
            if (self.player_x < bonus[0] < self.player_x + self.player_size or
                self.player_x < bonus[0] + self.bonus_size < self.player_x + self.player_size) and \
               (self.player_y < bonus[1] < self.player_y + self.player_size or
                self.player_y < bonus[1] + self.bonus_size < self.player_y + self.player_size):
                self.bonuses.remove(bonus)
                self.player_size += 10
                self.player_image = transform.scale(image.load('player.jpg'), (self.player_size, self.player_size))  # Оновлюємо вигляд гравця
            if bonus[1] > self.HEIGHT:
                self.bonuses.remove(bonus)
            self.screen.blit(self.speed_big_image, (bonus[0], bonus[1]))

    def update_maluses(self):
        for malus in self.maluses[:]:
            malus[1] += self.bonus_speed
            if (self.player_x < malus[0] < self.player_x + self.player_size or
                self.player_x < malus[0] + self.bonus_size < self.player_x + self.player_size) and \
               (self.player_y < malus[1] < self.player_y + self.player_size or
                self.player_y < malus[1] + self.bonus_size < self.player_y + self.player_size):
                self.maluses.remove(malus)
                self.player_size = max(20, self.player_size - 5)  # Не даємо зменшитись до менше ніж 20
                self.player_image = transform.scale(image.load('player.jpg'), (self.player_size, self.player_size))  # Оновлюємо вигляд гравця
            if malus[1] > self.HEIGHT:
                self.maluses.remove(malus)
            self.screen.blit(self.speed_small_image, (malus[0], malus[1]))

    def update_speed_boosts(self):
        for speed_boost in self.speed_boosts[:]:
            speed_boost[1] += self.bonus_speed
            if (self.player_x < speed_boost[0] < self.player_x + self.player_size or
                self.player_x < speed_boost[0] + self.bonus_size < self.player_x + self.player_size) and \
               (self.player_y < speed_boost[1] < self.player_y + self.player_size or
                self.player_y < speed_boost[1] + self.bonus_size < self.player_y + self.player_size):
                self.speed_boosts.remove(speed_boost)
                self.player_speed += 2
            if speed_boost[1] > self.HEIGHT:
                self.speed_boosts.remove(speed_boost)
            self.screen.blit(self.speed_speed_image, (speed_boost[0], speed_boost[1]))

    def update_speed_lows(self):
        for speed_low in self.speed_lows[:]:
            speed_low[1] += self.bonus_speed
            if (self.player_x < speed_low[0] < self.player_x + self.player_size or
                self.player_x < speed_low[0] + self.bonus_size < self.player_x + self.player_size) and \
               (self.player_y < speed_low[1] < self.player_y + self.player_size or
                self.player_y < speed_low[1] + self.bonus_size < self.player_y + self.player_size):
                self.speed_lows.remove(speed_low)
                self.player_speed = max(1, self.player_speed - 2)
                self.score = max(0, self.score - 1)
                self.hit_sound.play()
            if speed_low[1] > self.HEIGHT:
                self.speed_lows.remove(speed_low)
            self.screen.blit(self.speed_low_image, (speed_low[0], speed_low[1]))

    def display_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, self.COLORS["BLACK"])
        self.screen.blit(score_text, (10, 10))

    def game_over(self):
        self.screen.blit(self.backgrounds[1], (0, 0))
        self.draw_text("Game Over", 50, self.WIDTH // 2 - 100, self.HEIGHT // 2 - 50)
        self.draw_text("Press R to Restart", 36, self.WIDTH // 2 - 120, self.HEIGHT // 2)
        
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.restart_game()
                    waiting = False

    def game_won(self):
        self.screen.blit(self.backgrounds[3], (0, 0))  # Optionally change background for win screen
        self.draw_text("You Win!", 50, self.WIDTH // 2 - 100, self.HEIGHT // 2 - 50)
        self.draw_text("Press R to Restart", 36, self.WIDTH // 2 - 120, self.HEIGHT // 2)

        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.restart_game()
                    waiting = False

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
