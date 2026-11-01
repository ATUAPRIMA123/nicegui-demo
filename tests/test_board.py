"""
Testes Automatizados para a Lógica do Tabuleiro (Board)
Utiliza a biblioteca padrão unittest do Python.
"""

import unittest
from core.board import Board
from core.exceptions import InvalidMoveError, PositionOccupiedError, GameAlreadyOverError
from ai.minimax import get_best_move, evaluate_board


class TestBoardLogic(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_state(self):
        """Verifica o estado inicial limpo do tabuleiro."""
        self.assertEqual(len(self.board.get_available_moves()), 9)
        self.assertEqual(self.board.current_turn, Board.PLAYER_X)
        self.assertFalse(self.board.is_game_over)
        self.assertIsNone(self.board.winner)

    def test_valid_move(self):
        """Testa a execução de jogadas válidas alternadas."""
        is_over, winner = self.board.make_move(0, 0)
        self.assertFalse(is_over)
        self.assertIsNone(winner)
        self.assertEqual(self.board.grid[0][0], Board.PLAYER_X)
        self.assertEqual(self.board.current_turn, Board.PLAYER_O)

    def test_occupied_position_raises_exception(self):
        """Garante que jogar numa célula já ocupada levanta PositionOccupiedError."""
        self.board.make_move(1, 1)
        with self.assertRaises(PositionOccupiedError):
            self.board.make_move(1, 1)

    def test_out_of_bounds_raises_exception(self):
        """Garante que coordenadas fora de 0-2 levantam InvalidMoveError."""
        with self.assertRaises(InvalidMoveError):
            self.board.make_move(3, 0)
        with self.assertRaises(InvalidMoveError):
            self.board.make_move(-1, 2)

    def test_horizontal_win(self):
        """Testa vitória horizontal na linha 0."""
        # X: (0,0), O: (1,0), X: (0,1), O: (1,1), X: (0,2) -> X vence
        self.board.make_move(0, 0)  # X
        self.board.make_move(1, 0)  # O
        self.board.make_move(0, 1)  # X
        self.board.make_move(1, 1)  # O
        is_over, winner = self.board.make_move(0, 2)  # X
        self.assertTrue(is_over)
        self.assertEqual(winner, Board.PLAYER_X)

    def test_diagonal_win(self):
        """Testa vitória na diagonal principal."""
        self.board.make_move(0, 0)  # X
        self.board.make_move(0, 1)  # O
        self.board.make_move(1, 1)  # X
        self.board.make_move(0, 2)  # O
        is_over, winner = self.board.make_move(2, 2)  # X
        self.assertTrue(is_over)
        self.assertEqual(winner, Board.PLAYER_X)

    def test_draw_game(self):
        """Testa condição de empate (velha)."""
        # X O X
        # X X O
        # O X O
        moves = [
            (0, 0),  # X
            (0, 1),  # O
            (0, 2),  # X
            (1, 2),  # O
            (1, 0),  # X
            (2, 0),  # O
            (1, 1),  # X
            (2, 2),  # O
            (2, 1),  # X
        ]
        for r, c in moves:
            is_over, winner = self.board.make_move(r, c)
        self.assertTrue(is_over)
        self.assertEqual(winner, 'DRAW')

    def test_move_after_game_over_raises_exception(self):
        """Garante que não é permitido jogar após o fim da partida."""
        self.board.make_move(0, 0)
        self.board.make_move(1, 0)
        self.board.make_move(0, 1)
        self.board.make_move(1, 1)
        self.board.make_move(0, 2)  # X vence aqui
        with self.assertRaises(GameAlreadyOverError):
            self.board.make_move(2, 2)

    def test_minimax_prevents_immediate_loss(self):
        """Garante que a IA Minimax bloqueia vitória iminente do jogador."""
        # X tem (0,0) e (0,1). IA ('O') deve bloquear em (0,2).
        self.board.make_move(0, 0)  # X
        self.board.make_move(1, 1)  # O no centro
        self.board.make_move(0, 1)  # X ameaça ganhar em (0,2)
        ai_move = get_best_move(self.board, "Imbatível")
        self.assertEqual(ai_move, (0, 2))


if __name__ == '__main__':
    unittest.main()
