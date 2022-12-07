class GraphTree:
    """
    Plot Binomial Tree.
     
    """
    def __init__(self, data_tree, up_color = "cornflowerblue",
                 down_color = "salmon", text_color = "black"):
        
        self.data_tree = data_tree #
        self.up_color = up_color
        self.down_color = down_color
        self.text_color = text_color
        
    
    def real_tree(self):
        """
        Real Tree ==> Price proportional to distance
        """

        fig, ax = plt.subplots(figsize=(16, 8))
        tree = self.data_tree
        n = len(tree)
        for i in range(len(tree)-1):
            for j in range(len(tree)-1):
                if j >i:
                    next
                    
                else:
                    plt.plot([i,i+1], [tree[j,i],tree[j+1,i+1]],
                             color= self.down_color)

                    plt.plot([i,i+1], [tree[j,i],tree[j,i+1]],
                             color = self.up_color)

                    plt.text(i-0.15, tree[j][i], s = str(round(tree[j,i],4)),
                             color = self.text_color, zorder=10)

        for j in range(len(tree)-1):
            plt.text(n-1.15, tree[j-1][-1], s = str(round(tree[j-1,-1],4)),
                     color = self.text_color)

    def fake_tree(self):
        """
        Method that plot "Aesthetic tree". 
        Aesthetic <==> up move = down move
        In other word, price position is not proportional to the actual price. 
        """       

        fig, ax = plt.subplots(figsize=(16, 8))
        n = len(self.data_tree)
        
        tree_f = np.zeros((n+1,n+1))
        tree_f[0,0] = 100
        for i in range(n):
            tree_f[0,i+1] = tree_f[0,i] +10

            for j in range(n):
                if j >i:
                    next
                else:
                    tree_f[j+1,i+1] = tree_f[j,i] -10
        
        for i in range(n):
            for j in range(n):
                if j >i:
                    next
                else:

                    plt.plot([i, i+1], [tree_f[j, i],tree_f[j+1, i+1]],
                             color= self.down_color,zorder=2)

                    plt.plot([i, i+1], [tree_f[j, i],tree_f[j, i+1]],
                             color = self.up_color,zorder=1)

                    plt.text(i-0.15, tree_f[j, i], s = str(round(tree_f[j, i], 4)),
                             color = self.text_color, zorder=10)

        for j in range(n+1):
            plt.text(n-0.15, tree_f[j-1, -1], s = str(round(tree_f[j-1,-1],4)),
                     color = self.text_color)