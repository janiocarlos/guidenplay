
import pygame

ALMOST_BLACK = (50,50,50)
RED = (255,0,0)
GREEN = (0,255,0)
DARK_SLATE_BLUE = (72,61,139)
LIGHT_SEA_GREEN = (32,178,170)

FPS = 60

clock = pygame.time.Clock()

pygame.init()

tela = pygame.display.set_mode((500,500),True,32)
pygame.display.set_caption("Meu primeiro jogo")

# Carregando os sprites desta tela

player_image = pygame.image.load('player.png').convert_alpha()
player = pygame.transform.scale(player_image, (50,75))

bush_image = pygame.image.load('arbusto.png').convert_alpha()
bush = pygame.transform.scale(bush_image, (100,100))

cloud_image = pygame.image.load('cloud.png').convert_alpha()
cloud = pygame.transform.scale(cloud_image, (100,100))

rodando = True
cont = 0
yy = 0

while rodando:

    tela.fill((0,180,250))
    pygame.draw.rect(tela, (0,100,20), [0, 300, 500, 200])
    tela.blit(player,(50,250))
    tela.blit(bush, (180, 250))

    if cont/60 <= 10:
        cont = cont + 1


    tela.blit(cloud, (300 - 50*(cont / 60), 20+yy))

    for evento in pygame.event.get():

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                yy = yy-10
            elif evento.key == pygame.K_DOWN:
                yy = yy + 10

        if evento.type == pygame.QUIT:
            rodando = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()