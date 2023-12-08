from Board import *
from Montecarlo import *
import sys

#retorna a melhor jogada possível com minimax com cortes alfa-beta
def minimax(jog, mancala, dificuldade):
    alfa = float("-inf")
    beta = float("inf")
    _ , move = maximo(jog, mancala, dificuldade, alfa, beta, move=None)
    return move

#função maximo para o minimax
def maximo(jog, mancala, dificuldade, alfa, beta, move):
    if mancala.fim_jogo()!=-1 or dificuldade==0 or len(mancala.movimentos_possiveis(jog))==0:
        mancala_cp = deepcopy(mancala)
        mancala_cp.move(jog,move)
        return mancala_cp.utilidade(jog),move

    max_value = float("-inf")
    for s in mancala.movimentos_possiveis(jog):
        mancala_cp = deepcopy(mancala)
        mancala_cp.move(jog,s)
        value, _ = minimo(jog, mancala_cp, dificuldade - 1, alfa, beta, s)
        if  value>max_value:
            max_value=value
            move=s
        alfa = max(alfa, max_value)
        if alfa >= beta:
            break

    return max_value,move

#função minimo para o minimax
def minimo(jog, mancala, dificuldade, alfa, beta, move):
    if mancala.fim_jogo()!=-1 or dificuldade==0 or len(mancala.movimentos_possiveis(jog))==0:
        mancala_cp = deepcopy(mancala)
        mancala_cp.move(jog,move)
        return mancala_cp.utilidade(jog),move

    min_value = float("inf")
    for s in mancala.movimentos_possiveis(jog):
        mancala_cp = deepcopy(mancala)
        mancala_cp.move(jog,s)
        value, _ = maximo(jog, mancala_cp, dificuldade - 1, alfa, beta, s)
        if value<min_value:
            min_value=value
            move = s
        beta = min(beta, min_value)
        if beta <= alfa:
            break

    return min_value,move

#retorna a melhor jogada possível com montecarlo
def montecarlo(jog, mancala, dificuldade):
    mcts = MCTS(mancala, jog)
    mcts.search(dificuldade)
    best_move = mcts.best_move()
    return best_move


#jogada Humano vs Humano
def hum_hum(mancala):
    jog = 1
    while mancala.fim_jogo() == -1:
        print(mancala)
        if (mancala.jogada_impossivel(jog)):
            jog = mancala.troca_jog(jog)
        print('Jogador %d:'%jog)
        prox_jog = jog
        while prox_jog == jog and mancala.jogada_impossivel(jog)==False:
            print('Escolha a posição em que quer jogar:')
            pos = int(input())
            while pos>11 or pos<0:
                print('Posição Inválida. Insira outra posição.')
                pos = int(input())
            while pos>5 and jog == 1:
                print('Não é possível jogar na posição do adversário. Insira outra posição.')
                pos = int(input())
            while pos<6 and jog == 2:
                print('Não é possível jogar na posição do adversário. Insira outra posição.')
                pos = int(input())
            while mancala.list[pos] == 0:
                print('Não é possível jogar numa posição com 0 peças. Insira outra posição.')
                pos = int(input())
            prox_jog = mancala.move(jog, pos)
            if prox_jog == jog and mancala.jogada_impossivel(jog)==False:
                print(mancala)
                print('É o jogador %d a jogar outra vez.' %jog)
        jog = prox_jog
    print('O jogo acabou.')
    if (mancala.fim_jogo() == 0):
        print('Empate.')
    else:
        print('O vencedor foi o jogador %d.' %mancala.fim_jogo())
    print('Número total de jogadas: %d' %mancala.num_mov)
    sys.exit()

