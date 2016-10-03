class PGSolver(object):
    """ Base class for parity game solver -- algorithms to
    compute winning sets for a given parity game graph
    """

    def __init__(self, pg):
        """
        :param pg: ParityGameGraph
        """
        self.pg = pg
        self.priority = pg.vp.priority
        self.owner = pg.vp.owner

    def solve(self):
        """
        returns a boolean-valued `PropertyMap` representing the winning set
        (of player 0).
        """
        pass
