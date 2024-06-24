import pygame
import constantes
import os

pygame.init()

tela = pygame.display.set_mode((constantes.largura, constantes.altura))
pygame.display.set_caption('Mapeamento')

# Carrega e redimensiona a imagem de fundo
cenario_path = os.path.join(os.path.dirname(__file__), constantes.cenario)
bg = pygame.image.load(cenario_path).convert_alpha()
bg = pygame.transform.scale(bg, (constantes.largura, constantes.altura))

# Carrega a imagem do triângulo
triangulo_path = os.path.join(os.path.dirname(__file__), constantes.triangulo_imagem)
triangulo_imagem = pygame.image.load(triangulo_path).convert_alpha()
triangulo_imagem = pygame.transform.scale(triangulo_imagem, (100, 100))  # Ajuste o tamanho conforme necessário

# Ajusta a opacidade da imagem do triângulo
triangulo_imagem.set_alpha(constantes.opacidade_triangulo)  # Define a opacidade da imagem do triângulo conforme constantes

# Classe para o personagem estático
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(constantes.personagem).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))  # Ajuste o tamanho conforme necessário
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (50, constantes.altura - 50)  # Posiciona no canto inferior esquerdo

    def update(self):
        pass  # Não é necessário atualizar nada para um personagem estático

# Classe para o drone
class Drone(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(constantes.drone).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 40))  # Ajuste o tamanho conforme necessário
        self.rect = self.image.get_rect()
        self.rect.midbottom = (constantes.largura // 2, 50)  # Posiciona no topo da tela, no meio

        self.velocidade = 2
        self.direcao_horizontal = 0
        self.direcao_vertical = 0
        self.identificado = False  # Inicia como não identificado

    def update(self):
        self.rect.x += self.velocidade * self.direcao_horizontal
        self.rect.y += self.velocidade * self.direcao_vertical

    def desenhar_triangulo(self, tela):
        # Posiciona o triângulo abaixo do drone
        triangulo_rect = triangulo_imagem.get_rect(center=self.rect.midbottom)
        triangulo_rect.y += 50  # Ajuste a posição conforme necessário
        tela.blit(triangulo_imagem, triangulo_rect)

    def identificar(self):
        self.identificado = True

# Classe para o segundo cenário
class CenarioSecundario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(constantes.cenario_secundario).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constantes.largura * 2, 300))  # Ajuste o tamanho conforme necessário
        self.image.set_alpha(constantes.opacidade_cenario_secundario)  # Define a opacidade da imagem do cenário secundário
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, constantes.altura - 310)  # Posiciona inicialmente próximo ao fundo da tela

        self.velocidade_horizontal = 2

    def update(self):
        # Movimenta horizontalmente em loop
        self.rect.x -= self.velocidade_horizontal

        # Verifica se o cenário secundário atingiu as bordas da tela
        if self.rect.right <= 0:
            self.rect.x = constantes.largura  # Reposiciona à direita da tela quando a primeira parte sair da tela
        elif self.rect.left >= constantes.largura:
            self.rect.x = 0 - constantes.largura  # Reposiciona à esquerda da tela quando a segunda parte sair da tela

# Classe para a vítima
class Vitima(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(constantes.vitima).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))  # Ajuste o tamanho conforme necessário
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (constantes.largura // 2, constantes.altura - 418)  # Posição inicial da vítima

    def update(self):
        pass  # A vítima é estática, não precisa de atualização

# Criando os elementos do jogo
personagem = Personagem()
drone = Drone()
cenario_secundario = CenarioSecundario()
vitima = Vitima()

# Fonte para desenhar o texto
fonte = pygame.font.Font(None, 24)  # Ajuste o tamanho e a fonte conforme necessário

# Variável de controle do jogo
iniciando = True

# Loop principal do jogo
while iniciando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            iniciando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                drone.direcao_horizontal = -1  # Move o drone para a esquerda
            elif event.key == pygame.K_RIGHT:
                drone.direcao_horizontal = 1  # Move o drone para a direita
            elif event.key == pygame.K_UP:
                drone.direcao_vertical = -1  # Move o drone para cima
            elif event.key == pygame.K_DOWN:
                drone.direcao_vertical = 1  # Move o drone para baixo
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                drone.direcao_horizontal = 0  # Para de mover o drone horizontalmente
            elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                drone.direcao_vertical = 0  # Para de mover o drone verticalmente

    # Verifica colisão entre drone e vítima
    if drone.rect.colliderect(vitima.rect):
        drone.identificar()

    # Atualizações dos elementos do jogo
    drone.update()
    cenario_secundario.update()
    # Vitima não precisa ser atualizada pois é estática

    # Desenha a imagem de fundo
    tela.blit(bg, (0, 0))

    # Desenha os elementos na tela
    tela.blit(personagem.image, personagem.rect)
    tela.blit(drone.image, drone.rect)
    tela.blit(cenario_secundario.image, cenario_secundario.rect)
    tela.blit(vitima.image, vitima.rect)

    # Desenha o triângulo vermelho abaixo do drone com opacidade
    drone.desenhar_triangulo(tela)

    # Desenha o cenário secundário em loop
    if cenario_secundario.rect.right <= constantes.largura:
        tela.blit(cenario_secundario.image, (cenario_secundario.rect.x + constantes.largura, cenario_secundario.rect.y))

    # Desenha o nome da pessoa identificada
    if drone.identificado:
        texto = fonte.render("PESSOA IDENTIFICADA", True, (255, 0, 0))  # Texto vermelho
        texto_rect = texto.get_rect(center=(drone.rect.centerx, drone.rect.bottom + 10))  # Posição abaixo do drone
        tela.blit(texto, texto_rect)

    pygame.display.update()

# Encerra o Pygame
pygame.quit()
