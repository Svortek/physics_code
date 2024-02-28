from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

# Регистрация кастомного шрифта
LabelBase.register(name='TimesNewRoman', fn_regular='TimesNewRoman.ttf')

class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 14
        self.font_name = 'TimesNewRoman'
        self.background_normal = ''  # Убрать фон
        self.background_color = (1, 0.647, 0, 1)  # Оранжевый цвет
        self.size_hint = (None, None)
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source='background.webp', allow_stretch=True, keep_ratio=False))
        self.layout = FloatLayout()
        
        self.menu_button = CustomButton(
            text='Выбрать формулы',
            size_hint=(None, None),
            size=(Window.width * 0.3, Window.height * 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.menu_button.bind(on_release=self.open_calculations)
        self.layout.add_widget(self.menu_button)
        self.add_widget(self.layout)

    def open_calculations(self, instance):
        self.manager.current = 'calc'
class CalcScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source='background.webp', allow_stretch=True, keep_ratio=False))
        self.layout = FloatLayout()

        calculations = [
            "Калькулятор второго закона Ньютона", "Калькулятор закона Ома", "Закон Гука (нахождение силы упругости)",
            "Расчёт кинетической энергии", "Расчёт потенциальной энергии", "Закон сохранения механической энергии"
        ]

        self.add_buttons(calculations)

        self.back_button = CustomButton(
            text='Назад',
            size_hint=(None, None),
            size=(Window.width * 0.3, Window.height * 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.05}
        )
        self.back_button.bind(on_release=self.return_to_menu)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def add_buttons(self, calculations):
        button_width = (Window.width - 4 * 5) / 3
        button_height = Window.height * 0.12

        for i, calc in enumerate(calculations):
            button = CustomButton(
                text=calc,
                size_hint=(None, None),
                size=(button_width, button_height),
                pos_hint={'center_x': ((i % 3) * (button_width + 5) + button_width / 2) / Window.width, 
                          'top': 0.9 - (i // 3) * (button_height / Window.height + 0.05)}
            )
            button.bind(on_release=self.open_newton_calc_screen if calc == "Калькулятор второго закона Ньютона" else self.dummy)
            self.layout.add_widget(button)

    def open_newton_calc_screen(self, instance):
        self.manager.current = 'newton_calc'

    def dummy(self, instance):
        # Заглушка для кнопок
        pass

    def return_to_menu(self, instance):
        self.manager.current = 'menu'


class NextScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source='background.webp', allow_stretch=True, keep_ratio=False))
        self.layout = FloatLayout()

        calculations = [
            "Расчет давления", "Расчет частоты волн", "Дополнительные расчеты 3",
            "Дополнительные расчеты 4", "Дополнительные расчеты 5", "Дополнительные расчеты 6"
        ]

        self.add_buttons(calculations)

        self.back_button = CustomButton(
            text='Назад',
            size_hint=(None, None),
            size=(Window.width * 0.3, Window.height * 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.05}
        )
        self.back_button.bind(on_release=self.return_to_calc)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def add_buttons(self, calculations):
        button_width = (Window.width - 4 * 5) / 3
        button_height = Window.height * 0.12

        for i, calc in enumerate(calculations):
            button = CustomButton(
                text=calc,
                size_hint=(None, None),
                size=(button_width, button_height),
                pos_hint={'center_x': ((i % 3) * (button_width + 5) + button_width / 2) / Window.width, 
                          'top': 0.9 - (i // 3) * (button_height / Window.height + 0.05)}
            )
            self.layout.add_widget(button)

    def return_to_calc(self, instance):
        self.manager.current = 'calc'

class NewtonCalcScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source='background.webp', allow_stretch=True, keep_ratio=False))
        self.layout = FloatLayout()
        self.current_calculation_type = None
        self.popups = []  # Список

        options = ["Рассчитать силу", "Рассчитать массу", "Рассчитать ускорение"]
        for i, option in enumerate(options):
            btn = CustomButton(
                text=option,
                size_hint=(None, None),
                size=(Window.width * 0.6, Window.height * 0.1),
                pos_hint={'center_x': 0.5, 'center_y': 0.6 - i * 0.15}
            )
            btn.bind(on_release=lambda x, option=option: self.show_input_dialog(option))
            self.layout.add_widget(btn)

        self.back_button = CustomButton(
            text='Назад',
            size_hint=(None, None),
            size=(Window.width * 0.3, Window.height * 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.1}
        )
        self.back_button.bind(on_release=self.return_to_calc_screen)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def show_input_dialog(self, calculation_type):
        self.current_calculation_type = calculation_type
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        input1 = TextInput(hint_text='Введите первое значение', multiline=False)
        input2 = TextInput(hint_text='Введите второе значение', multiline=False)

        if calculation_type == "Рассчитать силу":
            input1.hint_text = 'Введите массу (кг)'
            input2.hint_text = 'Введите ускорение (м/с²)'
        elif calculation_type == "Рассчитать массу":
            input1.hint_text = 'Введите силу (Н)'
            input2.hint_text = 'Введите ускорение (м/с²)'
        elif calculation_type == "Рассчитать ускорение":
            input1.hint_text = 'Введите силу (Н)'
            input2.hint_text = 'Введите массу (кг)'

        popup_layout.add_widget(input1)
        popup_layout.add_widget(input2)
        
        calculate_button = Button(text='Рассчитать')
        calculate_button.bind(on_release=lambda x: self.calculate(calculation_type, input1.text, input2.text))
        popup_layout.add_widget(calculate_button)

        back_button = Button(text='Назад')
        back_button.bind(on_release=lambda x: self.close_all_popups())
        popup_layout.add_widget(back_button)

        popup = Popup(title='Введите данные', content=popup_layout, size_hint=(0.9, 0.5))
        popup.open()
        self.popups.append(popup)

    def calculate(self, calculation_type, val1, val2):
        try:
            val1 = float(val1)
            val2 = float(val2)
        except ValueError:
            self.show_error_popup('Неверный ввод')
            return

        if calculation_type == "Рассчитать силу":
            result = val1 * val2
            self.show_result(f'Рассчитанная сила равна: {result} Н')
        elif calculation_type == "Рассчитать массу":
            result = val1 / val2
            self.show_result(f'Рассчитанная масса: {result} кг')
        elif calculation_type == "Рассчитать ускорение":
            result = val1 / val2
            self.show_result(f'Рассчитанное ускорение: {result} м/с²')

    def show_error_popup(self, message):
        error_popup = Popup(title='Ошибка', content=Label(text=message), size_hint=(0.8, 0.3))
        error_popup.open()
        self.popups.append(error_popup)

    def show_result(self, message):
        result_label = Label(text=message)
        current_popup = self.popups[-1]
        current_popup.content.clear_widgets()
        current_popup.content.add_widget(result_label)

        recalculate_button = Button(text='Ввести другое значение')
        recalculate_button.bind(on_release=lambda x: self.show_input_dialog(self.current_calculation_type))
        current_popup.content.add_widget(recalculate_button)

        close_button = Button(text='Закрыть')
        close_button.bind(on_release=lambda x: self.close_all_popups())
        current_popup.content.add_widget(close_button)

    def close_all_popups(self):
        while self.popups:
            popup = self.popups.pop()
            popup.dismiss()

    def return_to_calc_screen(self, instance):
        self.close_all_popups()
        self.manager.current = 'calc'



class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(CalcScreen(name='calc'))
        sm.add_widget(NextScreen(name='next_screen'))
        sm.add_widget(NewtonCalcScreen(name='newton_calc'))
        return sm

if __name__ == '__main__':
    MyApp().run()
