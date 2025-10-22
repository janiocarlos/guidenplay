# importa pygame, random, os para usar no jogo
import pygame, random, os
# importa config as cfg para usar no jogo
import config as cfg
# inicia os módulos do pygame
pygame.init()

# configura suporte a controle/joystick
pygame.joystick.init()
# define controle
controle = pygame.joystick.Joystick(0) if pygame.joystick.get_count()>0 else None
# condição: se isso for verdade, faz o bloco abaixo
if controle: controle.init()
# função botao: bloco de código que executa uma tarefa
def botao(n): return bool(controle and controle.get_button(n))

# define tela
tela = pygame.display.set_mode((cfg.LARGURA_TELA, cfg.ALTURA_TELA))
# define o título da janela
pygame.display.set_caption(cfg.TITULO)
# define clock
clock = pygame.time.Clock()
# define fonte
fonte = pygame.font.SysFont(None, 36)

# função carregar_sprite: bloco de código que executa uma tarefa
def carregar_sprite(p, w, h):
# condição: se isso for verdade, faz o bloco abaixo
    if os.path.exists(p):
# carrega uma imagem do disco
        return pygame.transform.smoothscale(pygame.image.load(p).convert_alpha(), (w, h))
# devolve este valor para quem chamou a função
    return None

# define sprite_jogador
sprite_jogador = carregar_sprite(cfg.SPRITES["jogador"], cfg.LARGURA_JOGADOR, cfg.ALTURA_JOGADOR)
# define sprite_item
sprite_item = carregar_sprite(cfg.SPRITES["item"], cfg.LARGURA_ITEM, cfg.ALTURA_ITEM)
# define sprite_bomba
sprite_bomba = carregar_sprite(cfg.SPRITES["bomba"], cfg.LARGURA_ITEM, cfg.ALTURA_ITEM)

# CARREGAR FUNDO
# define fundo
fundo = None
# condição: se isso for verdade, faz o bloco abaixo
if os.path.exists(cfg.SPRITE_FUNDO):
# define fundo_bruto
    fundo_bruto = pygame.image.load(cfg.SPRITE_FUNDO).convert()
# define fundo
    fundo = pygame.transform.smoothscale(fundo_bruto, (cfg.LARGURA_TELA, cfg.ALTURA_TELA))

# função tela_inicial: bloco de código que executa uma tarefa
def tela_inicial():
    # mostra a tela de início do jogo até o jogador apertar START ou ESPAÇO.
# define esperando
    esperando = True
# laço: repete enquanto a condição for verdadeira
    while esperando:
# laço: repete para cada item
        for e in pygame.event.get():
# condição: se isso for verdade, faz o bloco abaixo
            if e.type == pygame.QUIT:
# encerra o pygame e fecha a janela
                pygame.quit()
# chama uma função/método para executar uma ação
                exit()
# define teclas
        teclas = pygame.key.get_pressed()
# define start
        start = botao(5) or teclas[pygame.K_SPACE] or teclas[pygame.K_RETURN]

# chama uma função/método para executar uma ação
        tela.fill(cfg.PRETO)
# define titulo (título que aparece na barra da janela)
        titulo = fonte.render(cfg.TITULO, True, cfg.BRANCO)
# define instrucao
        instrucao = fonte.render("APERTE START OU ESPAÇO PARA COMEÇAR", True, cfg.BRANCO)
