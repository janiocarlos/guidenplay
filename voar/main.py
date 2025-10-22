# importa pygame, random, os para usar no jogo
import pygame, random, os
# importa config as cfg para usar no jogo
import config as cfg
# inicia os módulos do pygame
pygame.init()

# define BASE_DIR
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# função cam: bloco de código que executa uma tarefa
def cam(rel):
# devolve este valor para quem chamou a função
    return os.path.join(BASE_DIR, rel) if rel else ""

# configura suporte a controle/joystick
pygame.joystick.init()
# condição: se isso for verdade, faz o bloco abaixo
if pygame.joystick.get_count() > 0:
# define controle
    controle = pygame.joystick.Joystick(0)
# chama uma função/método para executar uma ação
    controle.init()
# chama uma função/método para executar uma ação
    print(f"Controle detectado: {controle.get_name()}")
# caso contrário, cai aqui
else:
# define controle
    controle = None
# chama uma função/método para executar uma ação
    print("Nenhum controle detectado")

# função botao: bloco de código que executa uma tarefa
def botao(n):
# condição: se isso for verdade, faz o bloco abaixo
    if controle:
# devolve este valor para quem chamou a função
        return bool(controle.get_button(n))
# devolve este valor para quem chamou a função
    return False

# define tela
tela = pygame.display.set_mode((cfg.LARGURA_TELA, cfg.ALTURA_TELA))
# define o título da janela
pygame.display.set_caption(cfg.TITULO)
# define relogio
relogio = pygame.time.Clock()
# define fonte
fonte = pygame.font.SysFont(None, 36)

# função carregar_imagem: bloco de código que executa uma tarefa
def carregar_imagem(rel):
# condição: se isso for verdade, faz o bloco abaixo
    if not rel:
# devolve este valor para quem chamou a função
        return None
# define abs_path
    abs_path = cam(rel)
# condição: se isso for verdade, faz o bloco abaixo
    if not os.path.exists(abs_path):
# chama uma função/método para executar uma ação
        print(f"[AVISO] Arquivo não encontrado: {abs_path}")
# devolve este valor para quem chamou a função
        return None
# carrega uma imagem do disco
    return pygame.image.load(abs_path).convert_alpha()

# função carregar_spritesheet_grid: bloco de código que executa uma tarefa
def carregar_spritesheet_grid(caminho, w, h, total=None, margem=0, esp=0, escala_para=None):
# condição: se isso for verdade, faz o bloco abaixo
    if not caminho or not os.path.exists(caminho):
# chama uma função/método para executar uma ação
        print(f"[AVISO] Spritesheet ausente: {caminho}")
# devolve este valor para quem chamou a função
        return []
# define sheet
    sheet = pygame.image.load(caminho).convert_alpha()
# define W, H
    W, H = sheet.get_width(), sheet.get_height()
# define cols
    cols = (W - 2*margem + esp) // (w + esp)
# define rows
    rows = (H - 2*margem + esp) // (h + esp)
# define max_frames
    max_frames = max(0, cols * rows)
# condição: se isso for verdade, faz o bloco abaixo
    if total is None or total > max_frames:
# define total
        total = max_frames
# define frames, count
    frames, count = [], 0
# laço: repete para cada item
    for r in range(rows):
# laço: repete para cada item
        for c in range(cols):
# condição: se isso for verdade, faz o bloco abaixo
            if count >= total: break
# define x
            x = margem + c * (w + esp)
# define y
            y = margem + r * (h + esp)
# define rect
            rect = pygame.Rect(x, y, w, h)
# condição: se isso for verdade, faz o bloco abaixo
            if rect.right <= W and rect.bottom <= H:
# define img
                img = sheet.subsurface(rect)
# condição: se isso for verdade, faz o bloco abaixo
                if escala_para:
# define img
                    img = pygame.transform.smoothscale(img, escala_para)
# chama uma função/método para executar uma ação
                frames.append(img)
# define count +
                count += 1
# condição: se isso for verdade, faz o bloco abaixo
        if count >= total: break
# condição: se isso for verdade, faz o bloco abaixo
    if not frames:
# chama uma função/método para executar uma ação
        print("[AVISO] Nenhum frame carregado da spritesheet")
