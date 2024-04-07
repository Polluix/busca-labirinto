from pyamaze import maze, agent
from random import randint, choice





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


    lab.CreateMaze(line, column,loopPercent=50)
    mapa = lab.maze_map
    agente = agent(lab)
    lab.run()

    return lab

a = input('Tamanho do labirinto: ')

lab = createMaze(a)
print(lab.maze_map) #1 quando pode ir, 0 quando não pode ir
