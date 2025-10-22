# imports e init
# importa pygame, random, os para usar no jogo
import pygame, random, os
# importa config as cfg para usar no jogo
import config as cfg
# inicia os módulos do pygame
pygame.init()

# inicia e configura o joystick
# configura suporte a controle/joystick
pygame.joystick.init()
# condição: se isso for verdade, faz o bloco abaixo
if pygame.joystick.get_count() > 0:  # se tiver pelo menos um
# define controle
    controle = pygame.joystick.Joystick(0)  # pega o primeiro, "Joystick(0)" e guarda em controle
# chama uma função/método para executar uma ação
    controle.init()
# chama uma função/método para executar uma ação
    print(f"Controle detectado: {controle.get_name()}")
# caso contrário, cai aqui
else:
# define controle
    controle = None  # evita erros ao tentar ler os botoes
# chama uma função/método para executar uma ação
    print("Nenhum controle detectado")

# função botao: bloco de código que executa uma tarefa
def botao(n):
    # retorna True se o botão n estiver pressionado.
# condição: se isso for verdade, faz o bloco abaixo
    if controle:
# devolve este valor para quem chamou a função
        return bool(controle.get_button(n))
# devolve este valor para quem chamou a função
    return False  # se não tiver, retorna sempre False

# janela
# define tela
tela = pygame.display.set_mode((cfg.LARGURA_TELA, cfg.ALTURA_TELA))
# define o título da janela
pygame.display.set_caption(cfg.TITULO)
# define relogio
relogio = pygame.time.Clock()
# define fonte
fonte = pygame.font.SysFont(None, 32)

# função carregar_sprite: bloco de código que executa uma tarefa
def carregar_sprite(sprite, largura, altura):
# condição: se isso for verdade, faz o bloco abaixo
    if os.path.exists(sprite):
# devolve este valor para quem chamou a função
        return pygame.transform.smoothscale(
# carrega uma imagem do disco
            pygame.image.load(sprite).convert_alpha(),
            (largura, altura)
        )
# devolve este valor para quem chamou a função
    return None

# define sprite_jogador
sprite_jogador = carregar_sprite(cfg.SPRITES["jogador"], cfg.LARGURA_JOGADOR, cfg.ALTURA_JOGADOR)
# define sprite_tiro
sprite_tiro    = carregar_sprite(cfg.SPRITES["tiro"], cfg.LARGURA_TIRO,    cfg.ALTURA_TIRO)

# função cortar_frames_sheet: bloco de código que executa uma tarefa
def cortar_frames_sheet(
    caminho,
    qtd_frames,
    largura_final,
    altura_final,
# define orientacao
    orientacao="vertical",   # "horizontal" ou "vertical"
# define margin
    margin=0,                  # margem do sheet
# define spacing
    spacing=0,                 # espaço entre frames
# define frame_w
    frame_w=32,              # largura do frame dentro do sheet (opcional)
# define frame_h
    frame_h=32               # altura do frame dentro do sheet (opcional)
):
# define frames
    frames = []
# condição: se isso for verdade, faz o bloco abaixo
    if not os.path.exists(caminho):
# devolve este valor para quem chamou a função
        return frames

# define sheet
    sheet = pygame.image.load(caminho).convert_alpha()
# define sheet_w, sheet_h
    sheet_w, sheet_h = sheet.get_width(), sheet.get_height()

    # Recorta
# laço: repete para cada item
    for i in range(qtd_frames):
# condição: se isso for verdade, faz o bloco abaixo
        if orientacao == "horizontal":
# define x
            x = margin + i * (frame_w + spacing)
# define y
            y = margin
# caso contrário, cai aqui
        else:  # vertical
# define x
            x = margin
# define y
            y = margin + i * (frame_h + spacing)

        # área de recorte (x, y, w, h)
# define rect
        rect = pygame.Rect(x, y, frame_w, frame_h)

        # cria superfície do frame e copia o pedaço do sheet
# define frame_surface
        frame_surface = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA, 32)
# desenha essa superfície/Imagem na tela
        frame_surface.blit(sheet, (0, 0), rect)

        # redimensiona para caber no Rect do meteoro (colisão fica certinha)
# define frame_surface
        frame_surface = pygame.transform.smoothscale(frame_surface, (largura_final, altura_final))
# chama uma função/método para executar uma ação
        frames.append(frame_surface)

# devolve este valor para quem chamou a função
    return frames


# Carregar frames do meteoro a partir do sheet
# define sprite_meteoro_frames
sprite_meteoro_frames = []
# condição: se isso for verdade, faz o bloco abaixo
if "meteoro_sheet" in cfg.SPRITES:
# define qtd
    qtd       = cfg.SPRITES.get("meteoro_frames_qtd", 2)
