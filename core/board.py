"""
Módulo de Lógica do Tabuleiro (Board)
Gere o estado, validação de regras, jogadas e deteção de vitória/empate no jogo do Galo.
"""

from typing import List, Tuple, Optional, Dict, Any
from core.exceptions import InvalidMoveError, PositionOccupiedError, GameAlreadyOverError


class Board:
    """
    Representa o tabuleiro 3x3 do Jogo do Galo (Tic-Tac-Toe).
    Utiliza uma matriz 3x3 (lista de listas) como estrutura de dados primária.
    """

    PLAYER_X = 'X'  # Normalmente o utilizador humano
    PLAYER_O = 'O'  # Normalmente a Inteligência Artificial
    EMPTY = ' '

    def __init__(self):
        self.grid: List[List[str]] = [[self.EMPTY for _ in range(3)] for _ in range(3)]
        self.current_turn: str = self.PLAYER_X
        self.winner: Optional[str] = None
        self.winning_line: Optional[List[Tuple[int, int]]] = None
        self.is_game_over: bool = False
        self.moves_history: List[Dict[str, Any]] = []

    def reset(self) -> None:
        """Reinicia o tabuleiro para um novo jogo."""
        self.grid = [[self.EMPTY for _ in range(3)] for _ in range(3)]
        self.current_turn = self.PLAYER_X
        self.winner = None
        self.winning_line = None
        self.is_game_over = False
        self.moves_history.clear()

    @staticmethod
    def validate_coordinates(row: int, col: int) -> None:
        """
        Valida se as coordenadas estão dentro dos limites [0, 2].
        Lança InvalidMoveError caso estejam fora dos limites.
        """
        if not (0 <= row <= 2 and 0 <= col <= 2):
            raise InvalidMoveError(row, col, "Coordenadas fora dos limites válidos (0 a 2).")

    @staticmethod
    def validate_player_name(name: str) -> str:
        """
        Valida e higieniza o nome de utilizador introduzido.
        Garante tamanho mínimo e remove espaços desnecessários.
        """
        cleaned = name.strip() if name else ""
        if len(cleaned) < 2:
            return "Jogador"
        return cleaned[:25]

    def is_cell_empty(self, row: int, col: int) -> bool:
        """Verifica se uma determinada posição do tabuleiro está livre."""
        self.validate_coordinates(row, col)
        return self.grid[row][col] == self.EMPTY

    def get_available_moves(self) -> List[Tuple[int, int]]:
        """Retorna uma lista de tuplos (linha, coluna) com as casas ainda livres."""
        return [
            (r, c)
            for r in range(3)
            for c in range(3)
            if self.grid[r][c] == self.EMPTY
        ]

    def make_move(self, row: int, col: int, player: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """
        Executa uma jogada no tabuleiro.
        Valida limites, ocupação da célula e estado de término.
        
        Retorna (is_game_over, winner).
        """
        if self.is_game_over:
            raise GameAlreadyOverError()

        self.validate_coordinates(row, col)

        if not self.is_cell_empty(row, col):
            raise PositionOccupiedError(row, col)

        player_symbol = player or self.current_turn
        if player_symbol not in (self.PLAYER_X, self.PLAYER_O):
            raise ValueError(f"Símbolo de jogador inválido: '{player_symbol}'. Deve ser 'X' ou 'O'.")

        # Regista a jogada no tabuleiro
        self.grid[row][col] = player_symbol
        self.moves_history.append({
            'step': len(self.moves_history) + 1,
            'player': player_symbol,
            'position': (row, col)
        })

        # Verifica fim de jogo
        self._check_game_state()

        # Alterna o turno caso o jogo continue
        if not self.is_game_over:
            self.current_turn = self.PLAYER_O if self.current_turn == self.PLAYER_X else self.PLAYER_X

        return self.is_game_over, self.winner

    def _check_game_state(self) -> None:
        """Verifica se há um vencedor ou se o tabuleiro atingiu o empate (velha)."""
        # 1. Verificar Linhas
        for r in range(3):
            if self.grid[r][0] != self.EMPTY and self.grid[r][0] == self.grid[r][1] == self.grid[r][2]:
                self.winner = self.grid[r][0]
                self.winning_line = [(r, 0), (r, 1), (r, 2)]
                self.is_game_over = True
                return

        # 2. Verificar Colunas
        for c in range(3):
            if self.grid[0][c] != self.EMPTY and self.grid[0][c] == self.grid[1][c] == self.grid[2][c]:
                self.winner = self.grid[0][c]
                self.winning_line = [(0, c), (1, c), (2, c)]
                self.is_game_over = True
                return

        # 3. Verificar Diagonal Principal
        if self.grid[0][0] != self.EMPTY and self.grid[0][0] == self.grid[1][1] == self.grid[2][2]:
            self.winner = self.grid[0][0]
            self.winning_line = [(0, 0), (1, 1), (2, 2)]
            self.is_game_over = True
            return

        # 4. Verificar Diagonal Secundária
        if self.grid[0][2] != self.EMPTY and self.grid[0][2] == self.grid[1][1] == self.grid[2][0]:
            self.winner = self.grid[0][2]
            self.winning_line = [(0, 2), (1, 1), (2, 0)]
            self.is_game_over = True
            return

        # 5. Verificar Empate (sem mais jogadas disponíveis)
        if len(self.get_available_moves()) == 0:
            self.winner = 'DRAW'
            self.winning_line = None
            self.is_game_over = True

    def get_board_visual_str(self) -> str:
        """Retorna uma representação em texto do tabuleiro formatado."""
        rows_str = []
        for row in self.grid:
            rows_str.append(" " + " | ".join(row) + " ")
        return "\n---+---+---\n".join(rows_str)

    def to_dict(self) -> Dict[str, Any]:
        """Serializa o estado do tabuleiro para dicionário."""
        return {
            'grid': [row[:] for row in self.grid],
            'current_turn': self.current_turn,
            'winner': self.winner,
            'is_game_over': self.is_game_over,
            'moves_count': len(self.moves_history)
        }
