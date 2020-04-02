from os import listdir
import random
import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider

from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from settingsjson import settings_json

class AppLayout(BoxLayout):

    state = False
    start_time = 0
    elapsed_time = 0
    end_time = 0
    pose_count = 0

    def get_limit_toggle(self):
        return int(limittoggle)

    def get_total_poses(self):
        return int(totalposes)

    def get_pose_length(self):
        return poselength

    def get_path_list(self):
        return path_list

    def get_session_list(self):
        return session_list

    def get_image_path(self):
        return active_image_path

    def set_session_list(self):
        global session_list
        session_list = self.get_path_list().copy()

    def get_random_setting(self):
        return int(random_setting)

    def get_random_image(self):
        list_length = len(session_list)
        rand_num = random.randint(0, list_length-1)
        random_image = session_list[rand_num]
        active_image_path = dirpath + '/' + random_image
        self.ids.active_image.source = active_image_path
        result = session_list.pop(rand_num)
        session_list.insert(0, result)

    def change_scale(self, *args):
        self.ids.scatter.scale = min(args[1],args[1])

    def get_loop_setting(self):
        return int(loop_setting)

    def get_sound_setting(self):
        return int(sound_setting)

    def set_start_time(self):
        seconds = {
            '30 seconds': 30,
            '1 Minute': 60,
            '3 Minutes': 180,
            '5 Minutes': 300,
            '10 Minutes': 600,
            '15 Minutes': 900,
            '25 Minutes': 1500
        }

        self.start_time = seconds[self.get_pose_length()]

    def check_image_order(self):
        if self.get_random_setting() == 1:
            self.get_random_image()
        else:
            active_image_path = dirpath + '/' + self.get_session_list()[0]
            self.ids.active_image.source = active_image_path

    def format_seconds(self, num):
        minutes = num//60
        seconds = num%60
        if minutes == 0:
            minutes = '00'
        if seconds < 10:
            seconds = '0{}'.format(str(seconds))
        if self.get_limit_toggle() == 1:
            return '{} of {} | {}:{}'.format(str(self.pose_count+1),str(self.get_total_poses()),str(minutes), str(seconds))
        else:
            return '{}:{}'.format(str(minutes), str(seconds))

    def check_running_time(self):
        if self.state == True:
            time_remaining = self.start_time - self.elapsed_time
            self.ids.settings_button.text = self.format_seconds(time_remaining)
            self.elapsed_time += 1
            if time_remaining == self.end_time + 5:
                global sound_setting
                if self.get_sound_setting() == 1:
                    sound1 = SoundLoader.load('question_004.ogg')
                    sound1.play()
                    Clock.schedule_once(lambda dt: sound1.play(), 1)
                    Clock.schedule_once(lambda dt: sound1.play(), 2)
                    Clock.schedule_once(lambda dt: sound1.play(), 3)
                    Clock.schedule_once(lambda dt: sound1.play(), 4)
            elif time_remaining == self.end_time:
                self.pose_count += 1
                self.elapsed_time = 0
                session_list.pop(0)
                if self.get_limit_toggle() == 1 and self.pose_count == self.get_total_poses():
                    modal_layout = BoxLayout(orientation='vertical', width=self.parent.width, height=self.parent.height)
                    modal_layout.add_widget(Label(text='That was the last pose!', halign='center', valign='middle'))
                    dismiss_button = Button(text='Done', size_hint_y=0.5)
                    modal_layout.add_widget(dismiss_button)
                    pop = Popup(title='Finished set', content=modal_layout,auto_dismiss=False, size_hint=(None,None), size=(self.ids.stencil.width/1.8, self.ids. stencil.height/1.8))
                    dismiss_button.bind(on_press=pop.dismiss)
                    pop.open()
                    self.reset()
                elif len(session_list) > 0:
                    self.check_image_order()
                else:
                    if self.get_loop_setting() == 1:
                        self.set_session_list()
                        self.check_image_order()
                    else:
                        self.reset()
            self.increment_timer()

    def reset(self):
        self.pose_count = 0
        self.ids.start_button.text = 'START'
        self.ids.settings_button.text = 'SETTINGS'
        self.ids.start_button.background_color = (0.2,1,0.8,0.4)
        self.ids.stop_button.disabled = True
        self.ids.settings_button.disabled = False
        self.set_session_list()
        self.check_image_order()
        self.state = False

    def increment_timer(self):
        Clock.schedule_once(lambda dt: self.check_running_time(), 1)

    def start_clicked(self):
        print(self.ids.active_image.size)
        print(Window.size)
        if len(self.get_session_list()) > 0:
            self.set_start_time()
            if self.state == True:
                self.ids.start_button.text = 'RESUME'
                self.ids.start_button.background_color = (0.2,1,0.8,0.4)
                self.state = False
            else:
                self.ids.start_button.text = 'PAUSE'
                self.ids.start_button.background_color = (0.2,0.8,1,0.4)
                self.ids.stop_button.disabled = False
                self.ids.settings_button.disabled = True
                self.state = True
            self.check_running_time()
        else:
            modal_layout = BoxLayout(orientation='vertical', width=self.parent.width, height=self.parent.height)
            modal_layout.add_widget(Label(text='Go to Settings and select a new directory path.', halign='center', valign='middle'))
            dismiss_button = Button(text='Got it', size_hint_y=0.5)
            modal_layout.add_widget(dismiss_button)
            pop = Popup(title='No Images Found', content=modal_layout,auto_dismiss=False, size_hint=(None,None), size=(self.ids.stencil.width/1.8, self.ids.stencil.height/1.8))
            dismiss_button.bind(on_press=pop.dismiss)
            pop.open()

    def stop_clicked(self):
        self.ids.start_button.text = 'START'
        self.ids.start_button.background_color = (0.2,1,0.8,0.4)
        self.ids.stop_button.disabled = True
        self.ids.settings_button.disabled = False
        self.ids.settings_button.text = 'SETTINGS'
        self.elapsed_time = 0
        self.set_session_list()
        self.check_image_order()
        self.state = False

