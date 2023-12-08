from copy import deepcopy
import sys

#converter lista para string
#facilita para representar o jogo
def convert_str(list):
    return [str(num) for num in list]

class Board:

    def __init__(self):
        self.list=[4,4,4,4,4,4,4,4,4,4,4,4]
        self.mancalas=[0,0]
        self.num_mov = 0

    def __str__(self):
        list_aux=convert_str(self.list)
        manc = convert_str(self.mancalas)
        text = """
    11 10 09 08 07 06
┌──┬──┬──┬──┬──┬──┬──┬──┐
│  │{}│{}│{}│{}│{}│{}│  │
│{}│──┼──┼──┼──┼──┼──│{}│
│  │{}│{}│{}│{}│{}│{}│  │
└──┴──┴──┴──┴──┴──┴──┴──┘
    00 01 02 03 04 05
""" \
            .format(list_aux[11].rjust(2, '0'), list_aux[10].rjust(2, '0'), list_aux[9].rjust(2, '0'),
                    list_aux[8].rjust(2, '0'),list_aux[7].rjust(2, '0'), list_aux[6].rjust(2, '0'),
                    manc[1].rjust(2, '0') ,manc[0].rjust(2, '0'),
                    list_aux[0].rjust(2, '0'),list_aux[1].rjust(2, '0'),list_aux[2].rjust(2, '0'),
                    list_aux[3].rjust(2, '0'), list_aux[4].rjust(2, '0'),list_aux[5].rjust(2, '0'))
        return text

    #Diz se o jogo já acabou
    def fim_jogo(self):
        if self.mancalas[0] + self.mancalas[1] == 48:
            if self.mancalas[0]>self.mancalas[1]:
                return 1    #ganhou jogador 1
            if self.mancalas[0]<self.mancalas[1]:
                return 2    #ganhou jogador 2
            if self.mancalas[0]==self.mancalas[1]:
                return 0    #empate
        return -1 #ainda não acabou

    #faz os movimentos de uma jogada
    def move(self, jog, pos):
        pecas = self.list[pos]
        self.list[pos] = 0
        while pecas > 0:
            pos += 1
            if (pos==6 and jog==1) or (pos==12 and jog==2):
                self.mancalas[jog-1]+=1
                pecas -= 1
                if pecas == 0:
                    self.num_mov += 1
                    if self.jogada_impossivel(jog) == False:
                        return jog
                    else:
                        return self.troca_jog(jog)
            if pos==12:
                pos = 0
            self.list[pos]+=1
            pecas-=1
            if pecas == 0 and self.list[pos] == 1 and ((pos<6 and jog==1) or (pos>5 and jog==2)):
                if (self.list[self.oposto_pos(pos)]>0):
                    soma = self.list[pos] + self.list[self.oposto_pos(pos)]
                    self.mancalas[jog-1]+=soma
                    self.list[pos] = 0
                    self.list[self.oposto_pos(pos)] = 0
                    if self.jogada_impossivel(jog) == False:
                        self.num_mov += 1
                        return jog
        if self.jogada_impossivel(self.troca_jog(jog)):
            self.num_mov += 1
            return jog
        self.num_mov += 1
        return self.troca_jog(jog)

    #troca de jogador
    def troca_jog(self, jog):
        if jog == 1:
            return 2
        return 1

    #retorna a casa oposta
    def oposto_pos(self, pos):
        if pos == 0:
            return 11
        if pos == 1:
            return 10
        if pos == 2:
            return 9
        if pos == 3:
            return 8
        if pos == 4:
            return 7
        if pos == 5:
            return 6
        if pos == 6:
            return 5
        if pos == 7:
            return 4
        if pos == 8:
            return 3
        if pos == 9:
            return 2
        if pos == 10:
            return 1
        if pos == 11:
            return 0

    #Retorna True se o jog não puder fazer jogadas (todas as suas casas sem peças)
    def jogada_impossivel(self, jog):
        zeros = 0
        if jog == 1:
            for i in range (6):
                if self.list[i] == 0:
                    zeros +=1
            if zeros == 6:
                return True
        zeros = 0
        if jog == 2:
            for i in range (6,12):
                if self.list[i] == 0:
                    zeros +=1
            if zeros == 6:
                return True
        return False

    #função utilidade
    def utilidade(self, jog):
        mancala_atual = self.mancalas[jog-1]
        if jog==1:
            outro_jog = 2
            mancala_oponente = self.mancalas[1]
        elif jog==2:
            outro_jog = 1
            mancala_oponente = self.mancalas[0]
        if self.fim_jogo() != -1:
            pontuacao = mancala_atual - mancala_oponente
            if self.fim_jogo() == jog:
                return 100 + pontuacao
            elif self.fim_jogo() == outro_jog:
                return -100 - pontuacao
            else:
                return 0
        else:
            return mancala_atual - mancala_oponente

    #retorna uma lista com as jogadas possiveis do jogador
    def movimentos_possiveis(self,jog):
        list=[]
        moves1=[]
        moves2=[]
        if jog==1:
            for i in range (6):
                if self.list[i] != 0:
                    list.append(i)
        elif jog==2:
            for i in range (6,12):
                if self.list[i] != 0:
                    list.append(i)
        return list
