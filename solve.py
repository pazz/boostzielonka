#!/usr/bin/python

import sys
import argparse
from ParityGameGraph import ParityGameGraph
from Zielonka import Zielonka


def main():
    # parse parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('graphfile', nargs=1,
                        help='the name of the file containing the game graph')
    parser.add_argument('--output', default=None,
                        choices=["gt", "graphml", "xml", "dot", "gml"],
                        help='the output format')
    args = parser.parse_args()

    # get game graph object
    pg = ParityGameGraph()
    pg.load(args.graphfile[0])

    # get solver and compute winning set
    z = Zielonka(pg)
    W = z.solve()

    # output
    # if not output file format given, print for each node if winning or not.
    if not args.output:
        for v in pg.vertices():
            print v,W[v]
    else:
        # add winning set as new node property to graph
        pg.vp.win = pg.new_vertex_property('int', vals=W)
        # write amended graphfile to stdout
        pg.save(sys.stdout, args.output)

if __name__ == "__main__":
    main()
