from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from random import randint, choice


class PartyColorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = 0.8
        self.smoothness = 0.08
        self.color_count = 6
        self.palette_name = "PARTY"
        self.mode = "RANDOM"
        self.running = True
        self.current = [1.0, 0.0, 0.4]
        self.target = [0.0, 0.8, 1.0]

    def build(self):
        root = BoxLayout(orientation="vertical")

        with root.canvas.before:
            self.bg_color = Color(*self.current, 1)
            self.bg_rect = Rectangle(pos=root.pos, size=root.size)

        root.bind(pos=self._update_bg, size=self._update_bg)

        settings = Button(
            text="⚙",
            size_hint=(None, None),
            size=(60, 60),
            pos_hint={"right": 1},
        )
        settings.bind(on_release=lambda *_: self.open_settings())

        root.add_widget(Label())
        root.add_widget(settings)

        Clock.schedule_interval(self.animate, 1 / 60)
        return root

    def _update_bg(self, *_):
        self.bg_rect.pos = self.root.pos
        self.bg_rect.size = self.root.size

    def palette(self):
        if self.palette_name == "RED":
            return [1, 0.05, 0.05]
        if self.palette_name == "BLUE":
            return [0.05, 0.25, 1]
        if self.palette_name == "DARK":
            return [0.03, 0.03, 0.06]
        if self.palette_name == "NEON":
            return [choice([0, 1]), choice([0, 1]), choice([0, 1])]
        return [randint(0, 100) / 100, randint(0, 100) / 100, randint(0, 100) / 100]

    def animate(self, dt):
        if not self.running:
            return

        step = max(0.005, self.smoothness * self.speed)
        for i in range(3):
            self.current[i] += (self.target[i] - self.current[i]) * step

        if max(abs(self.current[i] - self.target[i]) for i in range(3)) < 0.015:
            self.target = self.palette()

        self.bg_color.rgba = (*self.current, 1)

    def open_settings(self):
        box = BoxLayout(orientation="vertical", spacing=8, padding=12)

        box.add_widget(Label(text="Party Color Settings", size_hint_y=None, height=35))

        box.add_widget(Label(text="Speed"))
        speed = Slider(min=0.1, max=3, value=self.speed)
        speed.bind(value=lambda _, v: setattr(self, "speed", v))
        box.add_widget(speed)

        box.add_widget(Label(text="Smoothness"))
        smooth = Slider(min=0.01, max=0.25, value=self.smoothness)
        smooth.bind(value=lambda _, v: setattr(self, "smoothness", v))
        box.add_widget(smooth)

        box.add_widget(Label(text="Color count"))
        count = Slider(min=2, max=12, step=1, value=self.color_count)
        count.bind(value=lambda _, v: setattr(self, "color_count", int(v)))
        box.add_widget(count)

        palette = Spinner(
            text=self.palette_name,
            values=("PARTY", "NEON", "RANDOM", "RED", "BLUE", "DARK"),
            size_hint_y=None,
            height=45,
        )
        palette.bind(text=lambda _, v: setattr(self, "palette_name", v))
        box.add_widget(palette)

        mode = Spinner(
            text=self.mode,
            values=("RANDOM", "SEQUENCE", "ALTERNATE"),
            size_hint_y=None,
            height=45,
        )
        mode.bind(text=lambda _, v: setattr(self, "mode", v))
        box.add_widget(mode)

        status = Label(text="Status: Running", size_hint_y=None, height=35)
        box.add_widget(status)

        pause = Button(text="Pause / Resume", size_hint_y=None, height=50)
        def toggle(_):
            self.running = not self.running
            status.text = "Status: Running" if self.running else "Status: Paused"
        pause.bind(on_release=toggle)
        box.add_widget(pause)

        close = Button(text="Close", size_hint_y=None, height=50)
        box.add_widget(close)

        popup = Popup(
            title="Party Color",
            content=box,
            size_hint=(0.9, 0.85),
        )
        close.bind(on_release=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    PartyColorApp().run()