# devolve este valor para quem chamou a função
    return frames

# define img_jogador_estatica
img_jogador_estatica = carregar_imagem(cfg.SPRITES.get("jogador", ""))
# define sheet_path
sheet_path = cam(getattr(cfg, "SPRITESHEET_JOGADOR", ""))
# define usa_sheet
usa_sheet = os.path.exists(sheet_path) if sheet_path else False
# define sheet_w
sheet_w = getattr(cfg, "SHEET_W", 60)
# define sheet_h
sheet_h = getattr(cfg, "SHEET_H", 50)
# define sheet_frames
sheet_frames = getattr(cfg, "SHEET_FRAMES", 0)
# define sheet_margem
sheet_margem = getattr(cfg, "SHEET_MARGEM", 0)
# define sheet_esp
sheet_esp = getattr(cfg, "SHEET_ESP", 0)
# define sheet_fps (quadros por segundo (velocidade do jogo))
sheet_fps = getattr(cfg, "SHEET_FPS", 10)
# define frames_jogador
frames_jogador = []
# condição: se isso for verdade, faz o bloco abaixo
if usa_sheet and sheet_frames > 0:
# define frames_jogador
    frames_jogador = carregar_spritesheet_grid(
        sheet_path, sheet_w, sheet_h,
# define total
        total=sheet_frames,
# define margem
        margem=sheet_margem, esp=sheet_esp,
# define escala_para
        escala_para=(cfg.LARGURA_JOGADOR, cfg.ALTURA_JOGADOR)
    )

# define img_fundo
img_fundo = None
# condição: se isso for verdade, faz o bloco abaixo
if hasattr(cfg, "SPRITE_FUNDO") and cfg.SPRITE_FUNDO:
# define tmp
    tmp = carregar_imagem(cfg.SPRITE_FUNDO)
# condição: se isso for verdade, faz o bloco abaixo
    if tmp:
# define img_fundo
        img_fundo = pygame.transform.smoothscale(tmp, (cfg.LARGURA_TELA, cfg.ALTURA_TELA))

# define fundo_rola
fundo_rola = bool(getattr(cfg, "FUNDO_ROLA", False))
# define vel_fundo
vel_fundo = getattr(cfg, "VEL_FUNDO", 3)
# define bg_x1, bg_x2
bg_x1, bg_x2 = 0, cfg.LARGURA_TELA

# função criar_par_canos: bloco de código que executa uma tarefa
def criar_par_canos():
# define y_gap
    y_gap = random.randint(120, cfg.ALTURA_TELA - 120 - cfg.VÃO)
# define topo
    topo = pygame.Rect(cfg.LARGURA_TELA, 0, cfg.LARGURA_CANO, y_gap)
# define baixo
    baixo = pygame.Rect(cfg.LARGURA_TELA, y_gap + cfg.VÃO, cfg.LARGURA_CANO, cfg.ALTURA_TELA - (y_gap + cfg.VÃO))
# devolve este valor para quem chamou a função
    return topo, baixo

# define spr_cano
spr_cano = carregar_imagem(cfg.SPRITES.get("cano", ""))

# define mask_player_static
mask_player_static = None
# define mask_player_frames
mask_player_frames = []
# condição: se isso for verdade, faz o bloco abaixo
if frames_jogador:
# define mask_player_frames
    mask_player_frames = [pygame.mask.from_surface(fr) for fr in frames_jogador]
# outra condição: se a de cima falhar, testa esta
elif img_jogador_estatica:
# define _scaled
    _scaled = pygame.transform.smoothscale(img_jogador_estatica, (cfg.LARGURA_JOGADOR, cfg.ALTURA_JOGADOR))
# define mask_player_static
    mask_player_static = pygame.mask.from_surface(_scaled)

# define _cano_cache
_cano_cache = {}
# função cano_surface_mask: bloco de código que executa uma tarefa
def cano_surface_mask(h):
# define key
    key = int(h)
# condição: se isso for verdade, faz o bloco abaixo
    if key in _cano_cache:
# devolve este valor para quem chamou a função
        return _cano_cache[key]
# condição: se isso for verdade, faz o bloco abaixo
    if not spr_cano:
