import os.path

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.tabbedpanel import TabbedPanel

import stylesheet as st
# MagicalNumber and MelodiesList NEEDS TO BE IMPORTED HERE (so kivy finds the class)
from magical_number import MagicalNumber, MagicalNumberSubscriber
from melodies_list import MelodiesList


class ComposeFromScratchMeta(type(BoxLayout), type(MagicalNumberSubscriber)):
    pass


class ComposeFromScratch(BoxLayout, MagicalNumberSubscriber, metaclass=ComposeFromScratchMeta):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.ids.magical_number.subscribe(self))

    def update(self, number: int):
        print(f"Composing from scratch with number {number}")


class AccompanyMelodyMeta(type(BoxLayout), type(MagicalNumberSubscriber)):
    pass


class AccompanyMelody(BoxLayout, MagicalNumberSubscriber, metaclass=AccompanyMelodyMeta):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.ids.magical_number.subscribe(self))
        self.melody = None

    def update(self, number: int):
        if self.melody is None:
            mel_list = self.ids.melodies_list
            self.melody = mel_list.data[mel_list.layout_manager.selected_nodes[0]]
            print(f"Accompanying selected melody {self.melody} with number {number}")
        else:
            print(f"Accompanying given melody {self.melody} with number {number}")

    def upload_midi(self):
        input_str = self.ids.upload_midi.text
        if os.path.exists(input_str):
            self.melody = input_str
            print(input_str)
        else:
            self.ids.upload_midi.text = "Please input valid file path"


class FeatureTabs(TabbedPanel):
    def switch_tab(self, clicked_tab):
        for tab in self.tab_list:
            if tab == clicked_tab:
                tab.font_size = st.H2_FONT_SIZE
            else:
                tab.font_size = st.H3_FONT_SIZE


class KiviUi(BoxLayout):
    pass


class KiviUiApp(App):
    def build(self):
        return KiviUi()


if __name__ == '__main__':
    Builder.load_file('kivi_ui.kv')
    KiviUiApp().run()
