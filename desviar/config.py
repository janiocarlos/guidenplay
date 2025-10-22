# define TITULO (título que aparece na barra da janela)
TITULO = "DESVIAR"
# define LARGURA_TELA (largura da janela do jogo em pixels)
LARGURA_TELA = 1920
# define ALTURA_TELA (altura da janela do jogo em pixels)
ALTURA_TELA = 1080
# define FPS (quadros por segundo (velocidade do jogo))
FPS = 60

# define BRANCO (cor branca)
BRANCO = (255, 255, 255)
# define PRETO (cor preta)
PRETO = (0, 0, 0)
# define VERMELHO (cor vermelha)
VERMELHO = (255, 0, 0)

# define LARGURA_JOGADOR
LARGURA_JOGADOR = 150
# define ALTURA_JOGADOR
ALTURA_JOGADOR = 150
# define X_JOGADOR
X_JOGADOR = 300
# define Y_JOGADOR
Y_JOGADOR = ALTURA_TELA // 2 - ALTURA_JOGADOR // 2
# define VEL_JOGADOR
VEL_JOGADOR = 10

# define LARGURA_OBS
LARGURA_OBS = 225
# define ALTURA_OBS
ALTURA_OBS = 225
# define VEL_OBS
VEL_OBS = 8
# define FREQ_OBS
FREQ_OBS = 25

# define SPRITES
SPRITES = {
    "jogador": "sprites/jogador.png",
    "obstaculo": "sprites/obstaculo.png"
}

# define SPRITE_FUNDO
SPRITE_FUNDO = "sprites/fundo.png"
# define FUNDO_ROLA
FUNDO_ROLA = True
# define VEL_FUNDO
VEL_FUNDO = 4

# define SPRITESHEET_JOGADOR
SPRITESHEET_JOGADOR = "sprites/jogador_spritesheet.png"
# define SHEET_W
SHEET_W = LARGURA_JOGADOR
# define SHEET_H
SHEET_H = ALTURA_JOGADOR
# define SHEET_FRAMES
SHEET_FRAMES = 0
# define SHEET_MARGEM
SHEET_MARGEM = 0
# define SHEET_ESP
SHEET_ESP = 0
# define SHEET_FPS (quadros por segundo (velocidade do jogo))
SHEET_FPS = 10
