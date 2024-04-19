# Algoritmos de busca em largura e profundidade para um labirinto - Sitemas Inteligentes (EMB5617)
![GitHub License](https://img.shields.io/github/license/Polluix/busca-labirinto)

## Como executar o script
- instalar o Python 3.11
- criar o ambiente virtual na pasta raiz do projeto utilizando o comando:

  `python venv .venv`

- ativar o ambiente virtual acessando o script de ativação utilizando o comando:

  `.venv/Scripts/activate`

- fazer a instalação das dependências a partir do arquivo requirements.txt utilizando o comando pip:

  `pip install -r requirements.txt`

- acessar a pasta do script principal

  `cd busca-labirinto`

- executar o script

  `python __init__.py

- as demais instruções serão impressas no terminal, nas quais o usuário pode escolher o tamanho do labirinto (mínimo 2) digitando um inteiro que represente o numero de células de cada lado (labirinto quadrado):

![escolha labirinto](https://github.com/Polluix/busca-labirinto/blob/main/assets/tamanho-labirinto.png)

e quais métodos de busca deseja executar

![quais metodos](https://github.com/Polluix/busca-labirinto/blob/main/assets/qual-metodo.png)

## Resultados
Os resultados de cada método de busca serão impressos no terminal, com métricas para avaliação do desempenho de cada método executado, incluindo tempo de execução, quantidade de nós avaliados e quantidade de nós percorridos diretamente até a saída.

![metricas-resultados](https://github.com/Polluix/busca-labirinto/blob/main/assets/resultado-busca-metricas.png)

## Visualização do resultado
O resultado será mostrado na janela do Python que será aberta logo após a execução de cada método. A cor dos agentes define qual método foi utilizado e será especificada junto às métricas de resultado apresentadas no terminal.

![visualização](https://github.com/Polluix/busca-labirinto/blob/main/assets/exemplo-solucao.png)

## Observações relevantes
 - A busca em largura foi implementada utilizando-se orientação a objetos, o que gerou uma carga bem grande para o computador durante a execução, chegando a utilizar 13 gb de memória RAM em labirintos grandes (maiores que 10x10). Por conta disso, a implementação foi otimizada, excluindo nós que já foram avaliados anteriormente e utilizando paralelismo de processos do módulo ![joblib](https://joblib.readthedocs.io/en/stable/) do Python, tornando o método menos custoso computacionalmente.
 - Visando evitar o custo elevado do método de busca em largura encontrado na implementação orientada a objetos, a busca em profundidade foi implementada a partir da manipulação de listas e variáveis auxiliares de controle de iteração, economizando memória



