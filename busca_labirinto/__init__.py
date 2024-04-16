from pyamaze import maze, agent
from random import randint, choice
import time

class No():
    def __init__(self) -> None:
        self.coord: tuple = () #coordenada da célula no labirinto
        self.nos: list = [] #coordenada das células que são caminhos válidos a partir do nó atual
        self.anterior: object = None #coordenada da célula visitada anteriormente no labirinto
        self.visitado: bool = False #se foi visitado ou nao

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

    lab.CreateMaze(line, column,
                   loopPercent=15,
                   )
    
    agente = agent(lab)

    return lab, agente, line, column

inicio = time.time()

size = input('Tamanho do labirinto: ')

lab, agente, line, column = createMaze(size)

MAPA = lab.maze_map #constante usada na criação de nós

initial_line = size
initial_column = size

initial_node = No()
initial_node.setCoord((initial_line, initial_column))
initial_node.criaNos()

# TODO1 : arrumar lógica da avaliação de cada nó
nodes = initial_node.nos

#* busca em profundidade
# while initial_column!=column and initial_line!=line: #verifica se não está na saída
    
#     for node in nodes:  #itera pelos nos mais profundos a cada passo
#         coord_line, coord_column = node.coord

#         if coord_line!=line and coord_column!=column: #verifica se não são as coordenadas da saída
#             node.criaNos()                             #cria os nós filhos para o próximo passo
#             for children in node.nos:
#                 children.setAnterior(node)

#         elif coord_line==line and coord_column==column:
#             initial_column = coord_column
#             initial_line = coord_line
    
#     new = []
#     for node in nodes:
#         for node in node.nos:
#             new.append(node)
#     nodes.clear()
#     nodes = new
#     [print(i.coord) for i in nodes]
#     break

#* busca em largura
i = 0 # controla a iteração de acesso aos nos
visitado = []
visitado.append(initial_node.coord)

def buscaLargura(node):
    if node.coord not in visitado:
        visitado.append(node.coord)
        coord_line, coord_column = node.coord
        # print(coord_line, coord_column)
        
        if coord_line!=line or coord_column!=column: #verifica se não são as coordenadas da saída
            print('Não é a saída')
            node.criaNos()               #cria os nós filhos para o próximo passo
            for children in node.nos:
                children.setAnterior(node)
        
            return node
        
        elif coord_line==line and coord_column==column:
            print('É a saída')
            visitados = []
            while node!=None:
                visitados.append(node.coord)
                node = node.anterior
            visitados.append((eval(size),eval(size)))
            
            return visitados
    else:
        return node
    
from joblib import Parallel, delayed

cont = 0
resultado = Parallel(n_jobs=2)(delayed(buscaLargura)(node) for node in nodes)

cont+=len(resultado) #controle de avaliações

controle = True
while controle:
    
    new = []
    for node in resultado:
        if type(node)!=list:
            for no in node.nos:
                new.append(no)

    nodes = new
    new = []

    resultado = Parallel(n_jobs=None)(delayed(buscaLargura)(node) for node in nodes)
    cont+=len(resultado)

    for r in resultado:
        if type(r)==list:
            resultado = r
            controle = False
    
print(resultado)
fim = time.time()
print(f'tempo de busca: {fim-inicio:.2f} s')
print(f'processos executados: {cont}')
# print(lab.path)
lab.run()



# TODO2: A solução deve conter as coordenadas de cada célula do caminho a ser percorrido
# TODO2: e deve ser comparada com a solução ótima proposta pelo próprio pyamaze
# TODO3: exibir o caminho percorrido no labirinto (mostrar o encontrado pelo código e
# TODO4: pelo pyamaze, caso sejam diferentes)
