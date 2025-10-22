# importa pygame, random, os para usar no jogo
import pygame, random, os
# importa config as cfg para usar no jogo
import config as cfg
# inicia os módulos do pygame
pygame.init()

# define BASE_DIR
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# função cam: bloco de código que executa uma tarefa
def cam(p): return os.path.join(BASE_DIR, p) if p else ""

# configura suporte a controle/joystick
pygame.joystick.init()
# condição: se isso for verdade, faz o bloco abaixo
if pygame.joystick.get_count() > 0:
# define controle
    controle = pygame.joystick.Joystick(0); controle.init(); print(f"Controle: {controle.get_name()}")
# caso contrário, cai aqui
else:
# define controle
    controle = None; print("Nenhum controle detectado")
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

# função load: bloco de código que executa uma tarefa
def load(rel):
# condição: se isso for verdade, faz o bloco abaixo
    if not rel: return None
# define p
    p = cam(rel)
# condição: se isso for verdade, faz o bloco abaixo
    if not os.path.exists(p):
# chama uma função/método para executar uma ação
        print(f"[AVISO] ausente: {p}")
# devolve este valor para quem chamou a função
        return None
# carrega uma imagem do disco
    return pygame.image.load(p).convert_alpha()

# função sheet_grid: bloco de código que executa uma tarefa
def sheet_grid(path, w, h, total=None, margem=0, esp=0, scale=None):
# condição: se isso for verdade, faz o bloco abaixo
    if not path or not os.path.exists(path): return []
# define sheet
    sheet = pygame.image.load(path).convert_alpha()
# define W, H
    W, H = sheet.get_width(), sheet.get_height()
# define cols
    cols = (W - 2*margem + esp) // (w + esp)
# define rows
    rows = (H - 2*margem + esp) // (h + esp)
# define maxf
    maxf = max(0, cols*rows)
# condição: se isso for verdade, faz o bloco abaixo
    if total is None or total > maxf: total = maxf
# define frames, k
    frames, k = [], 0
# laço: repete para cada item
    for r in range(rows):
# laço: repete para cada item
        for c in range(cols):
# condição: se isso for verdade, faz o bloco abaixo
            if k >= total: break
# define rect
            rect = pygame.Rect(margem + c*(w+esp), margem + r*(h+esp), w, h)
# condição: se isso for verdade, faz o bloco abaixo
            if rect.right <= W and rect.bottom <= H:
# define img
                img = sheet.subsurface(rect)
# condição: se isso for verdade, faz o bloco abaixo
                if scale: img = pygame.transform.smoothscale(img, scale)
# define frames.append(img); k +
                frames.append(img); k += 1
# condição: se isso for verdade, faz o bloco abaixo
        if k >= total: break
# devolve este valor para quem chamou a função
    return frames

# define img_jog
img_jog = load(cfg.SPRITES.get("jogador",""))
# define sheet_path
sheet_path = cam(getattr(cfg,"SPRITESHEET_JOGADOR",""))
# define use_sheet
use_sheet = os.path.exists(sheet_path) if sheet_path else False
# define _total
_total = getattr(cfg,"SHEET_FRAMES",0); _total = None if _total <= 0 else _total
# define frames_jog
frames_jog = sheet_grid(
    sheet_path,
# chama uma função/método para executar uma ação
    getattr(cfg,"SHEET_W", cfg.LARGURA_JOGADOR),
# chama uma função/método para executar uma ação
    getattr(cfg,"SHEET_H", cfg.ALTURA_JOGADOR),
# define total
    total=_total,
# define margem
    margem=getattr(cfg,"SHEET_MARGEM",0),
# define esp
    esp=getattr(cfg,"SHEET_ESP",0),
# define scale
    scale=(cfg.LARGURA_JOGADOR, cfg.ALTURA_JOGADOR)
) if use_sheet else []
# define sheet_fps (quadros por segundo (velocidade do jogo))
sheet_fps = getattr(cfg,"SHEET_FPS",10)

# define img_obs
img_obs = load(cfg.SPRITES.get("obstaculo",""))

# define img_fundo
img_fundo = None
# condição: se isso for verdade, faz o bloco abaixo
if getattr(cfg,"SPRITE_FUNDO",None):
# define tmp
    tmp = load(cfg.SPRITE_FUNDO)
# condição: se isso for verdade, faz o bloco abaixo
    if tmp: img_fundo = pygame.transform.smoothscale(tmp, (cfg.LARGURA_TELA, cfg.ALTURA_TELA))
