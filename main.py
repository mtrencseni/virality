import math
import random
import networkx as nx # pip install networkx

def init_simulation():
    g = nx.barabasi_albert_graph(100*1000, 10)
    # g = nx.watts_strogatz_graph(100*1000, 10, 0.5)
    # g = nx.gnm_random_graph(100*1000, 10*100*1000)
    # print(g.number_of_nodes())
    # print(g.number_of_edges())

    # get maximum node degree
    max_degree = 0
    for n in g:
        degree = len(g.neighbors(n))
        max_degree = max(max_degree, degree)
        g[n]["state"] = "blank"
    for n in g:
        degree = len(g.neighbors(n))
        g[n]["fitness_threshold"] = 1.0 - math.sqrt(math.log(degree) / math.log(max_degree))
        g[n]["adoption_round"] = "not_adopted"
    g[0]["state"] = "adopter"
    g[0]["adoption_round"] = 0
    sim = {}
    sim["g"] = g
    sim["adopters"] = [0]
    sim["product_fitness"] = 0.0
    sim["round"] = 0
    print(len(g.neighbors(0)))
    return sim

def advance_simulation(sim):
    sim["product_fitness"] += 0.01
    for i in xrange(3):
        sim["round"] += 1
        for n1 in sim["adopters"]:
            if sim["g"][n1]["adoption_round"] in xrange(sim["round"] - 1000, sim["round"]):
                for n2 in sim["g"].neighbors(n1):
                    if not isinstance(n2, int): continue
                    if sim["g"][n2]["state"] != "adopter":
                        num_adopters = 0
                        num_detractors = 0
                        for n3 in sim["g"].neighbors(n2):
                            if not isinstance(n3, int): continue
                            if sim["g"][n3]["state"] == "adopter":
                                num_adopters += 1
                            elif sim["g"][n3]["state"] == "detractor":
                                num_detractors += 1
                        if random.random() < 0.1 or sim["g"][n2]["state"] == "blank" or num_adopters >= num_detractors:
                            if random.random() < 0.01 or sim["product_fitness"] >= sim["g"][n2]["fitness_threshold"]:
                                sim["g"][n2]["state"] = "adopter"
                                sim["g"][n2]["adoption_round"] = sim["round"]
                                sim["adopters"].append(n2)
                            else:
                                sim["g"][n2]["state"] = "detractor"
        # print("%f, %d" % (sim["product_fitness"], len(sim["adopters"])))
        print("%d, %f, %d" % (sim["round"], sim["product_fitness"], len(sim["adopters"])))

sim = init_simulation()
while sim["product_fitness"] < 1:
# for i in xrange(36):
    advance_simulation(sim)
