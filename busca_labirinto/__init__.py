from pyamaze import maze, agent
from random import randint, choice

class No():
    def __init__(self) -> None:
        self.coord: tuple = () #coordenada da célula no labirinto
        self.nos: list = [] #coordenada das células que são caminhos válidos a partir do nó atual
        self.anterior: object = None #coordenada da célula visitada anteriormente no labirinto

    def setCoord(self, coord:tuple) -> None:
        
        x, y = coord
        x = int(x)
        y = int(y)

        self.coord = (x, y)
        

    def setAnterior(self, anterior:object) -> None:
        self.anterior = anterior

    def criaNos(self) -> None:
        #cria novos nós a partir das informações do mapa do labirinto em lab.maze_map
        info = MAPA[self.coord] #obtém informações de caminhos disponíveis

        coord = ()
        for key, value in info.items():
            if value==1:
                if key=='E': coord = (self.coord[0], self.coord[1]+1) #se vai para o leste
                elif key=='W': coord = (self.coord[0], self.coord[1]-1) #se vai para o oeste
                elif key=='N': coord = (self.coord[0]-1, self.coord[1]) #se vai para o norte
                elif key=='S': coord = (self.coord[0]+1, self.coord[1]) #se vai para o sul
                
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

    return lab, agente, line, column

size = input('Tamanho do labirinto: ')

lab, agente, line, column = createMaze(size)

MAPA = lab.maze_map #constante usada na criação de nós

visitados = []

initial_line = size
initial_column = size

initial_node = No()
initial_node.setCoord((initial_line, initial_column))
initial_node.criaNos()

# TODO1 : arrumar lógica da avaliação de cada nó

nodes = initial_node.nos
i = 0
while initial_column!=column and initial_line!=line: #verifica se não está na saída
    
    for node in nodes:  #itera pelos nos mais profundos a cada passo
        coord_line, coord_column = node.coord

        if coord_line!=line and coord_column!=column: #verifica se não são as coordenadas da saída
            node.criaNos()                             #cria os nós filhos para o próximo passo
            for children in node.nos:
                children.setAnterior(node)

        elif coord_line==line and coord_column==column:
            initial_column = coord_column
            initial_line = coord_line
    
    new = []
    for node in nodes:
        for node in node.nos:
            new.append(node)
    nodes.clear()
    nodes = new
    [print(i.coord) for i in nodes]
    break

lab.run()

print(coord_line, coord_column)
print(line, column)

# TODO2: A solução deve conter as coordenadas de cada célula do caminho a ser percorrido
# TODO2: e deve ser comparada com a solução ótima proposta pelo próprio pyamaze
# TODO3: exibir o caminho percorrido no labirinto (mostrar o encontrado pelo código e
# TODO4: pelo pyamaze, caso sejam diferentes)
