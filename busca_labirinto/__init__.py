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
    
    agente = agent(lab,footprints=True)

    return lab, agente, line, column

size = input('Tamanho do labirinto: ')
print('-------------------------------------------------------')
print('Criando labirinto...')

lab, agente, line, column = createMaze(size)

MAPA = lab.maze_map #constante usada na criação de nós

initial_line = size
initial_column = size

print('-------------------------------------------------------')

initial_node = No()
initial_node.setCoord((initial_line, initial_column))
initial_node.criaNos()

nodes_largura = initial_node.nos
nodes_profundidade = initial_node.coord

opcoes = eval(input('Deseja executar qual método de busca?\n1: Busca em largura\n2: Busca em profundidade\n3: Ambas\nResposta: '))
print('-------------------------------------------------------')

def testeObjetivo(node, coord_line, coord_column):
    
    if coord_line!=line or coord_column!=column: #verifica se não são as coordenadas da saída
        node.visitado = True
        node.criaNos()               #cria os nós filhos para o próximo passo
        for children in node.nos:
            children.setAnterior(node)
    
        return node
    
    elif coord_line==line and coord_column==column:
        print('Encontrou a saída!')
        visitados = []
        while node!=None:
            visitados.append(node.coord)
            node = node.anterior
        visitados.append((eval(size),eval(size)))
        
        return visitados

def testSaida(no):
    return True if no==(line, column) else False

def sucessorProfundidade(visitados, controle):
    caminho = {}
    i = 0
    while len(controle)>0:
        no = controle.pop()
        i+=1
        if testSaida(no)==True:
            print('É a saída!')
            break
        for direcao in 'ESNW':
            if lab.maze_map[no][direcao]==True:
                if direcao=='E': proximo = (no[0], no[1]+1) #se vai para o leste
                elif direcao=='W': proximo = (no[0], no[1]-1) #se vai para o oeste
                elif direcao=='N': proximo = (no[0]-1, no[1]) #se vai para o norte
                elif direcao=='S': proximo = (no[0]+1, no[1]) #se vai para o sul
                if proximo in visitados: continue
                visitados.append(proximo)
                controle.append(proximo)
                caminho[proximo] = no
    return caminho, i

def buscaProfundidade(node):
    
    visitados = [node]
    controle = [node]
    
    caminho, custo_total = sucessorProfundidade(visitados, controle)
    new_caminho={}
    cell=(line,column)
    while cell !=node:
        new_caminho[caminho[cell]]=cell
        cell=caminho[cell]
    return new_caminho, custo_total

    
def executa_busca_profundidade(node):
    print('Executando busca em profundidade...')
    inicio = time.time()

    resultado, custo_total = buscaProfundidade(node)

    fim = time.time()
    filename = 'resultado_busca_em_profundidade.txt'

    with open(filename, mode='w') as file:
        file.write(str(resultado))
        file.close()

    print(f'Verifique a solução no arquivo: {filename}')
    print(f'Tempo de busca: {fim-inicio:.2f} s')
    print(f'Quantidade de nós percorridos até a saída (custo da solução): {len(resultado)}')
    print(f'Quantidade de nós avaliados (custo total): {custo_total}')
    if opcoes==2:
        print('A solução será mostrada no labirinto. O caminho em azul foi encontrado pela busca, o caminho em amarelo pelo próprio módulo que cria o labirinto.')
    print('-------------------------------------------------------')

    return resultado

visitado = []
visitado.append(initial_node.coord)

def buscaLargura(node):
    if node.coord not in visitado:
        visitado.append(node.coord)
        coord_line, coord_column = node.coord

        resultado_teste = testeObjetivo(node, coord_line,coord_column)    

        return resultado_teste
    
    else:
        return node
    
from joblib import Parallel, delayed

def sucessorLargura(controle, resultado, cont):
        new = []
        for node in resultado:
            if type(node)!=list:
                for no in node.nos:
                    new.append(no)

        nodes = new
        new = []

        resultado = Parallel(n_jobs=2, prefer='threads')(delayed(buscaLargura)(node) for node in nodes)
        cont = custoTotal(cont, len(resultado)) #função custo

        for r in resultado:
            if type(r)==list:
                resultado = r
                controle = False

        return controle, resultado, cont

def custoTotal(cont,valor):
    cont += valor
    return cont

def executa_busca_largura(nodes):
    print('Executando busca em largura...')
    inicio = time.time()
    cont = 0 #utilizado para computar o custo (quantidade de nós avaliados)

    resultado = Parallel(n_jobs=2)(delayed(buscaLargura)(node) for node in nodes) #primeiro passo de execução da busca
    cont = custoTotal(cont, len(resultado)) #função custo
    controle = True
    while controle:
        controle, resultado, cont = sucessorLargura(controle, resultado, cont)

    fim = time.time()
    filename = 'resultado_busca_em_largura.txt'

    dictL = {}
    i = len(resultado)
    for i in range(len(resultado)-1,0,-1):
        dictL[resultado[i]]=resultado[i-1]
        i-=1

    with open(filename, mode='w') as file:
        file.write(str(resultado))
        file.close()

    print(f'Verifique a solução no arquivo: {filename}')
    print(f'Tempo de busca: {fim-inicio:.2f} s')
    print(f'Quantidade de nós avaliados (custo total): {cont}')
    print(f'Quantidade de nós percorridos até a saída (custo da solução): {len(resultado)}')
    if opcoes==1:
        print('A solução será mostrada no labirinto. O caminho em azul foi encontrado pela busca, o caminho em amarelo pelo próprio módulo que cria o labirinto.')
    print('-------------------------------------------------------')

    return dictL

if opcoes==1:
    solucao_largura = executa_busca_largura(nodes_largura)

    agente2 = agent(lab,footprints=True, color='yellow')

    lab.tracePath({agente:solucao_largura})
    lab.tracePath({agente2:lab.path})

    lab.run()
elif opcoes==2:
    solucao_profundidade = executa_busca_profundidade(nodes_profundidade)
    agente2 = agent(lab,footprints=True, color='yellow')

    lab.tracePath({agente:solucao_profundidade})
    lab.tracePath({agente2:lab.path})

    lab.run()
elif opcoes==3:

    solucao_largura = executa_busca_largura(nodes_largura)

    agente2 = agent(lab,footprints=True, color='yellow')

    solucao_profundidade = executa_busca_profundidade(nodes_profundidade)

    agente3 = agent(lab,footprints=True, color='red')

    print('''A solução será mostrada no labirinto. O primeiro caminho é da busca em largura (azul), o segundo da busca em profundidade(amarelo)
          e o terceiro o resultado dado pelo próprio módulo do labirinto (vermelho)''')

    lab.tracePath({agente:solucao_largura})
    lab.tracePath({agente2:solucao_profundidade})
    lab.tracePath({agente3:lab.path})
    lab.run()
