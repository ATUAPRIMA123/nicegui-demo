"""
Aplicação Principal: Tic-Tac-Toe AI (Jogo do Galo)
Desenvolvido com Python, NiceGUI e integração com Ollama / Minimax.
"""

import time
import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from nicegui import ui

from core.board import Board
from core.exceptions import TicTacToeException, PositionOccupiedError, GameAlreadyOverError
from ai.ollama_engine import OllamaAIEngine
from storage.persistence import StorageManager

# ==========================================
# INICIALIZAÇÃO DE ESTADO E GESTORES
# ==========================================
board = Board()
storage = StorageManager()
settings = storage.load_settings()
ai_engine = OllamaAIEngine(
    host=settings.get('ollama_host', 'http://localhost:11434'),
    model=settings.get('ollama_model', 'llama3.2')
)

game_state = {
    'match_id': str(uuid.uuid4())[:8],
    'start_time': time.time(),
    'is_ai_thinking': False,
    'ai_comment': "Pronto para o desafio? Faz a tua primeira jogada!",
    'ai_last_engine': "Aguardando início",
    'player_name': settings.get('player_name', 'Jogador'),
    'difficulty': settings.get('difficulty', 'Imbatível'),
    'personality': settings.get('personality', 'Sarcástico'),
}


def main():
    ui.page_title('Tic-Tac-Toe AI | Jogo do Galo')

    # Configuração de Tema Escuro
    dark = ui.dark_mode(value=settings.get('dark_mode', False))

    # ==========================================
    # CABEÇALHO SUPERIOR
    # ==========================================
    with ui.header().classes('items-center justify-between bg-primary text-white p-4 shadow-md'):
        with ui.row().classes('items-center gap-3'):
            ui.icon('sports_esports', size='md')
            with ui.column().classes('gap-0'):
                ui.label('Tic-Tac-Toe AI').classes('text-xl font-bold tracking-wide')
                ui.label('Jogo do Galo com Inteligência Artificial').classes('text-xs opacity-80')

        with ui.row().classes('items-center gap-2'):
            # Indicador de estado do Ollama no cabeçalho
            ollama_badge = ui.badge('Ollama Check...', color='grey').props('outline')

            def update_ollama_badge():
                online, _, msg = ai_engine.check_connection()
                if online:
                    ollama_badge.set_text(f'Ollama Online ({ai_engine.model})')
                    ollama_badge.props('color=positive')
                else:
                    ollama_badge.set_text('Ollama Offline (Fallback Ativo)')
                    ollama_badge.props('color=warning')

            ui.timer(0.1, update_ollama_badge, once=True)

            ui.button(
                icon='dark_mode',
                on_click=lambda: (dark.toggle(), storage.save_settings({**settings, 'dark_mode': dark.value}))
            ).props('flat round color=white')

    # ==========================================
    # CONTAINER PRINCIPAL COM ABAS
    # ==========================================
    with ui.column().classes('w-full max-w-5xl mx-auto p-4 gap-4'):
        with ui.tabs().classes('w-full text-primary') as tabs:
            tab_game = ui.tab('🎮 Jogo')
            tab_stats = ui.tab('📊 Estatísticas & Gráficos')
            tab_logs = ui.tab('📜 Histórico & Ficheiros')
            tab_settings = ui.tab('⚙️ Configurações')

        with ui.tab_panels(tabs, value=tab_game).classes('w-full bg-transparent'):

            # ==========================================
            # ABA 1: TABULEIRO DE JOGO
            # ==========================================
            with ui.tab_panel(tab_game).classes('p-0 gap-4'):
                with ui.row().classes('w-full gap-4 items-start justify-center flex-wrap'):
                    
                    # Coluna do Tabuleiro
                    with ui.card().classes('p-6 items-center shadow-lg rounded-2xl w-full max-w-md'):
                        # Indicadores de Jogadores
                        with ui.row().classes('w-full justify-between items-center mb-4 px-2'):
                            player_chip = ui.chip(f"Você: {game_state['player_name']} (X)", icon='person', color='primary')
                            vs_label = ui.label('VS').classes('font-bold text-gray-400')
                            ai_chip = ui.chip(f"IA: {game_state['difficulty']} (O)", icon='smart_toy', color='secondary')

                        turn_banner = ui.label('O teu turno! Escolhe uma casa.').classes(
                            'text-md font-semibold text-center mb-4 text-primary'
                        )

                        # Grelha 3x3 do Tabuleiro
                        buttons_grid = {}
                        with ui.grid(columns=3).classes('gap-3 p-2 bg-gray-100 dark:bg-gray-800 rounded-xl'):
                            for r in range(3):
                                for c in range(3):
                                    btn = ui.button(
                                        '',
                                        on_click=lambda _, row=r, col=c: handle_cell_click(row, col)
                                    ).classes(
                                        'w-24 h-24 text-4xl font-extrabold rounded-xl transition-all hover:scale-105 shadow-sm'
                                    ).props('unelevated color=white text-color=dark')
                                    buttons_grid[(r, c)] = btn

                        # Botão Nova Partida
                        with ui.row().classes('w-full justify-center mt-6'):
                            ui.button('Nova Partida', icon='replay', on_click=lambda: reset_game_ui()).classes(
                                'px-6 py-2 rounded-xl'
                            ).props('elevated color=primary')

                    # Coluna Lateral: Diálogo da IA e Resumo
                    with ui.column().classes('w-full max-w-md gap-4'):
                        # Balão de Fala da IA
                        with ui.card().classes('p-5 w-full shadow-md rounded-2xl'):
                            with ui.row().classes('items-center gap-2 mb-2'):
                                ui.icon('psychology', size='sm', color='secondary')
                                ui.label('Mente da IA (Ollama / Minimax)').classes('font-bold text-secondary')
                            
                            ai_comment_label = ui.label(f'"{game_state["ai_comment"]}"').classes(
                                'italic text-base text-gray-700 dark:text-gray-300 p-3 bg-secondary/10 rounded-xl'
                            )
                            ai_engine_badge = ui.badge(game_state['ai_last_engine'], color='grey').classes('mt-2')

                        # Painel Rápido de Placar
                        with ui.card().classes('p-5 w-full shadow-md rounded-2xl'):
                            ui.label('Placar em Tempo Real').classes('font-bold text-primary mb-2')
                            with ui.row().classes('w-full justify-around text-center'):
                                with ui.column().classes('items-center'):
                                    quick_wins = ui.label('0').classes('text-2xl font-black text-positive')
                                    ui.label('Vitórias').classes('text-xs text-gray-500')
                                with ui.column().classes('items-center'):
                                    quick_losses = ui.label('0').classes('text-2xl font-black text-negative')
                                    ui.label('Derrotas').classes('text-xs text-gray-500')
                                with ui.column().classes('items-center'):
                                    quick_draws = ui.label('0').classes('text-2xl font-black text-warning')
                                    ui.label('Empates').classes('text-xs text-gray-500')

                            def refresh_quick_stats():
                                lb = storage.get_leaderboard()
                                quick_wins.set_text(str(lb.get('player_wins', 0)))
                                quick_losses.set_text(str(lb.get('ai_wins', 0)))
                                quick_draws.set_text(str(lb.get('draws', 0)))

                            refresh_quick_stats()

            # ==========================================
            # ABA 2: ESTATÍSTICAS E GRÁFICOS
            # ==========================================
            with ui.tab_panel(tab_stats).classes('p-4 gap-6'):
                with ui.row().classes('w-full gap-4 items-center justify-between'):
                    ui.label('Visualização Gráfica de Desempenho').classes('text-xl font-bold text-primary')
                    ui.button('Atualizar Dados', icon='refresh', on_click=lambda: update_stats_view()).props('outline')

                # Gráfico ECharts (Elemento de Valorização)
                chart = ui.echart({
                    'title': {'text': 'Distribuição de Resultados', 'left': 'center'},
                    'tooltip': {'trigger': 'item'},
                    'legend': {'orient': 'vertical', 'left': 'left'},
                    'series': [{
                        'name': 'Partidas',
                        'type': 'pie',
                        'radius': '60%',
                        'data': [
                            {'value': 0, 'name': 'Vitórias Jogador'},
                            {'value': 0, 'name': 'Vitórias IA'},
                            {'value': 0, 'name': 'Empates'}
                        ],
                        'emphasis': {
                            'itemStyle': {
                                'shadowBlur': 10,
                                'shadowOffsetX': 0,
                                'shadowColor': 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }]
                }).classes('w-full h-80')

                # Tabela de Partidas Recentes
                ui.label('Tabela de Partidas Recentes (Base de Dados / CSV)').classes('text-lg font-bold mt-4')
                matches_table = ui.table(
                    columns=[
                        {'name': 'match_id', 'label': 'ID', 'field': 'match_id'},
                        {'name': 'timestamp', 'label': 'Data/Hora', 'field': 'timestamp'},
                        {'name': 'player_name', 'label': 'Jogador', 'field': 'player_name'},
                        {'name': 'winner', 'label': 'Vencedor', 'field': 'winner'},
                        {'name': 'total_moves', 'label': 'Jogadas', 'field': 'total_moves'},
                        {'name': 'difficulty', 'label': 'Dificuldade', 'field': 'difficulty'},
                        {'name': 'ai_engine', 'label': 'Motor IA', 'field': 'ai_engine'},
                    ],
                    rows=[],
                    row_key='match_id'
                ).classes('w-full shadow-sm')

                def update_stats_view():
                    lb = storage.get_leaderboard()
                    chart.options['series'][0]['data'] = [
                        {'value': lb.get('player_wins', 0), 'name': 'Vitórias Jogador', 'itemStyle': {'color': '#21ba45'}},
                        {'value': lb.get('ai_wins', 0), 'name': 'Vitórias IA', 'itemStyle': {'color': '#c10015'}},
                        {'value': lb.get('draws', 0), 'name': 'Empates', 'itemStyle': {'color': '#f2c037'}}
                    ]
                    chart.update()
                    records = storage.read_csv_records()
                    matches_table.rows = list(reversed(records))[:15]
                    refresh_quick_stats()

                update_stats_view()

            # ==========================================
            # ABA 3: HISTÓRICO & PERSISTÊNCIA (TXT, CSV, JSON)
            # ==========================================
            with ui.tab_panel(tab_logs).classes('p-4 gap-4'):
                ui.label('Armazenamento Persistente Multi-formato').classes('text-xl font-bold text-primary')
                ui.label('Demonstração dos ficheiros TXT, CSV e JSON criados pelo sistema.').classes('text-sm text-gray-500')

                with ui.row().classes('w-full gap-4'):
                    with ui.card().classes('w-full flex-1 p-4'):
                        ui.label('Log Narrativo em Texto (.txt)').classes('font-bold mb-2')
                        txt_display = ui.code('', language='text').classes('w-full h-64 overflow-y-auto text-xs')

                    with ui.card().classes('w-full flex-1 p-4'):
                        ui.label('Métricas em CSV (.csv)').classes('font-bold mb-2')
                        csv_display = ui.code('', language='text').classes('w-full h-64 overflow-y-auto text-xs')

                def refresh_logs_tab():
                    txt_display.set_content(storage.read_text_logs(max_lines=40))
                    try:
                        with open(storage.CSV_PATH, 'r', encoding='utf-8') as f:
                            csv_display.set_content(f.read())
                    except Exception:
                        csv_display.set_content("CSV não inicializado.")

                ui.button('Recarregar Ficheiros', icon='refresh', on_click=refresh_logs_tab).classes('mt-2')
                refresh_logs_tab()

            # ==========================================
            # ABA 4: CONFIGURAÇÕES E OLLAMA
            # ==========================================
            with ui.tab_panel(tab_settings).classes('p-4 gap-4'):
                ui.label('Configurações do Jogo & Parâmetros de IA').classes('text-xl font-bold text-primary')

                with ui.card().classes('w-full max-w-xl p-6 gap-4'):
                    name_input = ui.input(
                        'Nome do Jogador',
                        value=game_state['player_name'],
                        validation={'Tamanho mínimo': lambda v: len(v.strip()) >= 2}
                    ).classes('w-full')

                    personality_select = ui.select(
                        label='Personalidade da IA (Ollama)',
                        options=['Sarcástico', 'Amigável', 'Científico'],
                        value=game_state['personality']
                    ).classes('w-full')

                    difficulty_select = ui.select(
                        label='Dificuldade Minimax (Modo Fallback / Heurístico)',
                        options=['Fácil', 'Médio', 'Imbatível'],
                        value=game_state['difficulty']
                    ).classes('w-full')

                    ollama_host_input = ui.input('Host do Ollama', value=ai_engine.host).classes('w-full')
                    ollama_model_input = ui.input('Modelo Ollama', value=ai_engine.model).classes('w-full')

                    status_msg = ui.label('').classes('text-sm font-medium')

                    def test_and_save_settings():
                        validated_name = Board.validate_player_name(name_input.value)
                        game_state['player_name'] = validated_name
                        game_state['personality'] = personality_select.value
                        game_state['difficulty'] = difficulty_select.value

                        ai_engine.host = ollama_host_input.value.strip()
                        ai_engine.model = ollama_model_input.value.strip()

                        # Salvar em JSON
                        storage.save_settings({
                            'player_name': validated_name,
                            'personality': personality_select.value,
                            'difficulty': difficulty_select.value,
                            'ollama_host': ai_engine.host,
                            'ollama_model': ai_engine.model,
                            'dark_mode': dark.value,
                        })

                        # Testar conexão
                        is_online, models, test_msg = ai_engine.check_connection()
                        update_ollama_badge()
                        player_chip.set_text(f"Você: {validated_name} (X)")
                        ai_chip.set_text(f"IA: {difficulty_select.value} (O)")

                        if is_online:
                            status_msg.set_text(f"✅ Sucesso! Conectado ao Ollama. Modelos: {', '.join(models) if models else 'Nenhum modelo baixado'}")
                            status_msg.classes('text-positive')
                            ui.notify('Configurações salvas e Ollama operacional!', color='positive')
                        else:
                            status_msg.set_text(f"⚠️ {test_msg} O jogo usará o algoritmo Minimax.")
                            status_msg.classes('text-warning')
                            ui.notify('Configurações salvas (Ollama offline: Minimax ativo)', color='warning')

                    ui.button('Guardar e Testar Conexão', icon='save', on_click=test_and_save_settings).props('elevated color=primary')

    # ==========================================
    # LÓGICA DE JOGO E INTERAÇÃO
    # ==========================================
    def handle_cell_click(row: int, col: int):
        """Trata o clique do jogador humano numa célula da grelha."""
        if board.is_game_over or game_state['is_ai_thinking']:
            return

        try:
            # 1. Jogada Humana
            is_over, winner = board.make_move(row, col, Board.PLAYER_X)
            update_board_display()

            if is_over:
                handle_game_conclusion(winner)
                return

            # 2. Turno da IA
            turn_banner.set_text('A IA está a pensar na sua jogada...')
            game_state['is_ai_thinking'] = True

            # Agendamento assíncrono para UI responsiva
            ui.timer(0.2, trigger_ai_turn, once=True)

        except PositionOccupiedError:
            ui.notify('Essa casa já está ocupada!', color='warning', icon='warning')
        except GameAlreadyOverError:
            ui.notify('O jogo já terminou! Inicie uma nova partida.', color='info')
        except TicTacToeException as e:
            ui.notify(f'Erro no jogo: {e}', color='negative')

    def trigger_ai_turn():
        """Executa a jogada da IA com Ollama ou Minimax."""
        try:
            r, c, comment, engine_used = ai_engine.get_move_and_comment(
                board,
                personality=game_state['personality'],
                difficulty=game_state['difficulty']
            )

            is_over, winner = board.make_move(r, c, Board.PLAYER_O)
            game_state['ai_comment'] = comment
            game_state['ai_last_engine'] = engine_used
            ai_comment_label.set_text(f'"{comment}"')
            ai_engine_badge.set_text(engine_used)

            update_board_display()

            if is_over:
                handle_game_conclusion(winner)
            else:
                turn_banner.set_text('O teu turno! Escolhe uma casa.')

        except Exception as e:
            ui.notify(f'Erro na jogada da IA: {e}', color='negative')
        finally:
            game_state['is_ai_thinking'] = False

    def update_board_display():
        """Atualiza o texto, cores e estados dos botões do tabuleiro."""
        for r in range(3):
            for c in range(3):
                symbol = board.grid[r][c]
                btn = buttons_grid[(r, c)]
                btn.set_text(symbol if symbol != Board.EMPTY else '')

                # Estilização conforme o símbolo
                if symbol == Board.PLAYER_X:
                    btn.props('unelevated color=primary text-color=white')
                elif symbol == Board.PLAYER_O:
                    btn.props('unelevated color=secondary text-color=white')
                else:
                    btn.props('unelevated color=white dark:color=grey-9 text-color=dark')

        # Destaque da linha vencedora
        if board.winning_line:
            for wr, wc in board.winning_line:
                buttons_grid[(wr, wc)].props('unelevated color=positive text-color=white')

    def handle_game_conclusion(winner: Optional[str]):
        """Regista persistência e notifica os utilizadores sobre o fim de partida."""
        duration = round(time.time() - game_state['start_time'], 1)
        match_data = {
            'match_id': game_state['match_id'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'player_name': game_state['player_name'],
            'winner': winner,
            'total_moves': len(board.moves_history),
            'difficulty': game_state['difficulty'],
            'ai_engine': game_state['ai_last_engine'],
            'duration_seconds': duration
        }

        # Persistência em TXT, CSV, JSON e SQLite simultaneamente!
        storage.record_match_all_formats(match_data)
        refresh_quick_stats()

        if winner == Board.PLAYER_X:
            turn_banner.set_text('🎉 Parabéns! Venceste a partida!')
            ui.notify(f'Vitória esmagadora de {game_state["player_name"]}!', color='positive', icon='emoji_events')
        elif winner == Board.PLAYER_O:
            turn_banner.set_text('🤖 A IA venceu esta partida!')
            ui.notify('A Inteligência Artificial levou a melhor desta vez!', color='negative', icon='sentiment_very_dissatisfied')
        else:
            turn_banner.set_text('🤝 Empate (Galo)! Bom jogo!')
            ui.notify('Empate! Ninguém cedeu espaço.', color='warning', icon='handshake')

    def reset_game_ui():
        """Reinicia o estado para uma nova partida."""
        board.reset()
        game_state['match_id'] = str(uuid.uuid4())[:8]
        game_state['start_time'] = time.time()
        game_state['is_ai_thinking'] = False
        game_state['ai_comment'] = "Nova partida iniciada! Que vença o melhor."
        ai_comment_label.set_text(f'"{game_state["ai_comment"]}"')
        turn_banner.set_text('O teu turno! Escolhe uma casa.')
        update_board_display()
        ui.notify('Nova partida iniciada!', color='info')


if __name__ in {'__main__', '__mp_main__'}:
    main()
    ui.run(title='Tic-Tac-Toe AI | Jogo do Galo', port=8080, reload=False)
