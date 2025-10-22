# define TITULO (título que aparece na barra da janela)
TITULO = "ATIRAR VERTICAL"
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
VERMELHO = (200, 40, 40)

# JOGADOR
# define LARGURA_JOGADOR
LARGURA_JOGADOR = 50
# define ALTURA_JOGADOR
ALTURA_JOGADOR = 50
# define X_JOGADOR
X_JOGADOR = LARGURA_TELA // 2 - LARGURA_JOGADOR // 2
# define Y_JOGADOR
Y_JOGADOR = ALTURA_TELA - ALTURA_JOGADOR - 40
# define VEL_JOGADOR
VEL_JOGADOR = 9

# TIRO
# define LARGURA_TIRO
LARGURA_TIRO = 8
# define ALTURA_TIRO
ALTURA_TIRO = 18
# define VEL_TIRO
VEL_TIRO = 16
# define COOLDOWN
COOLDOWN = 8

# METEOROS
# define LARGURA_METEORO
LARGURA_METEORO = 56
# define ALTURA_METEORO
ALTURA_METEORO = 56
# define VEL_METEORO
VEL_METEORO = 6
# define FREQ_METEORO
FREQ_METEORO = 28

# define SPRITES
SPRITES = {
    "jogador": "atirar_vertical/sprites/jogador.png",
    "tiro": "atirar_vertical/sprites/tiro.png",

    # seu spritesheet do meteoro
    "meteoro_sheet": "atirar_vertical/sprites/meteoro_spritesheet.png",
    "meteoro_frames_qtd": 2,

    # NOVOS (opcionais, mas ajudam a não cortar)
    "meteoro_orientacao": "vertical",  # "horizontal" OU "vertical" para se a spritesheet é em linhas ou colunas
    "meteoro_margin": 0,                 # pixels de margem nas bordas do sheet
    "meteoro_spacing": 0,                # pixels entre um frame e outro

    "meteoro_frame_w": 32,
    "meteoro_frame_h": 32,
}


# FUNDO (OPCIONAL)
# define SPRITE_FUNDO
SPRITE_FUNDO = "atirar_vertical/sprites/fundo.png"
