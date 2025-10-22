# define TITULO (título que aparece na barra da janela)
TITULO = "COLETAR"
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
# define VERDE (cor verde)
VERDE = (0, 255, 0)

# JOGADOR
# define LARGURA_JOGADOR
LARGURA_JOGADOR = 150
# define ALTURA_JOGADOR
ALTURA_JOGADOR = 150
# define X_JOGADOR
X_JOGADOR = 50
# define Y_JOGADOR
Y_JOGADOR = ALTURA_TELA // 2 - ALTURA_JOGADOR // 2
# define VEL_JOGADOR
VEL_JOGADOR = 9

# ITENS E BOMBAS
# define LARGURA_ITEM
LARGURA_ITEM = 140
# define ALTURA_ITEM
ALTURA_ITEM = 140
# define VEL_ITEM
VEL_ITEM = 8
# define FREQ_ITEM
FREQ_ITEM = 25

# define VIDAS_INICIO
VIDAS_INICIO = 3

# define SPRITES
SPRITES = {
    "jogador": "coletar/sprites/jogador.png",
    "item": "coletar/sprites/item.png",
    "bomba": "coletar/sprites/bomba.png"
}

# FUNDO (OPCIONAL)
# define SPRITE_FUNDO
SPRITE_FUNDO = "coletar/sprites/fundo.png"
