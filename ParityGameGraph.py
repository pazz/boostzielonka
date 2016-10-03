from graph_tool import Graph, GraphView
from itertools import imap, ifilter


class ParityGameGraph(Graph):
    """ParityGameGraph is the game graph of a parity game.
    Vertices have properties owner (int) and priority (int).
    """

    def __init__(self):
        Graph.__init__(self)
        # add vertex properties for priority and owner
        self.vp.priority = self.new_vertex_property('short')
        self.vp.owner = self.new_vertex_property('short')

    def load(self, file_name):
        Graph.load(self, file_name)
        self.vp.priority = self.new_vertex_property('short', vals=self.vp.priority)
        self.vp.owner = self.new_vertex_property('short', vals=self.vp.priority)



    def vertices(self, priority=None):
        """ iterator over all verices (with given priority) """
        it = Graph.vertices(self)
        if priority is not None:
            it = ifilter(lambda v: self.vp.priority[v]==priority, it)
        return it

    def maxparity(self):
        """ return the maximal parity of all nodes """
        return self.vp.priority.ma.max().item()

    def save(self, file_name, fmt="auto"):
        """ overload Graph.save to make output dotfiles pretty.
            This is entirely cosmetic. """
        u = self

        # add some properties to prettify dot output
        if fmt is "dot" or fmt is "auto" and file_name.endswith(".dot"):
            u = GraphView(self)

            # add shape property according to vertex owners
            shape = u.new_vertex_property("string")
            for v in u.vertices():
                if u.vp.owner[v] == 1:
                    shape[v] = "box"
                else:
                    shape[v] = "diamond"
            u.vp.shape = shape

            # add label property according to priorities
            #u.vertex_properties['label'] = u.vertex_properties['priority']
            label = u.new_vertex_property("string")
            for v in u.vertices():
                prio = u.vertex_properties['priority'][v]
                name = u.vertex_index[v]
                label[v] = "%d (%d)" % (name, prio)
            u.vp.label = label

        Graph.save(u, file_name, fmt)