# define _cano_cache[key]
        _cano_cache[key] = (None, None)
# devolve este valor para quem chamou a função
        return _cano_cache[key]
# define surf
    surf = pygame.transform.smoothscale(spr_cano, (cfg.LARGURA_CANO, key))
# define m
    m = pygame.mask.from_surface(surf)
# define _cano_cache[key]
    _cano_cache[key] = (surf, m)
# devolve este valor para quem chamou a função
    return surf, m

# função tela_inicial: bloco de código que executa uma tarefa
def tela_inicial():
# define esperando
    esperando = True
# laço: repete enquanto a condição for verdadeira
    while esperando:
# laço: repete para cada item
        for e in pygame.event.get():
# condição: se isso for verdade, faz o bloco abaixo
            if e.type == pygame.QUIT:
# encerra o pygame e fecha a janela
                pygame.quit(); exit()
# define teclas
        teclas = pygame.key.get_pressed()
# define start
        start = botao(5) or teclas[pygame.K_SPACE] or teclas[pygame.K_RETURN]
# condição: se isso for verdade, faz o bloco abaixo
        if img_fundo:
# condição: se isso for verdade, faz o bloco abaixo
            if fundo_rola:
# desenha essa superfície/Imagem na tela
                tela.blit(img_fundo, (bg_x1, 0)); tela.blit(img_fundo, (bg_x2, 0))
# caso contrário, cai aqui
            else:
# desenha essa superfície/Imagem na tela
                tela.blit(img_fundo, (0, 0))
# caso contrário, cai aqui
        else:
# chama uma função/método para executar uma ação
            tela.fill(cfg.BRANCO)
# define titulo (título que aparece na barra da janela)
        titulo = fonte.render(cfg.TITULO, True, cfg.PRETO)
# define instr
        instr = fonte.render("APERTE START/ESPAÇO PARA COMEÇAR", True, cfg.PRETO)
