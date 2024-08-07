# Importe o módulo pygame
import pygame

# Importe o módulo random para números aleatórios 
import random

# Importe pygame.locals para fácil acesso as coordenadas chaves
# Atualizado para atender os padrões flake8 e black
from pygame.locals import (
    RLEACCEL,
    K_UP,               # Tecla para cima
    K_DOWN,             # Tecla para baixo
    K_LEFT,             # Tecla para esquerda
    K_RIGHT,            # Tecla para direita
    K_ESCAPE,           # Tecla de escape
    KEYDOWN,            # Qualquer tecla pressionada
    QUIT,               # Tecla de fechar janela
)

# Defina constantes para largura e a altura da tel
SCREEN_WIDTH = 800          # Esta define a largura
SCREEN_HEIGHT = 600         # Esta define a altura

# Defina o objeto jogador extendendo a classe pygame.sprite.Sprite
# A surface desenhada na tela agora vai ser um atributo de 'jogador'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()  # o jogador como imagem
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()        # salva essa informação na variável rect

    # Mova o sprite com base nas teclas pressionadas pelo usuário
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
    
        # Mantenha o jogador dentro da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Defina o objeto inimigo extendendo a classe pygame.sprite.Sprite
# A surface desenhada na tela agora vai ser um atributo de 'inimigo'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()  # o inimigo como imagem
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Mova o sprite com base na velocidade
    # Remova o sprite quando ele passa a borda esquerda da tela
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Defina o objeto Cloud
# Use uma imagem para ficar legal
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # Posição inicial gerada aleatoriamente
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Mova a nuvem com velocidade constante
    # Elimine a nuvem ao sair da tela
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Inicialize o pygame
pygame.init()

# Ajuste o clock para melhor visualização
clock = pygame.time.Clock()

# Crie o objeto da tela
# O tamanho da tela é definido pelas constantes SCREEN_WIDTH e SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Crie um evento personalizado para adicionar um novo inimigo e nuvens
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Variável para manter o loop do jogo
running = True

# Instanciar o jogador. Até aqui, isso é apenas um retângulo.
player = Player()

# Criar grupos para conter os sprites dos inimigos
# - inimigos são usados para detectar colisões e atualizar posição
# - all_sprites é usado para desenhar na tela
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Loop principal
while running:
    # Veja cada evento na fila de eventos
    for event in pygame.event.get():
        # O jogador pressionou alguma tecla?
        if event.type == KEYDOWN:
            # Foi a tecla ESCAPE? Se sim, para o loop.
            if event.type == K_ESCAPE:
                running = False
        # O jogador clicou o botão de fechar a janela? Se sim, pare o loop.
        elif event.type == QUIT:
            running = False

        # Adiciona um novo inimigo?
        elif event.type == ADDENEMY:
            # Crie um novo inimigo e adicione aos grupos de sprites
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)    

        # Adicione um nova nuvem?
        elif event.type == ADDCLOUD:
            # Crie a nova nuvem e adicione ao grupo de sprites
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)   
        
    # Use o conjunto de teclas pressionadas e verifique a entrada do usuário
    pressed_keys = pygame.key.get_pressed()

    # Atualize o sprite do jogador com base nas teclas pressionadas
    player.update(pressed_keys)

    # Atualize a posição do inimigo
    enemies.update()
    clouds.update()

    # Fill the screen with sky blue Azul bebe
    screen.fill((135, 206, 250))

    # Desenhe todos os sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)


    # Verifique se qualquer inimigo colidiu com o jogador
    if pygame.sprite.spritecollideany(player, enemies):
        # Se sim, remova o jogador e pare o jogo
        player.kill()
        running = False

    # Atualize o display
    pygame.display.flip()

    # Esse comando programa quantos frames vai ter no jogo 
    clock.tick(60)
