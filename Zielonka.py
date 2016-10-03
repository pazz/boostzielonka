from PGSolver import PGSolver  # interface of solvers defined here
from graph_tool import GraphView
from itertools import imap
from numpy import logical_not


class Zielonka(PGSolver):
    """ A parity game solver that implements Zielonka's dynamic programming
        algorithm """

    def attractor(self, U, i):
        """
        computes the 1-step i-attractor of mask U.
        The result is a boolean-valued PropertyMap.
        """

        def att(U, i):
            # if U contains already all vertices of g return U
            if U.ma.all():
                return U

            # otherwise extend U by 1-step safe states and return attractor
            # of the result result
            else:
                g = U.get_graph()
                changed = False
                for v in g.vertices():
                    if U[v]:
                        for w in v.in_neighbours():
                            if not U[w]:
                                if self.pg.vp.owner[w] == i:
                                    # add safe i-predecessor w
                                    changed = True
                                    U[w] = True
                                else:
                                    # add safe (1-i)-predecessor w
                                    all_in = True
                                    for vv in w.out_neighbours():
                                        all_in = all_in and U[vv]
                                    if all_in:
                                        U[w] = all_in
                                        changed = True
                if changed:
                    return att(U, i)
                else:
                    return U

        return att(U.copy(), i)

    def maxparity(self, subgraph):
        """ maximal parity among nodes of subgraph """
        prio_it = imap(lambda v: self.pg.vp.priority[v], subgraph.vertices())
        return reduce(max, prio_it, 0)

    def complement(self, Mask):
        """ flip given bitmask (that represents a subset of nodes) """
        graph=Mask.get_graph()
        #it = imap(lambda x:not Mask[x], graph.vertices())
        notMaskarr = logical_not(Mask.ma)
        return graph.new_vertex_property("bool", vals=notMaskarr)

    def maskplus(self, graph, M, W):
        """ add two bitmasks (to represent the union) """
        return self.pg.new_vertex_property('bool', vals=M.ma+W.ma)

    def vertices_with_priority(self, g, p):
        """ create bitmask representing all nodes with a given priority """
        it = imap(lambda x: self.pg.vp.priority[x]==p, g.vertices())
        return g.new_vertex_property('bool', vals=it)

    def solve(self):
        def solve(g):
            if g.num_vertices() == 0:
                W0 = self.pg.new_vertex_property("bool")
                W1 = self.pg.new_vertex_property("bool")
                return {0:W0, 1:W1}
            else:
                p = self.maxparity(g)
                i= p%2

                U=self.vertices_with_priority(g, p)

                A = self.attractor(U, i)  # get i attractor of U in g
                WW = solve(GraphView(g, vfilt=self.complement(A)))

                #if WW[1-i].ma.all():  ## does not work
                gg = GraphView(g, vfilt=WW[1-i]) # just to check emptiness
                if gg.num_vertices() == 0:
                    res = {}
                    res[i] = self.maskplus(g,WW[i],A)
                    res[1-i] = WW[1-i]
                    return res
                else:
                    B = self.attractor(WW[1-i], 1-i)
                    gg = GraphView(g, vfilt=self.complement(B))
                    WW = solve(gg)

                    res = {}
                    res[i] = WW[i]
                    res[1-i] = self.maskplus(g, WW[1-i], B)
                    return res
        return solve(self.pg)[0]