# desenha essa superfície/Imagem na tela
        tela.blit(titulo, (cfg.LARGURA_TELA//2 - titulo.get_width()//2, cfg.ALTURA_TELA//2 - 60))
# desenha essa superfície/Imagem na tela
        tela.blit(instrucao, (cfg.LARGURA_TELA//2 - instrucao.get_width()//2, cfg.ALTURA_TELA//2 + 10))
# chama uma função/método para executar uma ação
        pygame.display.update()
# limita os FPS para manter a velocidade estável
        clock.tick(30)

# condição: se isso for verdade, faz o bloco abaixo
        if start:
# define esperando
            esperando = False

# função jogo: bloco de código que executa uma tarefa
def jogo():
# define jogador
    jogador = pygame.Rect(cfg.X_JOGADOR, cfg.Y_JOGADOR, cfg.LARGURA_JOGADOR, cfg.ALTURA_JOGADOR)
# define itens, bombas
    itens, bombas = [], []
# define pontos
    pontos = 0
# define vidas
    vidas = cfg.VIDAS_INICIO
# define acabou
    acabou = False
# define rodando
    rodando = True

# laço: repete enquanto a condição for verdadeira
    while rodando:
# laço: repete para cada item
        for e in pygame.event.get():
# condição: se isso for verdade, faz o bloco abaixo
            if e.type == pygame.QUIT:
# define rodando
                rodando = False

# define teclas
        teclas = pygame.key.get_pressed()
# define cima
        cima  = botao(6) or teclas[pygame.K_w]
# define baixo
        baixo = botao(1) or teclas[pygame.K_s]
# define start
        start = botao(5) or teclas[pygame.K_SPACE]

# condição: se isso for verdade, faz o bloco abaixo
        if not acabou:
# condição: se isso for verdade, faz o bloco abaixo
            if cima and jogador.y > 0: jogador.y -= cfg.VEL_JOGADOR
# condição: se isso for verdade, faz o bloco abaixo
            if baixo and jogador.y < cfg.ALTURA_TELA - jogador.height: jogador.y += cfg.VEL_JOGADOR

# condição: se isso for verdade, faz o bloco abaixo
            if random.randint(1, cfg.FREQ_ITEM) == 1:
# define y
                y = random.randint(0, cfg.ALTURA_TELA - cfg.ALTURA_ITEM)
# condição: se isso for verdade, faz o bloco abaixo
                if random.randint(1, 5) == 1:
# chama uma função/método para executar uma ação
                    bombas.append(pygame.Rect(cfg.LARGURA_TELA, y, cfg.LARGURA_ITEM, cfg.ALTURA_ITEM))
# caso contrário, cai aqui
                else:
# chama uma função/método para executar uma ação
                    itens.append(pygame.Rect(cfg.LARGURA_TELA, y, cfg.LARGURA_ITEM, cfg.ALTURA_ITEM))

# laço: repete para cada item
            for l in itens + bombas: l.x -= cfg.VEL_ITEM
# define itens
            itens = [l for l in itens if l.right > 0]
# define bombas
            bombas = [l for l in bombas if l.right > 0]

# laço: repete para cada item
            for i in itens:
# condição: se isso for verdade, faz o bloco abaixo
                if jogador.colliderect(i): pontos += 1; itens.remove(i); break
# laço: repete para cada item
            for b in bombas:
# condição: se isso for verdade, faz o bloco abaixo
                if jogador.colliderect(b): vidas -= 1; bombas.remove(b); break
# condição: se isso for verdade, faz o bloco abaixo
            if vidas <= 0: acabou = True
# caso contrário, cai aqui
        else:
# condição: se isso for verdade, faz o bloco abaixo
            if start:
# define pontos, vidas
                pontos, vidas = 0, cfg.VIDAS_INICIO
# define itens.clear(); bombas.clear(); acabou
                itens.clear(); bombas.clear(); acabou = False; jogador.y = cfg.Y_JOGADOR

        # desenha o fundo se existir, se não existir, pinta de branco
# condição: se isso for verdade, faz o bloco abaixo
        if fundo:
# desenha essa superfície/Imagem na tela
            tela.blit(fundo, (0, 0))
# caso contrário, cai aqui
        else:
# chama uma função/método para executar uma ação
            tela.fill(cfg.BRANCO)

# condição: se isso for verdade, faz o bloco abaixo
        if sprite_jogador: tela.blit(sprite_jogador, jogador)
# caso contrário, cai aqui
        else: pygame.draw.rect(tela, cfg.PRETO, jogador)
# laço: repete para cada item
        for i in itens:
# condição: se isso for verdade, faz o bloco abaixo
            if sprite_item: tela.blit(sprite_item, i)
# caso contrário, cai aqui
            else: pygame.draw.rect(tela, cfg.VERDE, i)
# laço: repete para cada item
        for b in bombas:
# condição: se isso for verdade, faz o bloco abaixo
            if sprite_bomba: tela.blit(sprite_bomba, b)
# caso contrário, cai aqui
            else: pygame.draw.rect(tela, cfg.VERMELHO, b)
# desenha essa superfície/Imagem na tela
        tela.blit(fonte.render(f"PONTOS: {pontos}  VIDAS: {vidas}", True, cfg.PRETO), (10, 10))
# chama uma função/método para executar uma ação
        pygame.display.update()
# limita os FPS para manter a velocidade estável
        clock.tick(cfg.FPS)
# encerra o pygame e fecha a janela
    pygame.quit()

# condição: se isso for verdade, faz o bloco abaixo
if __name__ == "__main__":
# chama uma função/método para executar uma ação
    tela_inicial()
# chama uma função/método para executar uma ação
    jogo()
