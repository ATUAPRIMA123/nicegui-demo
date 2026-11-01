"""
Módulo Minimax
Implementação do algoritmo Minimax clássico com suporte a diferentes níveis de dificuldade.
Serve como fallback robusto para a IA Ollama ou modo de jogo determinístico.
"""

import random
from typing import Tuple, List, Optional
from core.board import Board


def evaluate_board(grid: List[List[str]]) -> int:
    """
    Avalia o tabuleiro estático:
    +10 para vitória de 'O' (IA),
    -10 para vitória de 'X' (Humano),
    0 para empate ou jogo em curso.
    """
    # Linhas e Colunas
    for i in range(3):
        if grid[i][0] != Board.EMPTY and grid[i][0] == grid[i][1] == grid[i][2]:
            return 10 if grid[i][0] == Board.PLAYER_O else -10
        if grid[0][i] != Board.EMPTY and grid[0][i] == grid[1][i] == grid[2][i]:
            return 10 if grid[0][i] == Board.PLAYER_O else -10

    # Diagonais
    if grid[0][0] != Board.EMPTY and grid[0][0] == grid[1][1] == grid[2][2]:
        return 10 if grid[0][0] == Board.PLAYER_O else -10
    if grid[0][2] != Board.EMPTY and grid[0][2] == grid[1][1] == grid[2][0]:
        return 10 if grid[0][2] == Board.PLAYER_O else -10

    return 0


def _minimax(grid: List[List[str]], depth: int, is_maximizing: bool) -> int:
    """Função recursiva Minimax."""
    score = evaluate_board(grid)

    if score == 10:
        return score - depth
    if score == -10:
        return score + depth

    # Verificar se restam casas livres
    empty_cells = [(r, c) for r in range(3) for c in range(3) if grid[r][c] == Board.EMPTY]
    if not empty_cells:
        return 0

    if is_maximizing:
        best_score = -1000
        for r, c in empty_cells:
            grid[r][c] = Board.PLAYER_O
            current_score = _minimax(grid, depth + 1, False)
            grid[r][c] = Board.EMPTY
            best_score = max(best_score, current_score)
        return best_score
    else:
        best_score = 1000
        for r, c in empty_cells:
            grid[r][c] = Board.PLAYER_X
            current_score = _minimax(grid, depth + 1, True)
            grid[r][c] = Board.EMPTY
            best_score = min(best_score, current_score)
        return best_score


def get_best_move(board: Board, difficulty: str = "Imbatível") -> Tuple[int, int]:
    """
    Determina a melhor jogada para a IA ('O').
    Suporta dificuldades:
    - 'Fácil': Escolhe jogadas aleatórias
    - 'Médio': 50% Minimax, 50% aleatório
    - 'Imbatível': 100% Minimax ótimo
    """
    available_moves = board.get_available_moves()
    if not available_moves:
        raise ValueError("Não existem jogadas disponíveis no tabuleiro.")

    # Nível Fácil: Escolha puramente aleatória
    if difficulty.lower() == "fácil":
        return random.choice(available_moves)

    # Nível Médio: Mistura aleatório e Minimax
    if difficulty.lower() == "médio" and random.random() < 0.4:
        return random.choice(available_moves)

    # Nível Imbatível / Minimax Puro
    best_score = -1000
    best_moves: List[Tuple[int, int]] = []

    # Criar cópia da grelha para simulação
    temp_grid = [row[:] for row in board.grid]

    for r, c in available_moves:
        temp_grid[r][c] = Board.PLAYER_O
        move_score = _minimax(temp_grid, 0, False)
        temp_grid[r][c] = Board.EMPTY

        if move_score > best_score:
            best_score = move_score
            best_moves = [(r, c)]
        elif move_score == best_score:
            best_moves.append((r, c))

    return random.choice(best_moves) if best_moves else available_moves[0]
