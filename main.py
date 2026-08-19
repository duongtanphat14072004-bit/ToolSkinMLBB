import os
import shutil
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

# Danh sách skin hiển thị cho khách chọn
SKINS_CONFIG = [
    ("1. Fanny Aspirant", "1"),
    ("2. Fanny Luckybox", "2"),
    ("3. Dyrroth Guile Street Fighter", "3"),
    ("4. Dyrroth HXH", "4"),
    ("5. Dyrroth KOF", "5"),
    ("6. Yin Jujutsu Kaisen", "6"),
    ("7. Yin Attack on Titan", "7")
]

class TanPhatHubApp(App):
    def build(self):
        self.title = "TanPhatHub Skin Manager"
        
        root = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Tiêu đề ứng dụng
        root.add_widget(Label(
            text="🔥 TANPHATHUB MOD SKIN 🔥", 
            font_size=20, size_hint_y=None, height=40, color=(0, 1, 0.8, 1)
        ))
        
        # Nhãn trạng thái
        self.status_lbl = Label(
            text="Trạng thái: Sẵn sàng cài đặt...", 
            font_size=14, size_hint_y=None, height=40, color=(1, 1, 1, 1)
        )
        root.add_widget(self.status_lbl)
        
        # Khung cuộn chứa danh sách nút bấm skin
        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        for skin_name, folder_id in SKINS_CONFIG:
            btn = Button(
                text=skin_name, 
                size_hint_y=None, height=55,
                background_color=(0.15, 0.15, 0.15, 1)
            )
            btn.bind(on_press=lambda instance, fid=folder_id, sname=skin_name: self.install_skin(fid, sname))
            grid.add_widget(btn)
            
        scroll.add_widget(grid)
        root.add_widget(scroll)
        
        return root

    def install_skin(self, folder_id, skin_name):
        self.status_lbl.text = f"Đang cài: {skin_name}..."
        Clock.schedule_once(lambda dt: self._process_copy(folder_id, skin_name), 0.1)

    def _process_copy(self, folder_id, skin_name):
        try:
            # Đường dẫn nguồn bên trong app (nơi chứa các folder 1, 2, 3...)
            source_path = os.path.join(self.user_data_dir, "assets", folder_id)
            if not os.path.exists(source_path):
                # Fallback tìm trong thư mục hiện tại khi chạy test
                source_path = os.path.join("./assets", folder_id)

            # Đường dẫn đích vào thư mục game MLBB trên Android
            target_path = "/storage/emulated/0/Android/data/com.mobile.legends/files/dragon2017/assets/document/"
            
            if not os.path.exists(target_path):
                self.status_lbl.text = "Lỗi: Không tìm thấy thư mục game MLBB!"
                return
                
            if not os.path.exists(source_path):
                self.status_lbl.text = f"Lỗi: Không tìm thấy gói dữ liệu số {folder_id}!"
                return

            # Tiến hành copy ghi đè các thư mục con bên trong (Art, Audio, UI...)
            for item in os.listdir(source_path):
                s_item = os.path.join(source_path, item)
                t_item = os.path.join(target_path, item)
                if os.path.isdir(s_item):
                    if os.path.exists(t_item):
                        shutil.rmtree(t_item)
                    shutil.copytree(s_item, t_item)
            
            self.status_lbl.text = f"Thành công! Đã cài {skin_name}"
        except Exception as e:
            self.status_lbl.text = f"Lỗi: {str(e)}"

if __name__ == '__main__':
    TanPhatHubApp().run()