#Jogada Humano vs Computador
def hum_comp(mancala, estrategia, dificuldade):
    jog = 1
    print(mancala)
    while mancala.fim_jogo() == -1:
        print('Jogador %d:'%jog)
        prox_jog = jog
        while prox_jog == 1 and mancala.jogada_impossivel(jog)==False:
            print('Escolha a posição em que quer jogar:')
            pos = int(input())
            while pos>11 or pos<0:
                print('Posição Inválida. Insira outra posição.')
                pos = int(input())
            while (pos>5 and jog == 1) or (pos<6 and jog == 2):
                print('Não é possível jogar na posição do adversário. Insira outra posição.')
                pos = int(input())
            while mancala.list[pos] == 0:
                print('Não é possível jogar numa posição com 0 peças. Insira outra posição.')
                pos = int(input())
            prox_jog = mancala.move(jog, pos)
            print(mancala)
            if prox_jog == jog and mancala.jogada_impossivel(jog)==False:
                print('É o jogador %d a jogar outra vez.' %jog)
        jog = prox_jog
        print('Jogador %d:'%jog)

        while prox_jog == 2 and mancala.jogada_impossivel(jog)==False:
            if estrategia == 1:
                melhor_jogada = minimax(jog, mancala, dificuldade)
            if estrategia == 2:
                melhor_jogada = montecarlo(jog, mancala, dificuldade)
            print('Posição escolhida: %d' %melhor_jogada)
            prox_jog = mancala.move(jog, melhor_jogada)
            print(mancala)
            if prox_jog == jog and mancala.jogada_impossivel(jog)==False:
                print('É o jogador %d a jogar outra vez.' %jog)
        jog = prox_jog
    print('O jogo acabou.')
    if (mancala.fim_jogo() == 0):
        print('Empate.')
    else:
        print('O vencedor foi o jogador %d.' %mancala.fim_jogo())
    print('Número total de jogadas: %d' %mancala.num_mov)
    sys.exit()

#Jogada Computador vs Computador
def comp_comp(mancala, estrategia1, estrategia2, dificuldade):
    jog = 1
    print(mancala)
    while mancala.fim_jogo() == -1:
        print('Jogador %d:'%jog)
        prox_jog = jog
        while prox_jog == 1 and mancala.jogada_impossivel(jog)==False:
            if estrategia1 == 1:
                melhor_jogada = minimax(jog, mancala, dificuldade)
            if estrategia1 == 2:
                melhor_jogada = montecarlo(jog, mancala, dificuldade)
            print('Posição escolhida: %d' %melhor_jogada)
            prox_jog = mancala.move(jog, melhor_jogada)
            print(mancala)
            if prox_jog == jog and mancala.jogada_impossivel(jog)==False:
                print('É o jogador %d a jogar outra vez.' %jog)
        jog = prox_jog
        print('Jogador %d:'%jog)
        while prox_jog == 2 and mancala.jogada_impossivel(jog)==False:
            if estrategia2 == 1:
                melhor_jogada = minimax(jog, mancala, dificuldade)
            if estrategia2 == 2:
                melhor_jogada = montecarlo(jog, mancala, dificuldade)
            print('Posição escolhida: %d' %melhor_jogada)
            prox_jog = mancala.move(jog, melhor_jogada)
            print(mancala)
            if prox_jog == jog and mancala.jogada_impossivel(jog)==False:
                print('É o jogador %d a jogar outra vez.' %jog)
        jog = prox_jog
    print('O jogo acabou.')
    if (mancala.fim_jogo() == 0):
        print('Empate.')
    else:
        print('O vencedor foi o jogador %d.' %mancala.fim_jogo())
    print('Número total de jogadas: %d' %mancala.num_mov)
    sys.exit()


def main():
    print('Jogo Mancala')
    mancala = Board()
    print('Escolha o modo de jogo (insira o número correspondente):')
    print('1: Humano vs Humano; 2: Humano vs Computador; 3: Computador vs Computador')
    modo_jog = int(input())
    if modo_jog == 1:
        hum_hum(mancala)
    if modo_jog == 2:
        print('Escolha a estratégia para o computador (insira o número correspondente):')
        print('1: Minimax com cortes Alfa-Beta; 2: Monte Carlo')
        estrategia = int(input())
        print('Escolha a dificuldade (insira o número correspondente):')
        print('1: Fácil; 2: Médio; 3: Difícil')
        dificuldade = int(input())
        hum_comp(mancala, estrategia, dificuldade)
    if modo_jog == 3:
        print('Escolha a estratégia para o computador 1 (insira o número correspondente):')
        print('1: Minimax com cortes Alfa-Beta; 2: Monte Carlo')
        estrategia1 = int(input())
        print('Escolha a estratégia para o computador 2 (insira o número correspondente):')
        print('1: Minimax com cortes Alfa-Beta; 2: Monte Carlo')
        estrategia2 = int(input())
        print('Escolha a dificuldade (insira o número correspondente):')
        print('1: Fácil; 2: Médio; 3: Difícil')
        dificuldade = int(input())
        comp_comp(mancala, estrategia1, estrategia2, dificuldade)

if __name__ == '__main__':
    main()
