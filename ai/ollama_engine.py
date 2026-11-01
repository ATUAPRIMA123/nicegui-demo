"""
Módulo de Integração com Ollama (LLM)
Efetua pedidos à API do Ollama para gerar jogadas estratégicas e comentários em linguagem natural.
Inclui tratamento rigoroso de exceções e fallback automático para Minimax.
"""

import json
import re
from typing import Tuple, List, Dict, Any, Optional
import urllib.request
import urllib.error

from core.board import Board
from core.exceptions import OllamaConnectionError
from ai.minimax import get_best_move


class OllamaAIEngine:
    """Motor de IA híbrido: integra modelos Ollama locais com fallback para Minimax."""

    DEFAULT_HOST = "http://localhost:11434"
    DEFAULT_MODEL = "llama3.2"

    PERSONALITIES = {
        "Sarcástico": "És um jogador de Jogo do Galo arrogante, sarcástico e com humor ácido. Faz provocações curtas e engraçadas ao utilizador.",
        "Amigável": "És um jogador amigável, encorajador e simpático que adora ensinar xadrez e jogos de tabuleiro.",
        "Científico": "És um supercomputador frio e calculista que fala de probabilidades, lógica booleana e entropia.",
    }

    def __init__(self, host: str = DEFAULT_HOST, model: str = DEFAULT_MODEL):
        self.host = host.rstrip('/')
        self.model = model

    def check_connection(self) -> Tuple[bool, List[str], str]:
        """
        Verifica se o serviço Ollama está ativo e lista os modelos disponíveis.
        Retorna (is_online, available_models, status_message).
        """
        try:
            req = urllib.request.Request(f"{self.host}/api/tags", headers={"User-Agent": "NiceGUI-TicTacToe"})
            with urllib.request.urlopen(req, timeout=2.5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    models = [m.get('name', '') for m in data.get('models', [])]
                    return True, models, "Ollama online e operacional."
        except urllib.error.URLError as e:
            return False, [], f"Não foi possível ligar ao Ollama ({e.reason})."
        except Exception as e:
            return False, [], f"Erro ao verificar Ollama: {str(e)}"

        return False, [], "Ollama indisponível."

    def _build_prompt(self, board: Board, personality: str) -> str:
        """Constrói o prompt estruturado para o modelo Ollama."""
        available = board.get_available_moves()
        board_str = board.get_board_visual_str()
        persona_desc = self.PERSONALITIES.get(personality, self.PERSONALITIES["Sarcástico"])

        prompt = f"""Tu és a IA num jogo de Jogo do Galo (Tic-Tac-Toe). O teu símbolo é 'O'. O teu adversário humano é 'X'.
{persona_desc}

Estado atual do tabuleiro:
{board_str}

Casas livres disponíveis (linha, coluna): {available}

INSTRUÇÃO:
Escolhe uma das casas livres disponíveis e gera uma frase curta em português (máx. 15 palavras) reagindo ao jogo.
Responde OBRIGATORIAMENTE APENAS em formato JSON válido, sem texto adicional:
{{"row": <int>, "col": <int>, "comment": "<frase curta>"}}
"""
        return prompt

    def get_move_and_comment(
        self,
        board: Board,
        personality: str = "Sarcástico",
        difficulty: str = "Imbatível"
    ) -> Tuple[int, int, str, str]:
        """
        Obtém a jogada da IA.
        Tenta contactar o Ollama. Se falhar, capturar exceções e usar Minimax como fallback.
        Retorna (row, col, comment, engine_used).
        """
        available_moves = board.get_available_moves()
        if not available_moves:
            raise ValueError("Não existem jogadas disponíveis.")

        # Tentativa de obter resposta do Ollama
        try:
            prompt = self._build_prompt(board, personality)
            payload = json.dumps({
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0.4,
                    "num_predict": 120
                }
            }).encode('utf-8')

            req = urllib.request.Request(
                f"{self.host}/api/generate",
                data=payload,
                headers={"Content-Type": "application/json"}
            )

            with urllib.request.urlopen(req, timeout=5.0) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                response_text = result.get('response', '')

                # Parse JSON da resposta
                data = json.loads(response_text)
                row = int(data.get('row'))
                col = int(data.get('col'))
                comment = str(data.get('comment', 'Estou a calcular o teu próximo erro!'))

                # Validação de regras da jogada devolvida pelo LLM
                if (row, col) in available_moves:
                    return row, col, comment, f"Ollama ({self.model})"
                else:
                    # Se o LLM alucinar uma casa já ocupada, fazemos fallback seguro
                    fallback_r, fallback_c = get_best_move(board, difficulty)
                    return fallback_r, fallback_c, f"{comment} (Ajuste tático)", f"Ollama+Minimax"

        except Exception as ex:
            # Tratamento de exceção de conexão/timeout/modelo não encontrado
            fallback_r, fallback_c = get_best_move(board, difficulty)
            fallback_comments = {
                "Sarcástico": "Ollama offline? Sem problema, o algoritmo clássico chega para te vencer!",
                "Amigável": "O servidor Ollama não respondeu, mas continuo aqui a jogar contigo!",
                "Científico": "Conexão neural indisponível. A executar subrotina heurística Minimax.",
            }
            comment = fallback_comments.get(personality, "Modo de contingência Minimax ativo.")
            return fallback_r, fallback_c, comment, "Minimax (Fallback)"
