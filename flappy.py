# Importação do pygame
import pygame 
from pygame.locals import *

# Tamanho da tela
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800

# Velocidade inicial do Pássaro
INITIAL_SPEED = 10

# classe do pássaro
class Bird(pygame.sprite.Sprite):
    # caracteristicas da Classe Bird
    def __init__(self):
        # Construtor de inicialição
        pygame.sprite.Sprite.__init__(self)
        # imagens para movimentação do Bird
        self.images = [pygame.image.load('bluebird-upflap.png').convert_alpha(), 
                       pygame.image.load('bluebird-midflap.png').convert_alpha(), 
                       pygame.image.load('bluebird-downflap.png').convert_alpha()]
        # Váriavel para cada atualização pegará uma imagem da lista de imagens
        self.current_image = 0

        # imagem de inicio do Pássaro
        self.image = pygame.image.load('bluebird-upflap.png').convert_alpha()

        # posição do Bird
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    # função de atualição das ações do Pássaro
    def update(self):
        
        # Movimentação das imagens iniciando da pocição 0
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        
        # Velocidade do Pássaro
        self.speed = INITIAL_SPEED

        # Atuaização de altura do Pássaro
        self.rect[1] += self.speed

    # função do voo do passaro
    def bump(self):
        
        # Pulo do Pássaro
        self.rect[1] -= 200
# Importação init
pygame.init()

# Papel de parede do jogo
BACKGROUND = pygame.image.load('background-day.png')

# Dimensionar o Background com a tela
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)) 

# Criação da Tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# ??
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

# Variavél para a velocidade o Pássaro
clock = pygame.time.Clock()

# Laço principal do jogo
while True:
    # Controlando a velocidade o Pássaro
    clock.tick(30)
        
    # Testando eventos do usuário com o jogo
    for event in pygame.event.get():
        # Evento de finalização do jogo
        if event.type == QUIT:
            pygame.quit()
            
        # Evento para o botão espaço do teclado
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()
    # Atualição da tela de fundo na tela
    screen.blit(BACKGROUND,(0, 0))

    # 
    bird_group.update()
    
    # Desenha o os elementos do grupo
    bird_group.draw(screen)

    # Atualização da tela
    pygame.display.update()


    
