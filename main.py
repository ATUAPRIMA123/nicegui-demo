from nicegui import ui

# App Header
with ui.header().classes('items-center justify-between bg-primary text-white p-4 shadow-md'):
    with ui.row().classes('items-center gap-2'):
        ui.icon('web', size='md')
        ui.label('NiceGUI Simple Demo').classes('text-xl font-bold')

    dark = ui.dark_mode()
    ui.button('Dark Mode', on_click=dark.toggle, icon='dark_mode').props('flat color=white')

# Main Container
with ui.column().classes('w-full max-w-2xl mx-auto p-6 gap-6 items-stretch'):
    # Welcome Card
    with ui.card().classes('w-full p-4 shadow-sm'):
        ui.label('Welcome to your NiceGUI App!').classes('text-2xl font-semibold text-primary')
        ui.label('A lightweight, reactive Python UI framework built on FastAPI, Vue, and Quasar.').classes('text-gray-500')

    # Interactive Input & Greeting Card
    with ui.card().classes('w-full p-4 shadow-sm'):
        ui.label('Interactive Greeting').classes('text-lg font-medium')
        name_input = ui.input(label='Your Name', placeholder='Type something here...').classes('w-full')
        greeting = ui.label().classes('text-base text-secondary font-medium')
        name_input.bind_value_to(greeting, 'text', forward=lambda val: f'Hello, {val}!' if val else '')

        def on_greet():
            name = name_input.value.strip() or 'Friend'
            ui.notify(f'Nice to meet you, {name}!', color='positive', icon='thumb_up')

        ui.button('Say Hello', on_click=on_greet, icon='send').props('elevated')

    # Counter Card
    with ui.card().classes('w-full p-4 shadow-sm'):
        ui.label('Interactive Counter').classes('text-lg font-medium')

        count = {'val': 0}
        counter_display = ui.label('0').classes('text-2xl font-bold min-w-16 text-center')

        def change_count(delta: int):
            count['val'] += delta
            counter_display.set_text(str(count['val']))

        def reset_count():
            count['val'] = 0
            counter_display.set_text('0')

        with ui.row().classes('items-center gap-4'):
            ui.button('-1', on_click=lambda: change_count(-1), icon='remove').props('outline')
            counter_display
            ui.button('+1', on_click=lambda: change_count(1), icon='add')
            ui.button('Reset', on_click=reset_count).props('flat color=grey')

    # Slider Card
    with ui.card().classes('w-full p-4 shadow-sm'):
        ui.label('Slider & Progress Bar').classes('text-lg font-medium')
        slider = ui.slider(min=0, max=100, value=40)
        progress = ui.linear_progress(value=0.4)
        slider.bind_value_to(progress, 'value', forward=lambda val: val / 100)
        slider_text = ui.label('Value: 40%')
        slider.bind_value_to(slider_text, 'text', forward=lambda val: f'Value: {int(val)}%')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='NiceGUI Demo', port=8080, reload=False)
