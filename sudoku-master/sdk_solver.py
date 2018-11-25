"""                     # Sudoku
CIS 211 project 6
Author: Anne Glickenhaus
Sudoku solution tactics.  These include the
constraint propogation tactics and (in phase
two) the search-based solver.
"""

from sdk_board import Board
from sdk_tile import UNKNOWN

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def naked_single(board: Board) -> bool:
    """As described in http://www.sadmansoftware.com/sudoku/nakedsingle.php
    Returns True iff some change has been made
    """
    logging.info("Applying naked single tactic")
    changed = False
    for group in board.groups:
        changed = group.naked_single_constrain() or changed
    return changed


def hidden_single(board: Board) -> bool:
    """As described in http://www.sadmansoftware.com/sudoku/hiddensingle.php
    Returns True iff some change has been made
    """
    logging.info("Applying hidden single tactic")
    changed = False
    for group in board.groups:
        changed = group.hidden_single_constrain() or changed
    return changed


def propagate(board: Board):
    """Propagate constraints until we either solve the puzzle,
    show the puzzle as given is unsolvable, or can make no more
    progress by constraint propagation.
    """
    logging.info("Propagating constraints")
    changed = True
    while changed:
        logging.info("Invoking naked single")
        changed = naked_single(board)
        if board.is_solved() or not board.is_consistent():
            return
        changed = hidden_single(board) or changed
        if board.is_solved() or not board.is_consistent():
            return
    return


def solve(board: Board) -> bool:
    """Main solver.  Initially this just invokes constraint
    propagation.  In phase 2 of the project, you will add
    recursive back-tracking search (guess-and-check with recursion).
    """

    log.debug("Called solve on board:\n{}".format(board))
    propagate(board)

    if board.is_solved():
        return True
    if not board.is_consistent():
        return False

    saved = board.as_list()

    minCand = 10
    bestTile = None

    for row in board.tiles:
        for tile in row:
            if tile.value == UNKNOWN and len(tile.candidates) < minCand:
                minCand = len(tile.candidates)
                bestTile = tile

    for guess in bestTile.candidates:
        bestTile.set_value(guess)

        isSolved = solve(board)

        if not isSolved:
            board.set_tiles(saved)
        else:
            return True

    return False
