import os
import time
import threading
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonText
from plyer import notification

import arabic_reshaper
from bidi.algorithm import get_display

# 1. تسجيل خط ويندوز الافتراضي (Arial) ليدعم العربية في التطبيق بالكامل
arial_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'arial.ttf')
LabelBase.register(name=DEFAULT_FONT, fn_regular=arial_path)

def fix_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

class MotivationApp(MDApp):
    def build(self):
        screen = MDScreen()
        
        self.label = MDLabel(
            text=fix_arabic("مُحفّز ANSER يعمل في الخلفية"),
            halign="center",
            font_size="20sp",
            pos_hint={"center_y": 0.6}
        )
        
        # زر لبدء تشغيل الإشعارات الدورية
        self.btn = MDButton(
            MDButtonText(text=fix_arabic("ابدأ الإشعارات التحفيزية")),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.start_notifications_thread
        )
        
        screen.add_widget(self.label)
        screen.add_widget(self.btn)
        return screen

    def start_notifications_thread(self, instance):
        self.label.text = fix_arabic("تم تفعيل الإشعارات بنجاح!")
        self.btn.disabled = True
        
        # تشغيل حلقة الإشعارات في الخلفية
        threading.Thread(target=self.send_periodic_notification, daemon=True).start()

    def send_periodic_notification(self):
        quotes = [
            "تقدم بخطوات ثابتة نحو أهدافك.. أنت قادر على إنجاز الأفضل اليوم!",
            "الاستمرارية هي سر التفوق والنجاح.",
            "اجعل كل يوم خطوة حقيقية تقربك لطموحاتك.",
            "لا تقلق بشأن السرعة، المهم هو الاتجاه الصحيح."
        ]
        
        i = 0
        while True:
            time.sleep(10)  # زمن الانتظار (10 ثوانٍ للاختبار)
            current_quote = quotes[i % len(quotes)]
            
            notification.notify(
                title=fix_arabic("إشعار تحفيزي 💡"),
                message=fix_arabic(current_quote),
                app_name=fix_arabic("ANSER Motivation"),
                timeout=10
            )
            i += 1

if __name__ == "__main__":
    MotivationApp().run()