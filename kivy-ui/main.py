import os.path

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.tabbedpanel import TabbedPanel

import stylesheet as st
# MagicalNumber and MelodiesList NEEDS TO BE IMPORTED HERE (so kivy finds the class)
from magical_number import MagicalNumber, MagicalNumberSubscriber
from melodies_list import MelodiesList


class GeneratingAnimation(FloatLayout):
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super(GeneratingAnimation, self).__init__(**kwargs)
        anim = Animation(angle=360, duration=2)
        anim += Animation(angle=360, duration=2)
        anim.repeat = True
        anim.start(self)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0


class ComposeFromScratchMeta(type(BoxLayout), type(MagicalNumberSubscriber)):
    pass


class ComposeFromScratch(BoxLayout, MagicalNumberSubscriber, metaclass=ComposeFromScratchMeta):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.ids.magical_number.subscribe(self))
        self.is_generating = False

    def update(self, number: int):
        # TODO: Generate music with AI
        print(f"Composing from scratch with number {number}")
        if not self.is_generating:
            self.add_widget(GeneratingAnimation())
            self.is_generating = True


class MidiFileUpload(StackLayout):
    pass


class ContinueTrackMeta(type(BoxLayout), type(MagicalNumberSubscriber)):
    pass


class ContinueTrack(BoxLayout, MagicalNumberSubscriber, metaclass=ContinueTrackMeta):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.ids.magical_number.subscribe(self))
        Clock.schedule_once(lambda dt: self.ids.midi_upload.ids.upload_button.bind(on_press=self.upload_midi))
        Clock.schedule_once(lambda dt: self.ids.melodies_list.layout_manager.bind(selected_nodes=self.select_melody_from_list))
        self.melody = None

    def select_melody(self, melody):
        self.melody = melody
        self.ids.selected_melody.text = f"Selected song: {melody}"

    def update(self, number: int):
        if self.melody is None:
            self.ids.selected_melody.text = f"You need to select song first!"
        else:
            # TODO: Continue track with AI
            print(f"Continue track {self.melody} with number {number}")

    def select_melody_from_list(self, melodies_list, event):
        if len(melodies_list.selected_nodes) > 0:
            melodies = melodies_list.recycleview.data
            # data in melodies list are dictionaries {'text': [name of the song]}
            self.select_melody(melodies[melodies_list.selected_nodes[0]]['text'])

    def upload_midi(self, button):
        input_str = self.ids.midi_upload.ids.upload_input.text
        if os.path.exists(input_str):
            self.select_melody(input_str)
        else:
            self.ids.midi_upload.ids.upload_input.text = "Please input valid file path"


class AccompanyMelodyMeta(type(BoxLayout), type(MagicalNumberSubscriber)):
    pass


class AccompanyMelody(BoxLayout, MagicalNumberSubscriber, metaclass=AccompanyMelodyMeta):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.ids.magical_number.subscribe(self))
        Clock.schedule_once(lambda dt: self.ids.midi_upload.ids.upload_button.bind(on_press=self.upload_midi))
        Clock.schedule_once(lambda dt: self.ids.melodies_list.layout_manager.bind(selected_nodes=self.select_melody_from_list))
        self.melody = None

    def select_melody(self, melody):
        self.melody = melody
        self.ids.selected_melody.text = f"Selected melody: {melody}"

    def update(self, number: int):
        if self.melody is None:
            self.ids.selected_melody.text = f"You need to select melody first!"
        else:
            # TODO: Accompany melody with AI
            print(f"Accompanying melody {self.melody} with number {number}")

    def select_melody_from_list(self, melodies_list, event):
        if len(melodies_list.selected_nodes) > 0:
            melodies = melodies_list.recycleview.data
            # data in melodies list are dictionaries {'text': [name of the song]}
            self.select_melody(melodies[melodies_list.selected_nodes[0]]['text'])

    def upload_midi(self, button):
        input_str = self.ids.midi_upload.ids.upload_input.text
        if os.path.exists(input_str):
            self.select_melody(input_str)
        else:
            self.ids.midi_upload.ids.upload_input.text = "Please input valid file path"


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
