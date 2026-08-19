from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line

# गोल कोनों वाले बटन्स के लिए क्लास
class RoundedButton(Button):
    def __init__(self, bg_color, fg_color, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.color = fg_color
        self.font_size = 22
        self.bold = True
        self.bg_color = bg_color
        
        with self.canvas.before:
            self.col = Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
            
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# प्राकृतिक नदी-पहाड़ जैसी सुंदर थीम वाला बेस क्लास (बिना किसी इंटरनेट एरर के)
class NatureThemeScreen(Screen):
    def __init__(self, **kwargs):
        super(NatureThemeScreen, self).__init__(**kwargs)
        self.layout_bg = BoxLayout()
        
        with self.layout_bg.canvas.before:
            # प्राकृतिक हरा और नीला (नदी-पहाड़ जैसी गहरी टोन)
            Color(0.05, 0.18, 0.14, 1) 
            self.bg_rect = Rectangle(size=(5000, 5000))
            
        self.layout_bg.bind(size=self.update_bg, pos=self.update_bg)
        self.add_widget(self.layout_bg)

    def update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos


# 1. मुख्य कैलकुलेटर स्क्रीन
class CalculatorScreen(NatureThemeScreen):
    def __init__(self, **kwargs):
        super(CalculatorScreen, self).__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical', padding=12, spacing=8)

        # टॉप हेडर
        header = BoxLayout(size_hint_y=None, height=45, padding=5)
        calc_btn = Button(text='Calculator', font_size=17, bold=True, color=(1,1,1,1), background_color=(0,0,0,0))
        conv_btn = Button(text='Converter', font_size=17, color=(0.7,0.8,0.7,1), background_color=(0,0,0,0))
        conv_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'converter'))
        header.add_widget(calc_btn)
        header.add_widget(conv_btn)
        main_layout.add_widget(header)

        # डिस्प्ले
        self.display = Label(text='0', font_size=65, halign='right', valign='middle', size_hint_y=None, height=140, color=(1, 1, 1, 1))
        self.display.bind(size=self.update_text_width)
        main_layout.add_widget(self.display)

        # कीपैड ग्रिड (संतुलित आकार)
        grid = GridLayout(cols=4, spacing=8, size_hint_y=None, height=400)
        buttons = [
            ('AC', 'op'), ('DEL', 'op'), ('%', 'op'), ('÷', 'op'),
            ('7', 'num'), ('8', 'num'), ('9', 'num'), ('×', 'op'),
            ('4', 'num'), ('5', 'num'), ('6', 'num'), ('-', 'op'),
            ('1', 'num'), ('2', 'num'), ('3', 'num'), ('+', 'op'),
            ('CONV', 'op'), ('0', 'num'), ('.', 'num'), ('=', 'eq')
        ]

        for label, btype in buttons:
            bg = (0.95, 0.5, 0.1, 1) if btype == 'eq' else (0.1, 0.25, 0.2, 0.9)
            fg = (1, 1, 1, 1) if btype == 'eq' else ((0.95, 0.6, 0.2, 1) if btype == 'op' else (1, 1, 1, 1))
            
            btn = RoundedButton(bg_color=bg, fg_color=fg, text=label)
            btn.bind(on_press=self.on_button_press)
            grid.add_widget(btn)

        main_layout.add_widget(grid)
        self.add_widget(main_layout)

    def update_text_width(self, *args):
        self.display.text_size = (self.display.width - 20, self.display.height)

    def on_button_press(self, instance):
        text = instance.text
        current = self.display.text
        if text == 'AC':
            self.display.text = '0'
        elif text == 'DEL':
            self.display.text = current[:-1] if len(current) > 1 and current != '0' else '0'
        elif text == '=':
            try:
                res = str(eval(current.replace('×', '*').replace('÷', '/')))
                self.display.text = res[:-2] if res.endswith('.0') else res
            except:
                self.display.text = 'Error'
        elif text == 'CONV':
            self.manager.current = 'converter'
        else:
            self.display.text = text if current == '0' or current == 'Error' else current + text


