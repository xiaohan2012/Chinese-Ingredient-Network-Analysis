import networkx as nx
import matplotlib.pyplot as plt

def degree_histgram(path="data/douguo.gpickle"):
    g = nx.read_gpickle(path)
    ds = nx.degree(g)
    y = ds.values()
    plt.hist(y)
    plt.title("Degree distribution plot")
    plt.ylabel("#")
    plt.xlabel("degree")
    plt.show()

def popular_ingredients(path="data/douguo.gpickle", n = 100):
    g = nx.read_gpickle(path)
    ds = nx.degree(g)
    return sorted(ds, key = lambda k: ds[k], reverse = True)[:n]

def main():
    #degree_histgram()
    print " ".join(popular_ingredients())

if __name__ == '__main__':
    main()