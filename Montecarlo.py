from Board import *
from copy import deepcopy
import random
import math
import time
import sys

class Node:
    def __init__(self, move, pai):
        self.move = move
        self.pai = pai
        self.N = 0   #simulações
        self.Q = 0   #quantidade de vitorias
        self.filhos = {}

    #adiciona os filhos ao respetivo pai
    def adiciona_filhos(self, filhos):
        for filho in filhos:
            self.filhos[filho.move] = filho

    #função Upper Confidence Bound (UCB)
    def UCB(self):
        if self.N == 0:
            return 0 if math.sqrt(2) == 0 else float('inf')
        return self.Q / self.N + math.sqrt(2) * math.sqrt(math.log(self.pai.N) / self.N)

class MCTS:
    def __init__(self, mancala, jog):
        self.estado_raiz = deepcopy(mancala)
        self.raiz = Node(None, None)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0
        self.jog = jog

    #função seleção
    def selection(self):
        node = self.raiz
        mancala = deepcopy(self.estado_raiz)

        while len(node.filhos) != 0:
            filhos = node.filhos.values()
            maior_ucb = max(filhos, key=lambda n: n.UCB()).UCB()
            max_nodes = [n for n in filhos if n.UCB() == maior_ucb]
            node = random.choice(max_nodes)
            posicao = node.move
            mancala.move(self.jog, posicao)

            if node.N == 0:
                return node, mancala

        if self.expand(node, mancala):
            node = random.choice(list(node.filhos.values()))
            mancala.move(self.jog, node.move)
        return node, mancala

    #função expansão
    def expand(self, pai: Node, mancala) -> bool:
        if mancala.fim_jogo() != -1 or mancala.jogada_impossivel(self.jog):
            return False

        filhos = [Node(move, pai) for move in mancala.movimentos_possiveis(self.jog)]
        pai.adiciona_filhos(filhos)
        return True

    #função simulação
    def simulation(self, mancala):
        while mancala.fim_jogo() == -1 and mancala.jogada_impossivel(self.jog) == False:
            jogadas_possiveis = mancala.movimentos_possiveis(self.jog)
            posicao = random.choice(jogadas_possiveis)
            mancala.move(self.jog, posicao)
        return mancala.fim_jogo()

    #função retropropagação
    def back_propagate(self, node, vencedor):
        recompensa = 0 if vencedor == self.jog else 1
        while node is not None:
            node.N += 1
            node.Q += recompensa
            node = node.pai
            if vencedor == 0: #empate
                recompensa = 0
            else:
                recompensa = 1 - recompensa

    #faz a pesquisa utilizando os 4 passos, com um período de tempo limitado
    def search(self, time_limit):
        start_time = time.process_time()
        num_rollouts = 0
        while time.process_time() - start_time < time_limit:
            node, mancala = self.selection()
            vencedor = self.simulation(mancala)
            self.back_propagate(node, vencedor)
            num_rollouts += 1

        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.num_rollouts = num_rollouts

    #melhor movimento
    def best_move(self):
        if self.estado_raiz.fim_jogo() != -1:
            return -1

        maior_ucb = max(self.raiz.filhos.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.raiz.filhos.values() if n.N == maior_ucb]
        melhor_filho = random.choice(max_nodes)

        return melhor_filho.move
