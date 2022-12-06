def graph_tree(tree, graph_type="", up_color="cornflowerblue",
               down_color="salmon", text_color="black"):
    """
    Plot BINOMIAL Tree using matplotlib


    Args:
        tree (DataFrame): DataFrame containing Binomial Tree Data
        graph_type (str, optional): if "real" Graph takes into account 
                                    actual value. Else, it will plot standard
                                    Binomial Tree. Defaults to "". 

        up_color (str, optional): _description_. Defaults to "cornflowerblue".
        down_color (str, optional): _description_. Defaults to "salmon".
        text_color (str, optional): _description_. Defaults to "black".
    Requirement: 
        import matplotlib.pyplot as plt
    """
    fig, ax = plt.subplots(figsize=(16, 8))

    n = len(tree)

    if graph_type == "real":

        for i in range(len(tree)-1):
            for j in range(len(tree)-1):
                if j > i:
                    next
                else:

                    plt.plot([i, i+1], [tree[j][i], tree[j+1][i+1]],
                             color=down_color)

                    plt.plot([i, i+1], [tree[j][i], tree[j][i+1]],
                             color=up_color)

                    plt.text(
                        i-0.15, tree[j][i], s=str(round(tree[j][i], 4)), color=text_color, zorder=10)

    for j in range(len(tree)-1):
        plt.text(n-1.15, tree[j-1][-1],
                 s=str(round(tree[j-1][-1], 4)), color=text_color)

    # Aesthetic tree where the price position
    # is not proportional to the actual price
    
    else:
        tree_f = np.zeros((n+1, n+1))
        tree_f[0][0] = 100
        for i in range(n):
            tree_f[0][i+1] = tree_f[0][i] + 10

            for j in range(n):
                if j > i:
                    next
                else:
                    tree_f[j+1][i+1] = tree_f[j][i] - 10

        for i in range(n):
            for j in range(n):
                if j > i:
                    next
                else:
                    plt.plot([i, i+1], [tree_f[j,i], tree_f[j+1]
                             [i+1]], color=down_color, zorder=2)

                    plt.plot([i, i+1], [tree_f[j][i], tree_f[j][i+1]],
                             color=up_color, zorder=1)

                    plt.text(
                        i-0.15, tree_f[j,i], s=str(round(tree[j][i], 4)), color=text_color, zorder=10)

        for j in range(n+1):
            plt.text(
                n-0.15, tree_f[j-1,-1], s=str(round(tree[j-1][-1], 4)), color=text_color)
