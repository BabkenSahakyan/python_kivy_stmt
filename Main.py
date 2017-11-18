#uncomment for windows OS
#import os
#os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

import kivy

kivy.require('1.9.0')
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.lang import Builder
import tasks

presentation = Builder.load_file('lab.kv')


class LabApp(App):
    def build(self):
        return presentation


lab = LabApp()

if __name__ == '__main__':
    lab.run()
