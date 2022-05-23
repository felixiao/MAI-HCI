from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel

import stylesheet as st


class FeatureTabs(TabbedPanel):
    def switch_tab(self, clicked_tab):
        for tab in self.tab_list:
            if tab == clicked_tab:
                tab.font_size = st.H2_FONT_SIZE
            else:
                tab.font_size = st.H3_FONT_SIZE

    def generate_from_scratch(self):
        input_str = self.ids.gen_number.text
        try:
            number = int(input_str)
            print(number)
        except ValueError:
            self.ids.gen_number.text = "Please input a whole number"


class KiviUi(BoxLayout):
    pass


class KiviUiApp(App):
    def build(self):
        return KiviUi()


if __name__ == '__main__':
    Builder.load_file('kivi_ui.kv')
    KiviUiApp().run()
