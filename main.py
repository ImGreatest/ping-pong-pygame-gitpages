import asyncio
from random import randint
import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.playing = True
        self.display = pygame.Surface((700, 500))
        self.window = pygame.display.set_mode((700, 500))

        self.clock = pygame.time.Clock()

        self.images1 = pygame.image.load('assets/image1.jpg')
        self.images1 = pygame.transform.scale(self.images1, self.display.get_size())

        self.paddleA = Paddle((255, 255, 255), 10, 100)
        self.paddleA.rect.x, self.paddleA.rect.y = 10, 200

        self.paddleB = Paddle((255, 255, 255), 10, 100)
        self.paddleB.rect.x, self.paddleB.rect.y = 680, 200

        self.ball = Ball(10, 10)
        self.ball.rect.x, self.ball.rect.y = 350, 250

        self.all_sprites_list = pygame.sprite.Group()
        self.all_sprites_list.add([self.paddleA, self.paddleB, self.ball])

        self.score, self.score2 = 0, 0
        self.status = True

    def win_condition(self):
        if self.score == 11:
            self.playing = False
            print("Player 1 выиграл")
        elif self.score2 == 11:
            self.playing = False
            print("Player 2 win")

    def otskok(self):
        if self.ball.rect.x >= 690:
            self.score += 1

            pygame.time.wait(750)

            self.ball.rect.x, self.ball.rect.y = 350, 250
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.rect.x <= 0:
            self.score2 += 1

            pygame.time.wait(750)

            self.ball.rect.x, self.ball.rect.y = 350, 250
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.rect.y > 490:
            self.ball.velocity[1] = -self.ball.velocity[1]
        if self.ball.rect.y < 0:
            self.ball.velocity[1] = -self.ball.velocity[1]

        if pygame.sprite.collide_mask(self.ball, self.paddleA) or pygame.sprite.collide_mask(self.ball, self.paddleB):
            self.ball.velocity[0] = -self.ball.velocity[0]
            self.ball.velocity[1] = randint(-8, 8)

    def move_flat(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.paddleA.rect.y -= 5
            if self.paddleA.rect.y < 0:
                self.paddleA.rect.y = 0
        if keys[pygame.K_s]:
            self.paddleA.rect.y += 5
            if self.paddleA.rect.y > 400:
                self.paddleA.rect.y = 400
        if keys[pygame.K_UP]:
            self.paddleB.rect.y -= 5
            if self.paddleB.rect.y < 0:
                self.paddleB.rect.y = 0
        if keys[pygame.K_DOWN]:
            self.paddleB.rect.y += 5
            if self.paddleB.rect.y > 400:
                self.paddleB.rect.y = 400

    def draw_score(self):
        font = pygame.font.Font(None, 74)
        text = font.render(str(self.score), True, pygame.Color("white"))
        self.window.blit(text, (250, 5))
        text = font.render(str(self.score2), True, pygame.Color("white"))
        self.window.blit(text, (420, 5))

    async def run(self):
        self.playing = True

        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False

            if not self.playing:
                break

            self.move_flat()
            self.otskok()
            self.win_condition()

            self.window.blit(self.images1, (0, 0))

            pygame.draw.line(
                self.window,
                (255, 255, 255),
                (350, 0),
                (350, 500),
                3,
            )

            self.draw_score()
            self.all_sprites_list.draw(self.window)
            self.all_sprites_list.update()

            self.ball.rect.x += self.ball.velocity[0]
            self.ball.rect.y += self.ball.velocity[1]

            pygame.display.flip()

            self.clock.tick(60)
            await asyncio.sleep(0)

        pygame.quit()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(None, size)
        surface_text = font.render(text, True, pygame.Color("black"))
        rect = surface_text.get_rect()
        rect.center = (x, y)
        self.display.blit(surface_text, rect)

class Ball (pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (255, 255, 255), (width/2, height/2), 5, 0)
        self.velocity = [randint(4, 8), randint(-8, 8)]
        self.rect = self.image.get_rect()


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect(topleft=(0, 0))


if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())
