"""
Módulo de Integração com Ollama (LLM)
Efetua pedidos à API do Ollama para gerar jogadas estratégicas e comentários contextuais.
Inclui tratamento de exceções e fallback para o motor Minimax.
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
        "Sarcástico": "És um jogador experiente de Jogo do Galo. Faz comentários breves e irónicos sobre o jogo.",
        "Amigável": "És um jogador cordial e positivo. Faz comentários encorajadores e breves.",
        "Analítico": "És um jogador focado em estratégia e probabilidade. Faz comentários concisos sobre a posição.",
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
            req = urllib.request.Request(f"{self.host}/api/tags", headers={"User-Agent": "TicTacToe-Client"})
            with urllib.request.urlopen(req, timeout=2.0) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    models = [m.get('name', '') for m in data.get('models', [])]
                    return True, models, "Serviço ativo"
        except urllib.error.URLError as e:
            return False, [], f"Falha de ligação ({e.reason})"
        except Exception as e:
            return False, [], f"Erro de comunicação: {str(e)}"

        return False, [], "Serviço indisponível"

    def _build_prompt(self, board: Board, personality: str) -> str:
        """Constrói o prompt estruturado para o modelo Ollama."""
        available = board.get_available_moves()
        board_str = board.get_board_visual_str()
        persona_desc = self.PERSONALITIES.get(personality, self.PERSONALITIES["Sarcástico"])

        prompt = f"""Tu és o jogador 'O' num jogo de Jogo do Galo (Tic-Tac-Toe). O adversário é 'X'.
{persona_desc}

Tabuleiro atual:
{board_str}

Casas livres (linha, coluna): {available}

Regra estrita:
Escolhe uma das casas livres e escreve um comentário curto (máx. 12 palavras).
Responde exclusivamente em formato JSON:
{{"row": <int>, "col": <int>, "comment": "<comentário>"}}
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
        Tenta contactar o Ollama. Se falhar, utiliza Minimax como contingência.
        Retorna (row, col, comment, engine_used).
        """
        available_moves = board.get_available_moves()
        if not available_moves:
            raise ValueError("Não existem jogadas disponíveis.")

        try:
            prompt = self._build_prompt(board, personality)
            payload = json.dumps({
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0.3,
                    "num_predict": 100
                }
            }).encode('utf-8')

            req = urllib.request.Request(
                f"{self.host}/api/generate",
                data=payload,
                headers={"Content-Type": "application/json"}
            )

            with urllib.request.urlopen(req, timeout=4.0) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                response_text = result.get('response', '')

                data = json.loads(response_text)
                row = int(data.get('row'))
                col = int(data.get('col'))
                comment = str(data.get('comment', 'Jogada realizada.'))

                if (row, col) in available_moves:
                    return row, col, comment, f"Ollama ({self.model})"
                else:
                    fallback_r, fallback_c = get_best_move(board, difficulty)
                    return fallback_r, fallback_c, f"{comment} [Ajuste posicional]", "Ollama+Minimax"

        except Exception:
            fallback_r, fallback_c = get_best_move(board, difficulty)
            fallback_comments = {
                "Sarcástico": "Serviço Ollama indisponível. Jogada calculada por Minimax.",
                "Amigável": "Sem resposta do Ollama. A utilizar motor Minimax.",
                "Analítico": "Ollama offline. Heurística Minimax aplicada.",
            }
            comment = fallback_comments.get(personality, "Minimax ativo.")
            return fallback_r, fallback_c, comment, "Minimax"
