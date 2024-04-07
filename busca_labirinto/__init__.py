from pyamaze import maze, agent
from random import randint, choice

class No():
    def __init__(self) -> None:
        self.coord: tuple = () #coordenada da célula no labirinto
        self.nos: list = [] #coordenada das células que são caminhos válidos a partir do nó atual

    def setCoord(self, coord:tuple) -> None:
        self.coord = coord

    def criaNos(self) -> None:
        #cria novos nós a partir das informações do mapa do labirinto em lab.maze_map
        info = MAPA[self.coord] #obtém informações de caminhos disponíveis

        coord = ()

        for key, value in info.items():
            if value==1:
                if key!='E':
                    if key!='W':
                        if key!='N':
                            coord = (self.coord[0]+1, self.coord[1]) #se vai para o sul
                        else: coord = (self.coord[0]-1, self.coord[1]) #se vai para o norte
                    else: coord = (self.coord[0], self.coord[1]-1) #se vai para o oeste
                else: coord = (self.coord[0]+1, self.coord[1]) #se vai para o leste

                novoNo = No() #cria o nó do próximo passo
                novoNo.setCoord(coord) #seta as coordenadas do novo nó a partir do mapa
                self.nos.append(novoNo) #adiciona o no como seguinte


def createMaze(size=10):

    #cria um labirinto quadrado de dimensões a partir do input
    lab = maze(eval(size),eval(size))

    #randomização do objetivo
    lista = ['linha', 'coluna']

    rand = choice(lista)

    if rand == 'linha':
        line = randint(1, eval(size))
        column = 1
    else:
        line = 1
        column = randint(1, eval(size))

    lab.CreateMaze(line, column,loopPercent=15)
    
    agente = agent(lab)
    
    lab.run()

    return lab, agente

a = input('Tamanho do labirinto: ')

lab, agente = createMaze(a)

MAPA = lab.maze_map #constante usada na criação de nós

#1 quando pode ir, 0 quando não pode ir
# testa criação dos nós
# no1 = No()
# no1.setCoord((5,5))
# no1.criaNos()
# [print(i.coord) for i in no1.nos]

# TODO1 : Implementar loop de verificação de cada nó usando a busca em largura
# TODO2: A solução deve conter as coordenadas de cada célula do caminho a ser percorrido
# TODO2: e deve ser comparada com a solução ótima proposta pelo próprio pyamaze
# TODO3: exibir o caminho percorrido no labirinto (mostrar o encontrado pelo código e
# TODO4: pelo pyamaze, caso sejam diferentes)
