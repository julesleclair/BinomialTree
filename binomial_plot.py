import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class GraphTree:
    """
    Plot Binomial Tree.
    
    data_tree: nxn numpy array or DataFrame

    up_color(optional): str color of an up move 
    down_color(optional): str color of an down move
    text_color (optional): str color of text
    """
    def __init__(self, data_tree, up_color = "salmon",
                 down_color = "cornflowerblue", text_color = "black",
                 fig_size = (16,8)):

        self.data_tree = data_tree #
        self.up_color = up_color
        self.down_color = down_color
        self.text_color = text_color
        self.fig_size = fig_size # tuple
        
    
    def real_tree(self):
        """
        Real Tree ==> Price proportional to distance
        """

        plt.subplots(figsize=self.fig_size) # useful for outpub in jupyternotebook
        tree = self.data_tree
        n = len(tree)
        
        
        #TODO: Vectorise plot?
        for i in range(n-1):
            for j in range(n-1):
                if j <= i:

                    plt.plot([i,i+1], [tree[j,i],tree[j+1,i+1]],
                             color= self.down_color)

                    plt.plot([i,i+1], [tree[j,i],tree[j,i+1]],
                             color = self.up_color)

                    plt.text(i-0.15, tree[j, i], s = str(round(tree[j, i],4)),
                             color = self.text_color, zorder=10)

        for j in range(n):

            plt.text(n-1.15, tree[j,-1], s = str(round(tree[j,-1],4)),
                     color = self.text_color)
            
        # Legend - Manually inputted
        down = mpatches.Patch(color=self.down_color, label='down movement')
        up = mpatches.Patch(color=self.up_color, label='up movement')

        plt.legend(handles=[up, down])

    def fake_tree(self):
        """
        Method that plot "Aesthetic tree".
        Aesthetic <==> up move = down move
        In other word, price position is not proportional to the actual price. 
        """

        plt.subplots(figsize=self.fig_size) # useful for outpub in jupyternotebook
        plt.gca().axes.yaxis.set_ticklabels([]) # Remove y-axis (confusing otherwise!)

        tree = self.data_tree
        n = len(tree)

        # Fake Tree for aesthetic purposes
        tree_f = np.zeros((n,n)) #(n+1) ?
        tree_f[0,:] = 100 + np.arange(n) * 10 # Vectorise first row
        
        for i in range(n-1,0,-1):
            tree_f[1:i+1,i] = tree_f[0,i] - 20 * np.arange(1,i+1) # vectorise each column 
                    

        for i in range(n-1):
            for j in range(n-1):
                if j <= i:
                    plt.plot([i, i+1], [tree_f[j, i],tree_f[j+1, i+1]],
                             color= self.down_color,zorder=2)

                    plt.plot([i, i+1], [tree_f[j, i],tree_f[j, i+1]],
                             color = self.up_color,zorder=1)

                    plt.text(i-0.15, tree_f[j, i], s = str(round(self.data_tree[j, i], 4)),
                             color = self.text_color, zorder=10)

        for j in range(n):
            plt.text(n-1.15, tree_f[j, -1], s = str(round(tree[j,-1],4)),
                     color = self.text_color)
        
        # Legend - Manually inputted
        down = mpatches.Patch(color=self.down_color, label='down movement')
        up = mpatches.Patch(color=self.up_color, label='up movement')

        plt.legend(handles=[up, down])