# desenha essa superfície/Imagem na tela
        tela.blit(titulo, (cfg.LARGURA_TELA//2 - titulo.get_width()//2, cfg.ALTURA_TELA//2 - 60))
# desenha essa superfície/Imagem na tela
        tela.blit(instr, (cfg.LARGURA_TELA//2 - instr.get_width()//2, cfg.ALTURA_TELA//2 + 10))
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
    global bg_x1, bg_x2
# define y
    y = cfg.ALTURA_TELA // 2
# define vy
    vy = 0
# define canos
    canos = []
# define frame
    frame = 0
# define pontos
    pontos = 0
# define acabou
    acabou = False
# define prev_b0
    prev_b0 = False

# define vel_cano
    vel_cano = getattr(cfg, "VEL_CANO_INICIAL", getattr(cfg, "VEL_CANO", 6))
# define aumento
    aumento = getattr(cfg, "AUMENTO_VEL", 0)
# define ciclo
    ciclo = getattr(cfg, "CICLO_AUMENTO", 999999)
# define vel_max
    vel_max = getattr(cfg, "VEL_CANO_MAX", 9999)

# define frame_ms
    frame_ms = max(1, int(1000 / sheet_fps))
# define frame_atual
    frame_atual = 0

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
# condição: se isso for verdade, faz o bloco abaixo
            if e.type == pygame.JOYBUTTONDOWN and controle and e.joy == 0:
# condição: se isso for verdade, faz o bloco abaixo
                if not acabou and e.button == 0:
# define vy
                    vy = cfg.PULO
# outra condição: se a de cima falhar, testa esta
                elif acabou and e.button == 5:
# define y
                    y = cfg.ALTURA_TELA // 2; vy = 0; canos.clear(); pontos = 0; frame = 0
# define acabou
                    acabou = False; vel_cano = getattr(cfg, "VEL_CANO_INICIAL", vel_cano)
# condição: se isso for verdade, faz o bloco abaixo
            if e.type == pygame.KEYDOWN:
# condição: se isso for verdade, faz o bloco abaixo
                if not acabou and e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
# define vy
                    vy = cfg.PULO
# outra condição: se a de cima falhar, testa esta
                elif acabou and e.key in (pygame.K_SPACE, pygame.K_RETURN):
# define y
                    y = cfg.ALTURA_TELA // 2; vy = 0; canos.clear(); pontos = 0; frame = 0
# define acabou
                    acabou = False; vel_cano = getattr(cfg, "VEL_CANO_INICIAL", vel_cano)

# define b0
        b0 = botao(0)
# condição: se isso for verdade, faz o bloco abaixo
        if not acabou and b0 and not prev_b0:
# define vy
            vy = cfg.PULO
# define prev_b0
        prev_b0 = b0

# condição: se isso for verdade, faz o bloco abaixo
        if not acabou:
# define frame +
            frame += 1
# condição: se isso for verdade, faz o bloco abaixo
            if aumento > 0 and frame % ciclo == 0:
# define vel_cano
                vel_cano = min(vel_cano + aumento, vel_max)

# define vy +
            vy += cfg.GRAVIDADE
# define y
            y = max(0, min(cfg.ALTURA_TELA - cfg.ALTURA_JOGADOR, y + vy))

# condição: se isso for verdade, faz o bloco abaixo
            if frames_jogador:
# define frame_atual
                frame_atual = (pygame.time.get_ticks() // frame_ms) % len(frames_jogador)

# condição: se isso for verdade, faz o bloco abaixo
            if frame % cfg.FREQ_CANO_FRAMES == 0:
# chama uma função/método para executar uma ação
                canos.append(criar_par_canos())

# define novos
            novos = []
# laço: repete para cada item
            for topo, baixo in canos:
# define topo.x -
                topo.x -= vel_cano; baixo.x -= vel_cano
# condição: se isso for verdade, faz o bloco abaixo
                if topo.right > 0:
# chama uma função/método para executar uma ação
                    novos.append((topo, baixo))
# caso contrário, cai aqui
                else:
# define pontos +
                    pontos += 1
# define canos
            canos = novos

# define jogador_rect
            jogador_rect = pygame.Rect(cfg.X_JOGADOR, y, cfg.LARGURA_JOGADOR, cfg.ALTURA_JOGADOR)
# condição: se isso for verdade, faz o bloco abaixo
            if y <= 0 or y + cfg.ALTURA_JOGADOR >= cfg.ALTURA_TELA:
# define acabou
                acabou = True
# caso contrário, cai aqui
            else:
# define colidiu
                colidiu = False
# laço: repete para cada item
                for topo, baixo in canos:
# condição: se isso for verdade, faz o bloco abaixo
                    if not jogador_rect.colliderect(topo) and not jogador_rect.colliderect(baixo):
# pula para a próxima volta do laço
                        continue
# condição: se isso for verdade, faz o bloco abaixo
                    if spr_cano and (mask_player_frames or mask_player_static):
# condição: se isso for verdade, faz o bloco abaixo
                        if jogador_rect.colliderect(topo):
# define _, mask_top
                            _, mask_top = cano_surface_mask(topo.height)
# condição: se isso for verdade, faz o bloco abaixo
                            if mask_top:
# condição: se isso for verdade, faz o bloco abaixo
                                if mask_player_frames:
# define off
                                    off = (topo.x - jogador_rect.x, topo.y - jogador_rect.y)
# condição: se isso for verdade, faz o bloco abaixo
                                    if mask_player_frames[frame_atual].overlap(mask_top, off):
# define colidiu
                                        colidiu = True
# caso contrário, cai aqui
                                else:
# define off
                                    off = (topo.x - jogador_rect.x, topo.y - jogador_rect.y)
# condição: se isso for verdade, faz o bloco abaixo
                                    if mask_player_static.overlap(mask_top, off):
# define colidiu
                                        colidiu = True
# condição: se isso for verdade, faz o bloco abaixo
                        if not colidiu and jogador_rect.colliderect(baixo):
# define _, mask_bot
                            _, mask_bot = cano_surface_mask(baixo.height)
# condição: se isso for verdade, faz o bloco abaixo
                            if mask_bot:
# condição: se isso for verdade, faz o bloco abaixo
                                if mask_player_frames:
# define off
                                    off = (baixo.x - jogador_rect.x, baixo.y - jogador_rect.y)
# condição: se isso for verdade, faz o bloco abaixo
                                    if mask_player_frames[frame_atual].overlap(mask_bot, off):
# define colidiu
                                        colidiu = True
# caso contrário, cai aqui
                                else:
# define off
                                    off = (baixo.x - jogador_rect.x, baixo.y - jogador_rect.y)
# condição: se isso for verdade, faz o bloco abaixo
                                    if mask_player_static.overlap(mask_bot, off):
# define colidiu
                                        colidiu = True
# caso contrário, cai aqui
                    else:
# condição: se isso for verdade, faz o bloco abaixo
                        if jogador_rect.colliderect(topo) or jogador_rect.colliderect(baixo):
# define colidiu
                            colidiu = True
# condição: se isso for verdade, faz o bloco abaixo
                    if colidiu:
# define acabou
                        acabou = True
# sai do laço agora
                        break

# condição: se isso for verdade, faz o bloco abaixo
        if img_fundo and fundo_rola:
# define bg_x1 -
            bg_x1 -= vel_fundo; bg_x2 -= vel_fundo
# condição: se isso for verdade, faz o bloco abaixo
            if bg_x1 <= -cfg.LARGURA_TELA: bg_x1 = bg_x2 + cfg.LARGURA_TELA
# condição: se isso for verdade, faz o bloco abaixo
            if bg_x2 <= -cfg.LARGURA_TELA: bg_x2 = bg_x1 + cfg.LARGURA_TELA

# condição: se isso for verdade, faz o bloco abaixo
        if img_fundo:
# condição: se isso for verdade, faz o bloco abaixo
            if fundo_rola:
# desenha essa superfície/Imagem na tela
                tela.blit(img_fundo, (bg_x1, 0)); tela.blit(img_fundo, (bg_x2, 0))
# caso contrário, cai aqui
            else:
# desenha essa superfície/Imagem na tela
                tela.blit(img_fundo, (0, 0))
# caso contrário, cai aqui
        else:
# chama uma função/método para executar uma ação
            tela.fill(cfg.BRANCO)

# condição: se isso for verdade, faz o bloco abaixo
        if frames_jogador:
# desenha essa superfície/Imagem na tela
            tela.blit(frames_jogador[frame_atual], (cfg.X_JOGADOR, y))
# outra condição: se a de cima falhar, testa esta
        elif img_jogador_estatica:
# define img
            img = pygame.transform.smoothscale(img_jogador_estatica, (cfg.LARGURA_JOGADOR, cfg.ALTURA_JOGADOR))
# desenha essa superfície/Imagem na tela
            tela.blit(img, (cfg.X_JOGADOR, y))
# caso contrário, cai aqui
        else:
# chama uma função/método para executar uma ação
            pygame.draw.rect(tela, cfg.PRETO, (cfg.X_JOGADOR, y, cfg.LARGURA_JOGADOR, cfg.ALTURA_JOGADOR))

# laço: repete para cada item
        for topo, baixo in canos:
# condição: se isso for verdade, faz o bloco abaixo
            if spr_cano:
# define surf_top, _
                surf_top, _ = cano_surface_mask(topo.height)
# define surf_bot, _
                surf_bot, _ = cano_surface_mask(baixo.height)
# condição: se isso for verdade, faz o bloco abaixo
                if surf_top: tela.blit(surf_top, topo)
# caso contrário, cai aqui
                else: pygame.draw.rect(tela, cfg.PRETO, topo)
# condição: se isso for verdade, faz o bloco abaixo
                if surf_bot: tela.blit(surf_bot, baixo)
# caso contrário, cai aqui
                else: pygame.draw.rect(tela, cfg.PRETO, baixo)
# caso contrário, cai aqui
            else:
# chama uma função/método para executar uma ação
                pygame.draw.rect(tela, cfg.PRETO, topo); pygame.draw.rect(tela, cfg.PRETO, baixo)

# desenha essa superfície/Imagem na tela
        tela.blit(fonte.render(f"PONTOS: {pontos}", True, cfg.PRETO), (10, 10))
# condição: se isso for verdade, faz o bloco abaixo
        if acabou:
# define msg
            msg = fonte.render("PERDEU! START/ESPAÇO PARA REINICIAR", True, cfg.VERMELHO)
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
