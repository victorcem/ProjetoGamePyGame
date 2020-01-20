# Importação do pygame
import pygame, random
from pygame.locals import *

# Tamanho da tela
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 750
# Velocidade inicial do Pássaro
SPEED = 10
# Gravidade do jogo
GRAVITY = 1
# Velocidade do jogo
GAME_SPEED = 10
# Tamanho do chão
GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100
# Tamanho do cano
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
# Vão do chão
PIPE_GAP = 200

# Classe do pássaro
class Bird(pygame.sprite.Sprite):
    
    def __init__(self):
        # Construtor de inicialização
        pygame.sprite.Sprite.__init__(self)
        # Imagens para movimentação do Bird
        self.images = [pygame.image.load('bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('bluebird-downflap.png').convert_alpha()]
        # Speed do Pássaro
        self.speed = SPEED
        # Váriavel para cada atualização pegará uma imagem da lista de imagens
        self.current_image = 0
        # imagem de inicio do Pássaro
        self.image = pygame.image.load('bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        # posição do Bird
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2
    # função de atualição das ações do Pássaro
    def update(self):
        # Movimentação das imagens iniciando da pocição 0
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]
        # Gravidade do Bird
        self.speed += GRAVITY
        # Atuaização de altura do Pássaro
        self.rect[1] += self.speed
    # função do voo do passaro
    def bump(self):
        # Pulo do Pássaro
        self.speed = -SPEED
# Classe do Cano
class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        # Imagem da base e cano
        self.image = pygame.image.load('pipe-red.png').convert_alpha()
        # Tansformando a imagem para tele de fundo
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH,PIPE_HEIGHT))
        # Posicionamento do chão
        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)
    # Função para a velocidade do chão
    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)

# Importação init
pygame.init()
# Criação da Tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Papel de parede do jogo
BACKGROUND = pygame.image.load('background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
# Adicionar o Pássaro no Pássaro grupo
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)
# Grupo chão
ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

# Variavél para a velocidade o Pássaro
clock = pygame.time.Clock()
# Laço principal do jogo
while True:
    # Controlando a velocidade o Pássaro
    clock.tick(30)
    # Testando eventos do usuário com o jogo
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        # Evento para o botão espaço do teclado
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()
    # Atualição da tela de fundo na tela
    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
    # Atualização de grupo
    bird_group.update()
    ground_group.update()
    pipe_group.update()
    # Desenha o os elementos do grupo
    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)
    # Atualização da tela
    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
       pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        # Game over
        input()
        break
                