# define fundo_rola
fundo_rola = bool(getattr(cfg,"FUNDO_ROLA",False))
# define vel_fundo
vel_fundo = getattr(cfg,"VEL_FUNDO",3)
# define bg_x1, bg_x2
bg_x1, bg_x2 = 0, cfg.LARGURA_TELA

# define mask_jogador_estatica
mask_jogador_estatica = None
# define masks_jogador_frames
masks_jogador_frames = []
# condição: se isso for verdade, faz o bloco abaixo
if frames_jog:
# define masks_jogador_frames
    masks_jogador_frames = [pygame.mask.from_surface(fr) for fr in frames_jog]
# outra condição: se a de cima falhar, testa esta
elif img_jog:
# define _j
    _j = pygame.transform.smoothscale(img_jog, (cfg.LARGURA_JOGADOR, cfg.ALTURA_JOGADOR))
# define mask_jogador_estatica
    mask_jogador_estatica = pygame.mask.from_surface(_j)

# define mask_obstaculo
mask_obstaculo = None
# define _obs_scaled
_obs_scaled = None
# condição: se isso for verdade, faz o bloco abaixo
if img_obs:
# define _obs_scaled
    _obs_scaled = pygame.transform.smoothscale(img_obs, (cfg.LARGURA_OBS, cfg.ALTURA_OBS))
# define mask_obstaculo
    mask_obstaculo = pygame.mask.from_surface(_obs_scaled)

# função tela_inicial: bloco de código que executa uma tarefa
def tela_inicial():
# laço: repete enquanto a condição for verdadeira
    while True:
# laço: repete para cada item
        for e in pygame.event.get():
# condição: se isso for verdade, faz o bloco abaixo
            if e.type == pygame.QUIT: pygame.quit(); exit()
# define k
        k = pygame.key.get_pressed()
# define start
        start = botao(5) or k[pygame.K_SPACE] or k[pygame.K_RETURN]
# condição: se isso for verdade, faz o bloco abaixo
        if img_fundo:
# condição: se isso for verdade, faz o bloco abaixo
            if fundo_rola: tela.blit(img_fundo,(bg_x1,0)); tela.blit(img_fundo,(bg_x2,0))
# caso contrário, cai aqui
            else: tela.blit(img_fundo,(0,0))
# caso contrário, cai aqui
        else:
# chama uma função/método para executar uma ação
            tela.fill(cfg.BRANCO)
# define t
        t = fonte.render(cfg.TITULO, True, cfg.PRETO)
# define i
        i = fonte.render("START/ESPAÇO PARA COMEÇAR", True, cfg.PRETO)
