import random
import string

import util

from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

from plot import MeshLinePlot

user = str()
texts = dict()
c_texts = dict()
t_num = int()


class ScreenManagement(ScreenManager):
    now = False

    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        Clock.schedule_interval(lambda x: self.switch(now=ScreenManagement.now), 0)

    screen_management = ObjectProperty(None)

    def on_screen_management(self, *args):
        pass

    def switch(self, *args, now):
        if now:
            self.screen_management.current = 'check_screen'
            ScreenManagement.now = False


class LoginScreen(Screen):
    def login(self):
        if self.ids.login_text.text == '':
            self.ids.login_text.text = 'admin'
        with open('users.txt', 'r') as f:
            users = [s.split('  ') for s in f][0]
        if not users.__contains__(self.ids.login_text.text):
            with open('users.txt', 'a') as f:
                f.write('  ' + self.ids.login_text.text)
        globals()['user'] = self.ids.login_text.text


class TasksScreen(Screen):
    def on_leave(self, *args):
        ScreenManagement.done = False


class SuperScreen(Screen):
    text = {}
    labels = {}

    def on_pre_enter(self, *args):
        Clock.schedule_interval(self.ids.time_label.update, 1)
        self.ids.time_label.text = '10'

    def on_leave(self, *args):
        for child in self.children[0].children[:]:
            if child != self.ids.time_label:
                self.children[0].remove_widget(child)


class Task1(SuperScreen):
    def on_enter(self, *args):
        globals()['t_num'] = 1
        for i in range(10):
            text = str(random.randint(0, 100))
            globals()['texts'][i] = text
            self.ids.task_1_grid.add_widget(ColoredLabel(text=text), 1)
        self.ids.task_1_grid.add_widget(Label(), 1)
        self.ids.task_1_grid.add_widget(Label(), 1)


class Task2(SuperScreen):
    def on_enter(self, *args):
        globals()['t_num'] = 2
        for i in range(10):
            text = random.choice(string.ascii_lowercase)
            globals()['texts'][i] = text
            self.ids.task_2_grid.add_widget(ColoredLabel(text=text), 1)

        self.ids.task_2_grid.add_widget(Label(), 1)
        self.ids.task_2_grid.add_widget(Label(), 1)


class Task3(SuperScreen):
    def on_enter(self, *args):
        globals()['t_num'] = 3
        for i in range(10):
            text = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.choice(range(1, 6))))
            globals()['texts'][i] = text
            self.ids.task_3_grid.add_widget(ColoredLabel(text=text), 1)
        self.ids.task_3_grid.add_widget(Label(), 1)
        self.ids.task_3_grid.add_widget(Label(), 1)


class Task4(SuperScreen):
    def on_enter(self, *args):
        globals()['t_num'] = 4
        for i in range(10):
            with open('words.txt', 'r') as f:
                lines = f.readlines()
                text = random.choice(lines)[:-1]
                globals()['texts'][i] = text
                self.ids.task_4_grid.add_widget(ColoredLabel(text=text), 1)
        self.ids.task_4_grid.add_widget(Label(), 1)
        self.ids.task_4_grid.add_widget(Label(), 1)


class CheckScreen(Screen):
    text_inputs = {}
    empty_labels = {}

    def on_enter(self, *args):
        for i in range(10):
            self.text_inputs[i] = TextInput(multiline=False)
            self.text_inputs[i].bind(text=self.on_text_change)
        for i in range(10):
            self.ids.check_screen.add_widget(self.text_inputs[i], 1)

        self.ids.check_screen.add_widget(Label(), 1)
        self.ids.check_screen.add_widget(Label(), 1)

    def on_button(self, *args):
        values = list(texts.values())
        i = 0
        for v in c_texts.values():
            if v in values:
                i += 1
                values.remove(v)

        util.write_json(user=user, score=i, t_num=t_num)

    def on_text_change(self, instance, value):
        for d_key, d_value in self.text_inputs.items():
            if d_value == instance:
                globals()['c_texts'][d_key] = value

    def on_leave(self, *args):
        for child in self.children[0].children[:]:
            if child != self.ids.check_button:
                self.children[0].remove_widget(child)


class ChartScreen(Screen):
    def on_enter(self, *args):
        graphs = {1: self.ids.graph_1, 2: self.ids.graph_2, 3: self.ids.graph_3, 4: self.ids.graph_4}
        for i in range(1, 5):
            plot = MeshLinePlot(color=[1, 0, 0, 1])
            graphs[i].xlabel = str(i)
            points = []
            j = 0
            for score in util.get_user_score(user=user):
                if score[1] == i:
                    points.append((j, score[0]))
                    j += 1
            plot.points = points
            graphs[i].xmax = len(plot.points)
            graphs[i].add_plot(plot)


class ColoredLabel(Label):
    def randomrgba(self, l):
        rgba = []
        for i in range(3):
            rgba.append(random.randint(0, 255) / 255)
        rgba.append(l)
        return rgba

    def update_text(self, text):
        self.text = text


class TimeLabel(Label):
    count_down = 10

    def update(self,  *args):
        current = int(self.text)
        self.text = str(current - 1)
        if self.text == '0':
            Clock.unschedule(self.update)
            ScreenManagement.now = True