class DrawingTimer(App):
    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        global totalposes
        global poselength
        global dirpath
        global path_list
        global active_image_path
        global random_setting
        global loop_setting
        global session_list
        global sound_setting
        global limittoggle
        totalposes = self.config.get('session', 'totalposes')
        poselength = self.config.get('session', 'poselength')
        dirpath = self.config.get('session', 'dirpath')
        random_setting = self.config.get('session', 'randomtoggle')
        loop_setting = self.config.get('session', 'looptoggle')
        sound_setting = self.config.get('session', 'soundtoggle')
        limittoggle = self.config.get('session', 'limittoggle')
        self.set_path_list()
        self.icon = 'logo.jpg'
        self.title = 'Drawing Timer v0.1'
        Window.minimum_width = 640
        Window.minimum_height = 640
        return AppLayout()

    def set_path_list(self):
        global dirpath
        global path_list
        global session_list
        global active_image_path
        global random_setting
        path_list = []
        file_types = [
            '.jpg',
            '.JPG',
            '.png',
            '.PNG'
        ]
        dir_list = listdir(dirpath)
        for item in dir_list:
            for name in file_types:
                if item.endswith(name):
                    path_list.append(item)
        path_list.sort()
        self.set_image()

    def set_image(self):
        global dirpath
        global path_list
        global session_list
        global active_image_path
        session_list = path_list.copy()
        if len(session_list) > 0:
            if int(random_setting) == 1:
                list_length = len(session_list)
                rand_num = random.randint(0, list_length-1)
                random_image = session_list[rand_num]
                active_image_path = dirpath + '/' + random_image
                result = session_list.pop(rand_num)
                session_list.insert(0, result)
            active_image_path = dirpath + '/' + session_list[0]
        else:
            active_image_path = 'logo.jpg'

    def build_config(self, config):
        config.setdefaults('session', {
            'dirpath': '/',
            'poselength': '5 Minutes',
            'limittoggle': 1,
            'totalposes': 5,
            'randomtoggle': 1,
            'looptoggle': 1,
            'soundtoggle': 1
        })

    def build_settings(self, settings):
        settings.add_json_panel('Session Settings', self.config, data=settings_json)

    def on_config_change(self, config, section, key, value):
        global totalposes
        global poselength
        global dirpath
        global active_image_path
        global random_setting
        global loop_setting
        global sound_setting
        global limittoggle
        if key == 'totalposes':
            totalposes = int(value)
        elif key == 'poselength':
            poselength = value
        elif key == 'dirpath':
            dirpath = value
            self.set_path_list()
            self.set_image()
            self.root.ids.active_image.source = active_image_path
        elif key == 'randomtoggle':
            random_setting = int(value)
            self.set_image()
            self.root.ids.active_image.source = active_image_path
        elif key == 'looptoggle':
            loop_setting = int(value)
        elif key == 'soundtoggle':
            sound_setting = int(value)
        elif key == 'limittoggle':
            limittoggle = int(value)

if __name__ == '__main__':
    DrawingTimer().run()