# define orient
    orient    = cfg.SPRITES.get("meteoro_orientacao", "horizontal").lower()
# define margin
    margin    = cfg.SPRITES.get("meteoro_margin", 0)
# define spacing
    spacing   = cfg.SPRITES.get("meteoro_spacing", 0)
# define frame_w
    frame_w   = cfg.SPRITES.get("meteoro_frame_w", 32)
# define frame_h
    frame_h   = cfg.SPRITES.get("meteoro_frame_h", 32)

# define sprite_meteoro_frames
    sprite_meteoro_frames = cortar_frames_sheet(
        cfg.SPRITES["meteoro_sheet"],
# define qtd_frames
        qtd_frames=qtd,
# define largura_final
        largura_final=cfg.LARGURA_METEORO,
# define altura_final
        altura_final=cfg.ALTURA_METEORO,
# define orientacao
        orientacao=orient,
# define margin
        margin=margin,
# define spacing
        spacing=spacing,
# define frame_w
        frame_w=frame_w,
# define frame_h
        frame_h=frame_h
    )


# CARREGAR FUNDO
# define fundo
fundo = None
# condição: se isso for verdade, faz o bloco abaixo
if hasattr(cfg, "SPRITE_FUNDO") and os.path.exists(cfg.SPRITE_FUNDO):
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
        for event in pygame.event.get():
# condição: se isso for verdade, faz o bloco abaixo
            if event.type == pygame.QUIT:
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
        relogio.tick(30)

# condição: se isso for verdade, faz o bloco abaixo
        if start:
# define esperando
            esperando = False

# função jogo: bloco de código que executa uma tarefa
def jogo():
# define jogador
    jogador = pygame.Rect(cfg.X_JOGADOR, cfg.Y_JOGADOR, cfg.LARGURA_JOGADOR, cfg.ALTURA_JOGADOR)
# define tiros, meteoros
    tiros, meteoros = [], []
# define pontos
    pontos = 0
# define acabou
    acabou = False
# define cooldown
    cooldown = 0
# define rodando
    rodando = True

    # --- animação do meteoro (global simples para todos os meteoros) ---
# define anim_index
    anim_index = 0
# define anim_timer
    anim_timer = 0
# define ANIM_COOLDOWN
    ANIM_COOLDOWN = 8  # menor = mais rápido; maior = mais lento

# laço: repete enquanto a condição for verdadeira
    while rodando:
# laço: repete para cada item
        for e in pygame.event.get():
# condição: se isso for verdade, faz o bloco abaixo
            if e.type == pygame.QUIT:
# define rodando
                rodando = False

# define teclas
        teclas   = pygame.key.get_pressed()
# define esquerda
        esquerda = botao(3) or teclas[pygame.K_a]
# define direita
        direita  = botao(2) or teclas[pygame.K_d]
# define atirar
        atirar   = botao(4) or teclas[pygame.K_SPACE]
# define start
        start    = botao(5)

# condição: se isso for verdade, faz o bloco abaixo
        if not acabou:
            # movimento
# condição: se isso for verdade, faz o bloco abaixo
            if esquerda and jogador.x > 0:
# define jogador.x -
                jogador.x -= cfg.VEL_JOGADOR
# condição: se isso for verdade, faz o bloco abaixo
            if direita and jogador.x < cfg.LARGURA_TELA - jogador.width:
# define jogador.x +
                jogador.x += cfg.VEL_JOGADOR

            # tiro
# condição: se isso for verdade, faz o bloco abaixo
            if cooldown > 0:
# define cooldown -
                cooldown -= 1
# condição: se isso for verdade, faz o bloco abaixo
            if atirar and cooldown == 0:
# define bx
                bx = jogador.x + jogador.width // 2 - cfg.LARGURA_TIRO // 2
# define by
                by = jogador.y - cfg.ALTURA_TIRO
# chama uma função/método para executar uma ação
                tiros.append(pygame.Rect(bx, by, cfg.LARGURA_TIRO, cfg.ALTURA_TIRO))
# define cooldown
                cooldown = cfg.COOLDOWN

            # spawn de meteoro
# condição: se isso for verdade, faz o bloco abaixo
            if random.randint(1, cfg.FREQ_METEORO) == 1:
# define x
                x = random.randint(0, cfg.LARGURA_TELA - cfg.LARGURA_METEORO)
# chama uma função/método para executar uma ação
                meteoros.append(pygame.Rect(x, -cfg.ALTURA_METEORO, cfg.LARGURA_METEORO, cfg.ALTURA_METEORO))

            # mover projéteis/meteoros
# laço: repete para cada item
            for t in tiros:
# define t.y -
                t.y -= cfg.VEL_TIRO
