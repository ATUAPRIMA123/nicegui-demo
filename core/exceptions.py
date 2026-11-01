"""
Módulo de Exceções Personalizadas
Define a hierarquia de exceções utilizadas no jogo Tic-Tac-Toe AI.
"""


class TicTacToeException(Exception):
    """Exceção base para todos os erros do jogo."""
    pass


class InvalidMoveError(TicTacToeException):
    """Lançada quando uma jogada viola as regras do jogo (ex: fora dos limites)."""
    def __init__(self, row: int, col: int, message: str = "Jogada inválida fora dos limites do tabuleiro."):
        self.row = row
        self.col = col
        super().__init__(f"{message} Coordenadas: ({row}, {col})")


class PositionOccupiedError(InvalidMoveError):
    """Lançada quando o jogador tenta jogar numa célula que já está ocupada."""
    def __init__(self, row: int, col: int):
        super().__init__(row, col, message="A posição selecionada já se encontra ocupada.")


class GameAlreadyOverError(TicTacToeException):
    """Lançada quando se tenta efetuar uma jogada num jogo que já terminou."""
    def __init__(self, message: str = "O jogo já terminou. Inicie uma nova partida."):
        super().__init__(message)


class StorageError(TicTacToeException):
    """Lançada quando ocorre uma falha na leitura ou escrita de ficheiros de persistência."""
    def __init__(self, file_path: str, reason: str):
        self.file_path = file_path
        self.reason = reason
        super().__init__(f"Falha de persistência no ficheiro '{file_path}': {reason}")


class OllamaConnectionError(TicTacToeException):
    """Lançada quando a comunicação com a API local do Ollama falha."""
    def __init__(self, reason: str = "Servidor Ollama inacessível."):
        super().__init__(f"Erro de comunicação com o Ollama: {reason}")