# 2. कनवर्टर मेनू स्क्रीन
class ConverterScreen(NatureThemeScreen):
    def __init__(self, **kwargs):
        super(ConverterScreen, self).__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical', padding=12, spacing=8)

        header = BoxLayout(size_hint_y=None, height=45, padding=5)
        calc_btn = Button(text='Calculator', font_size=17, color=(0.7,0.8,0.7,1), background_color=(0,0,0,0))
        calc_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'calculator'))
        conv_btn = Button(text='Converter', font_size=17, bold=True, color=(1,1,1,1), background_color=(0,0,0,0))
        header.add_widget(calc_btn)
        header.add_widget(conv_btn)
        main_layout.add_widget(header)

        grid = GridLayout(cols=3, spacing=10, padding=10)
        categories = ['Currency', 'Length', 'Mass', 'Area', 'Time', 'Data', 'Discount', 'Volume', 'Numeral sys', 'Speed', 'Temperature', 'BMI', 'GST']

        for title in categories:
            btn = RoundedButton(bg_color=(0.1, 0.25, 0.2, 0.9), fg_color=(1, 1, 1, 1), text=title)
            btn.font_size = 15
            btn.bind(on_press=lambda inst, t=title: self.open_detail(t))
            grid.add_widget(btn)

        main_layout.add_widget(grid)
        self.add_widget(main_layout)

    def open_detail(self, title):
        detail_screen = self.manager.get_screen('detail')
        detail_screen.setup_converter(title)
        self.manager.current = 'detail'


# 3. कनवर्टर डिटेल स्क्रीन
class ConverterDetailScreen(NatureThemeScreen):
    def __init__(self, **kwargs):
        super(ConverterDetailScreen, self).__init__(**kwargs)
        
        scroll = ScrollView()
        self.layout = BoxLayout(orientation='vertical', padding=25, spacing=20, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.title_label = Label(text='Converter', font_size=26, bold=True, color=(0.95, 0.6, 0.2, 1), size_hint_y=None, height=50)
        self.layout.add_widget(self.title_label)

        self.val_input = TextInput(hint_text='Enter value...', font_size=22, multiline=False, size_hint_y=None, height=60)
        self.layout.add_widget(self.val_input)

        self.res_label = Label(text='Result: --', font_size=24, color=(1, 1, 1, 1), size_hint_y=None, height=60)
        self.layout.add_widget(self.res_label)

        conv_action_btn = Button(text='Calculate', font_size=20, bold=True, size_hint_y=None, height=55, background_color=(0.95, 0.5, 0.1, 1))
        conv_action_btn.bind(on_press=self.calculate)
        self.layout.add_widget(conv_action_btn)

        back_btn = Button(text='Back to Converter', font_size=18, size_hint_y=None, height=50, background_color=(0.2, 0.3, 0.25, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'converter'))
        self.layout.add_widget(back_btn)

        scroll.add_widget(self.layout)
        self.add_widget(scroll)

    def setup_converter(self, title):
        self.current_type = title
        self.title_label.text = f'{title} Converter'
        self.val_input.text = ''
        self.res_label.text = 'Result: --'

    def calculate(self, instance):
        try:
            val = float(self.val_input.text)
            t = self.current_type
            if t == 'Length':
                res = f'{val * 100} cm / {val / 1000} km'
            elif t == 'Temperature':
                res = f'{(val * 9/5) + 32:.2f} °F'
            elif t == 'Mass':
                res = f'{val * 1000} grams / {val / 1000} kg'
            elif t == 'GST':
                res = f'GST: {val * 0.18:.2f} | Total: {val * 1.18:.2f}'
            elif t == 'Currency':
                res = f'₹ {val} = $ {val / 83:.2f} (Approx)'
            else:
                res = f'Converted Value: {val * 2.54:.2f}'
            self.res_label.text = f'Result: {res}'
        except:
            self.res_label.text = 'Please enter a valid number!'


# 4. मुख्य ऐप मैनेजर
class NatureCalculatorApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CalculatorScreen(name='calculator'))
        sm.add_widget(ConverterScreen(name='converter'))
        sm.add_widget(ConverterDetailScreen(name='detail'))
        return sm

if __name__ == '__main__':
    NatureCalculatorApp().run()