# laço: repete para cada item
            for m in meteoros:
# define m.y +
                m.y += cfg.VEL_METEORO

            # limpar fora da tela
# define tiros
            tiros = [t for t in tiros if t.bottom > 0]
# define meteoros
            meteoros = [m for m in meteoros if m.top < cfg.ALTURA_TELA]

            # colisões
# laço: repete para cada item
            for m in meteoros:
# condição: se isso for verdade, faz o bloco abaixo
                if jogador.colliderect(m):
# define acabou
                    acabou = True
# sai do laço agora
                    break
# condição: se isso for verdade, faz o bloco abaixo
            if not acabou:
                # cuidado ao remover enquanto itera: usa cópias rasas
# laço: repete para cada item
                for t in tiros[:]:
# define hit
                    hit = False
# laço: repete para cada item
                    for m in meteoros[:]:
# condição: se isso for verdade, faz o bloco abaixo
                        if t.colliderect(m):
# chama uma função/método para executar uma ação
                            meteoros.remove(m)
# chama uma função/método para executar uma ação
                            tiros.remove(t)
# define pontos +
                            pontos += 1
# define hit
                            hit = True
# sai do laço agora
                            break
# condição: se isso for verdade, faz o bloco abaixo
                    if hit:
# pula para a próxima volta do laço
                        continue

            # --- atualizar animação dos meteoros ---
# condição: se isso for verdade, faz o bloco abaixo
            if sprite_meteoro_frames:
# define anim_timer +
                anim_timer += 1
# condição: se isso for verdade, faz o bloco abaixo
                if anim_timer >= ANIM_COOLDOWN:
# define anim_timer
                    anim_timer = 0
# define anim_index
                    anim_index = (anim_index + 1) % len(sprite_meteoro_frames)

# caso contrário, cai aqui
        else:
# condição: se isso for verdade, faz o bloco abaixo
            if start:
# define jogador.x
                jogador.x = cfg.X_JOGADOR; jogador.y = cfg.Y_JOGADOR
# chama uma função/método para executar uma ação
                tiros.clear(); meteoros.clear()
# define pontos
                pontos = 0; acabou = False; cooldown = 0
# define anim_index
                anim_index = 0; anim_timer = 0  # reset da animação

        # desenha o fundo se existir
# condição: se isso for verdade, faz o bloco abaixo
        if fundo:
# desenha essa superfície/Imagem na tela
            tela.blit(fundo, (0, 0))
# caso contrário, cai aqui
        else:
# chama uma função/método para executar uma ação
            tela.fill(cfg.PRETO)

        # jogador
# condição: se isso for verdade, faz o bloco abaixo
        if sprite_jogador:
# desenha essa superfície/Imagem na tela
            tela.blit(sprite_jogador, jogador)
# caso contrário, cai aqui
        else:
# chama uma função/método para executar uma ação
            pygame.draw.rect(tela, (100, 180, 255), jogador)

        # tiros
# laço: repete para cada item
        for t in tiros:
# condição: se isso for verdade, faz o bloco abaixo
            if sprite_tiro:
# desenha essa superfície/Imagem na tela
                tela.blit(sprite_tiro, t)
# caso contrário, cai aqui
            else:
# chama uma função/método para executar uma ação
                pygame.draw.rect(tela, cfg.BRANCO, t)

        # meteoros (usa frame atual da animação, se houver)
# laço: repete para cada item
        for m in meteoros:
# condição: se isso for verdade, faz o bloco abaixo
            if sprite_meteoro_frames:
# desenha essa superfície/Imagem na tela
                tela.blit(sprite_meteoro_frames[anim_index], m)
# caso contrário, cai aqui
            else:
# chama uma função/método para executar uma ação
                pygame.draw.rect(tela, cfg.VERMELHO, m)

        # HUD
# desenha essa superfície/Imagem na tela
        tela.blit(fonte.render(f"PONTOS: {pontos}", True, cfg.BRANCO), (10, 10))
# condição: se isso for verdade, faz o bloco abaixo
        if acabou:
# define msg
            msg = fonte.render("PERDEU! START PARA REINICIAR", True, cfg.BRANCO)
# desenha essa superfície/Imagem na tela
            tela.blit(msg, (cfg.LARGURA_TELA//2 - msg.get_width()//2, cfg.ALTURA_TELA//2))

# chama uma função/método para executar uma ação
        pygame.display.update()
# limita os FPS para manter a velocidade estável
        relogio.tick(cfg.FPS)

# encerra o pygame e fecha a janela
    pygame.quit()

# condição: se isso for verdade, faz o bloco abaixo
if __name__ == "__main__":
# chama uma função/método para executar uma ação
    tela_inicial()
# chama uma função/método para executar uma ação
    jogo()
