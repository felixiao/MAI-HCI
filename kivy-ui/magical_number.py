from abc import ABC, abstractmethod

from kivy.uix.boxlayout import BoxLayout


class MagicalNumberSubscriber(ABC):
    @abstractmethod
    def update(self, number: int):
        pass


class MagicalNumberPublisher(ABC):
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber: MagicalNumberSubscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: MagicalNumberSubscriber):
        self.subscribers.remove(subscriber)

    def notify(self, number: int):
        for subscriber in self.subscribers:
            subscriber.update(number)


class MetaMagicalNumber(type(BoxLayout), type(MagicalNumberPublisher)):
    pass


class MagicalNumber(BoxLayout, MagicalNumberPublisher, metaclass=MetaMagicalNumber):
    def clicked(self):
        input_str = self.ids.gen_number.text
        try:
            number = int(input_str)
            self.notify(number)
        except ValueError:
            self.ids.gen_number.text = "Please input a whole number"
