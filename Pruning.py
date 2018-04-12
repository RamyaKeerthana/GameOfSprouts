class Pruning:
    def __init__(self, game_tree):
        self.game_tree = game_tree  
        self.root = game_tree.root  
        return

    def alpha_beta_search(self, node):
        infinity = float('inf')
        best_val = -infinity
        beta = infinity

        successors_moves = self.getSuccessorsMoves(node)
        best_move = None
        for move in successors_moves:
            value = self.min_value(move, best_val, beta)
            if value > best_val:
                best_val = value
                best_move = move
        print "AlphaBeta:  Utility Value of Root Node: = " + str(best_val)
        print "AlphaBeta:  Best Move is: " + best_move.Name
        return best_move

    def max_value(self, node, alpha, beta):
        print "AlphaBeta-->MAX: Visited Node :: " + node.Name
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = -infinity

        successors_moves = self.getSuccessorsMoves(node)
        for move in successors_moves:
            value = max(value, self.min_value(move, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        print "AlphaBeta-->MIN: Visited Node :: " + node.Name
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = infinity

        successors_moves = self.getSuccessorsMoves(node)
        for move in successors_moves:
            value = min(value, self.max_value(move, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value

    def getSuccessors_moves(self, node):

    def isTerminal(self, node):

    def getUtility(self, node):


return node.value