# desenha essa superfície/Imagem na tela
        tela.blit(t,(cfg.LARGURA_TELA//2 - t.get_width()//2, cfg.ALTURA_TELA//2 - 50))
# desenha essa superfície/Imagem na tela
        tela.blit(i,(cfg.LARGURA_TELA//2 - i.get_width()//2, cfg.ALTURA_TELA//2 + 10))
# limita os FPS para manter a velocidade estável
        pygame.display.update(); clock.tick(30)
# condição: se isso for verdade, faz o bloco abaixo
        if start: return

# função jogo: bloco de código que executa uma tarefa
def jogo():
    global bg_x1, bg_x2
# define jogador
    jogador = pygame.Rect(cfg.X_JOGADOR, cfg.Y_JOGADOR, cfg.LARGURA_JOGADOR, cfg.ALTURA_JOGADOR)
# define obs
    obs = []
# define pontos
    pontos = 0
# define acabou
    acabou = False
# define running
    running = True
# define frame_ms
    frame_ms = max(1, int(1000 / sheet_fps))
# define frame_idx
    frame_idx = 0

# laço: repete enquanto a condição for verdadeira
    while running:
# laço: repete para cada item
        for e in pygame.event.get():
# condição: se isso for verdade, faz o bloco abaixo
            if e.type == pygame.QUIT: running = False

# define k
        k = pygame.key.get_pressed()
# define cima
        cima  = botao(0) or k[pygame.K_UP]   or k[pygame.K_w]
# define baixo
        baixo = botao(1) or k[pygame.K_DOWN] or k[pygame.K_s]
# define start
        start = botao(5) or k[pygame.K_RETURN]

# condição: se isso for verdade, faz o bloco abaixo
        if not acabou:
# condição: se isso for verdade, faz o bloco abaixo
            if cima and jogador.y > 0: jogador.y -= cfg.VEL_JOGADOR
# condição: se isso for verdade, faz o bloco abaixo
            if baixo and jogador.y < cfg.ALTURA_TELA - jogador.height: jogador.y += cfg.VEL_JOGADOR

# condição: se isso for verdade, faz o bloco abaixo
            if frames_jog: frame_idx = (pygame.time.get_ticks() // frame_ms) % len(frames_jog)

# condição: se isso for verdade, faz o bloco abaixo
            if random.randint(1, cfg.FREQ_OBS) == 1:
# define y
                y = random.randint(0, cfg.ALTURA_TELA - cfg.ALTURA_OBS)
# chama uma função/método para executar uma ação
                obs.append(pygame.Rect(cfg.LARGURA_TELA, y, cfg.LARGURA_OBS, cfg.ALTURA_OBS))

# laço: repete para cada item
            for o in obs: o.x -= cfg.VEL_OBS
# define obs
            obs = [o for o in obs if o.right > 0]

# laço: repete para cada item
            for o in obs:
# condição: se isso for verdade, faz o bloco abaixo
                if not jogador.colliderect(o): continue
# define colidiu
                colidiu = False
# condição: se isso for verdade, faz o bloco abaixo
                if mask_obstaculo and (masks_jogador_frames or mask_jogador_estatica):
# define off
                    off = (o.x - jogador.x, o.y - jogador.y)
# condição: se isso for verdade, faz o bloco abaixo
                    if masks_jogador_frames:
# condição: se isso for verdade, faz o bloco abaixo
                        if masks_jogador_frames[frame_idx].overlap(mask_obstaculo, off): colidiu = True
# caso contrário, cai aqui
                    else:
# condição: se isso for verdade, faz o bloco abaixo
                        if mask_jogador_estatica.overlap(mask_obstaculo, off): colidiu = True
# caso contrário, cai aqui
                else:
# define colidiu
                    colidiu = True
# condição: se isso for verdade, faz o bloco abaixo
                if colidiu:
# define acabou
                    acabou = True
# sai do laço agora
                    break

# define pontos +
            pontos += 1
# caso contrário, cai aqui
        else:
# condição: se isso for verdade, faz o bloco abaixo
            if start:
# define obs.clear(); pontos
                obs.clear(); pontos = 0; acabou = False
# define jogador.y
                jogador.y = cfg.Y_JOGADOR

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
            if fundo_rola: tela.blit(img_fundo,(bg_x1,0)); tela.blit(img_fundo,(bg_x2,0))
# caso contrário, cai aqui
            else: tela.blit(img_fundo,(0,0))
# caso contrário, cai aqui
        else:
# chama uma função/método para executar uma ação
            tela.fill(cfg.BRANCO)

# condição: se isso for verdade, faz o bloco abaixo
        if frames_jog:
# desenha essa superfície/Imagem na tela
            tela.blit(frames_jog[frame_idx], jogador)
# outra condição: se a de cima falhar, testa esta
        elif img_jog:
# desenha essa superfície/Imagem na tela
            tela.blit(pygame.transform.smoothscale(img_jog,(cfg.LARGURA_JOGADOR,cfg.ALTURA_JOGADOR)), jogador)
# caso contrário, cai aqui
        else:
# chama uma função/método para executar uma ação
            pygame.draw.rect(tela, cfg.PRETO, jogador)

# laço: repete para cada item
        for o in obs:
# condição: se isso for verdade, faz o bloco abaixo
            if img_obs:
# desenha essa superfície/Imagem na tela
                tela.blit(pygame.transform.smoothscale(img_obs,(cfg.LARGURA_OBS,cfg.ALTURA_OBS)), o)
# caso contrário, cai aqui
            else:
# chama uma função/método para executar uma ação
                pygame.draw.rect(tela, cfg.PRETO, o)

# desenha essa superfície/Imagem na tela
        tela.blit(fonte.render(f"PONTOS: {pontos}", True, cfg.PRETO), (10,10))
# condição: se isso for verdade, faz o bloco abaixo
        if acabou:
# define m
            m = fonte.render("PERDEU! START/ESPAÇO PARA REINICIAR", True, cfg.VERMELHO)
# desenha essa superfície/Imagem na tela
            tela.blit(m, (cfg.LARGURA_TELA//2 - m.get_width()//2, cfg.ALTURA_TELA//2))
# limita os FPS para manter a velocidade estável
        pygame.display.update(); clock.tick(cfg.FPS)
# encerra o pygame e fecha a janela
    pygame.quit()

# condição: se isso for verdade, faz o bloco abaixo
if __name__ == "__main__":
# chama uma função/método para executar uma ação
    tela_inicial(); jogo()
