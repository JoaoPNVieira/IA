
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod # -------------------------------------> CLasse: Abstract Base Classes - Criar classes abstractas 

###########################################################################################################################################
#### CLASSE DOMINIOS DE PESQUISA ##########################################################################################################
# -------------------------------> Calcular ações possíveis em cada estado etc...
#################################################################################

class SearchDomain(ABC): #-------------------------------------------------> CLASSE: Formata a estrutura de um domı́nio

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


###########################################################################################################################################
#### CLASSES SEARCH #######################################################################################################################
# ------------------> Problemas concretos a resolver dentro de um determinado dominio
######################################################################################



class SearchProblem: # ----------------------------------------------------> CLASSE: para especificar problemas de pesquisa:
    def __init__(self, domain, initial, goal): # ----------------------------------> CONSTRUTOR: Argumentos de iniciação
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state): # -----------------------------------------> Método: Testar se o estado atual é o Objectivo(Goal).
        return self.domain.satisfies(state,self.goal)




class SearchNode: # -------------------------------------------------------> CLASSE: dos Nós da árvore de pesquisa
    def __init__(self,state,parent,depth,cost): # --------------------------------------> CONSTRUTOR: Argumentos de iniciação
        self.state = state
        self.parent = parent


#__________________________________________________________________________
    #Solution of II.2.) Problema: Na estrutura de dados usada para representar os nós no módulo de pesquisa, acrescentar atributo para registar a 
    #                   profundidade do nó. Considera-se que a raiz da árvore de pesquisa está na profundidade 0.
    
        self.depth = depth # II.2)

#__________________________________________________________________________
    #Solution of II.8.) Problema: Na estrutura de dados para representar nós acrescente um atributo para o custo acumulado raiz-nó. Registar custo acumulado em cada nó.
        self.cost = cost


    def __str__(self): # ---------------------------------------------------> Método: retorna string do objecto (formato "humano"). Faz output de todos os membros da Classe.
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    
    
    def __repr__(self): # --------------------------------------------------> Método: retorna string do objecto (formato coding).
        return str(self)

    def in_parent(self, newstate): # ---------------------------------------> II.2) Método: Verifica se o novo estado atual é filho de um node pai
        if self.parent == None: # --------------------------------------------------> Se o estado atual não tem pai,
            return False # ---------------------------------------------------------> então retorna FALSE.
        if self.parent.state == newstate: #-----------------------------------------> Se o estado atual tem pai e o seu pai é o novo estado,
            return True # ----------------------------------------------------------> então retorna TRUE.
        return self.parent.in_parent(newstate) # ---------------------------> END II.2) RETORNA: o novo estado 

#__________________________________________________________________________
#
#
#
#
#
###########################################################################################################################################
#### ARVORES DE PESQUISA ##################################################################################################################
# -----------------------> Métodos para gerar árvore de pesquisa para um problema
######################################################################################

class SearchTree: # -------------------------------------------------------> CLASSE: gera árvore de pesquisa para um problema


    def __init__(self,problem, strategy='breadth'):  # ----------------------------> CONSTRUTOR: Argumentos de iniciação
        self.problem = problem # ------------------------------------------> PROBLEMA
        
        root = SearchNode(problem.initial, None, 0)  # --------------------> ROOT: 1º Node de todos ( problem.initial = state inicial | None = Parent | breadth = 0 )
        
        self.open_nodes = [root] # ----------------------------------------> FILA DE NODES A EXPANDIR: Neste caso a partir de root anterior
        
        self.strategy = strategy # ----------------------------------------> ESTRATÉGIA 
        self.solution = None # --------------------------------------------> SOLUÇÃO
        self.terminals = 0 # ----------------------------------------------> Nós terminais
        self.non_terminals = 0 # ------------------------------------------> Nós não terminais
#__________________________________________________________________________
    #Solution II.3.) Problema: desenvolver property length para devolver comprimento da solução encontrada
    @property
    def length(self):
        return self.solution.depth
#__________________________________________________________________________
#
#
#
#__________________________________________________________________________
    #Solution II.6.) Problema: desenvolver property avg_branching para retornar o factor de ramificação média 
    @property 
    def avg_branching(self):
        return((self.terminals-1) + self.non_terminals) / self.non_terminals
#__________________________________________________________________________


    def get_path(self,node): # --------------------------------------------> Método: Obter o caminho de state até um node
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)



#__________________________________________________________________________           
    #Solution II.4.) Problema: pesquisa em profundidade deve suportar limite máximo (evitar custo elevado)
    #Solution II.5.) Problema: Acrescentar ao search() código para calcular o nº total de nós terminais (folhas) e não terminais 
    #                          (nós já expandidos, mesmo que sem filhos). Usar self para armazenar valores.
    
    def search(self, limit=12): # -----------------------------------------> Procurar a solução. II.4) Impôr limite de 12
        while self.open_nodes != []: # ------------------------------------> Enquanto o vector (lista) de Nodes tiver elementos:
            node = self.open_nodes.pop(0) # -------------------------------> retirar (pop) elemento de idx 0
            self.terminals = len(self.open_nodes) + 1 # -------------------> II.5) terminals = comprimento dos nós abertos + 1 (root)

            if self.problem.goal_test(node.state) and node.depth <= limit: # --> II.4) Impôr limite no loop
                self.solution = node
                return self.get_path(node)
            
            self.non_terminals += 1 # ------------------------------------------> II.5.) Nós não terminais (+1 contagem)

            lnewnodes = [] # ---------------------------------------------------> Vector (lista) de novos Nodes 
            
            if node.depth<limit: # ---------------------------------------------> II.5.) Impôr limite na contagem
                for a in self.problem.domain.actions(node.state): # ------------> Para uma acção A das ações possíveis para o problema
                    newstate = self.problem.domain.result(node.state,a) # ------> Novo State = resultado da ação A anterior
#__________________________________________________________________________           
    #Solution II.1.) Problema: desperdicio de memória em breath e ciclos infinitos em depth

                    if newstate not in self.get_path(node): # ------------------> Se o Novo State não estire no caminho do Node
                        newnode = SearchNode(newstate,node,node.depth+1) #------> Novo Node = ( novo estado, node(parent), depth+1 (para ir para a proxima layer))
                        lnewnodes.append(newnode) # ----------------------------> Vector de novos Nodes vai receber novo node
                self.add_to_open(lnewnodes) # ----------------------------------> Call da função a baixo
        return None
#__________________________________________________________________________

    def add_to_open(self,lnewnodes): # -------------------------------------> Juntar novos nodes à lista de nodes abertos (de acordo com estratégia)
        if self.strategy == 'breadth': # -----------------------------------> Se ESTRATÉGIA é Largura
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth': # -----------------------------------> Se ESTRATÉGIA é Prefundidade
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform': # ---------------------------------> Se Estratégia é Uniforme
            pass