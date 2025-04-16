import sys
import os
import sounddevice as sd
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from character_tts import inference
from gpt_api import API
import random
import parse_settings

# settings.yaml 파일 경로
# PARSE_SETTINGS_FILE_PATH = "settings.yaml"

class ApiThread(QThread):
    finished = pyqtSignal(str)  # API 호출 완료 시 응답 데이터를 전달할 시그널

    def __init__(self, user_text, holo_api):
        super().__init__()
        self.user_text = user_text
        self.holo_api = holo_api

    def run(self):
        response = self.holo_api.get_serifu_from_message(self.user_text)
        self.finished.emit(response)

class VisualNovelWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = parse_settings.parse_settings()

        os.environ["OPENAI_API_KEY"] = self.settings['API_SETTINGS']['openai_api_key']

        self.holo_api = API(self.settings['API_SETTINGS']['openai_assistant_key'])  
        self.hps, self.net_g = inference.load_model_and_config(
            self.settings['APPLICATION_SETTINGS']['config_path'],
            self.settings['APPLICATION_SETTINGS']['weight_path']
        )

        if self.settings['EMOTION_SETTINGS']['enabled']:
            try:
                import MeCab
            except:
                raise ImportError("MeCab is not installed. Please install MeCab to use emotion detection.")

        self.initUI()

    def _split_jpn(self, message):
        return message.split(self.settings['APPLICATION_SETTINGS']['lang_delimiter'])[0]

    def _split_kr(self, message):
        return "".join(message.split(self.settings['APPLICATION_SETTINGS']['lang_delimiter'])[1:])

    def initUI(self):
        # 전체 레이아웃
        main_layout = QVBoxLayout()
        
        self.background_label = QLabel(self)

        image_path = os.path.join(os.getcwd(), self.settings['EMOTION_SETTINGS']['default_img_path'])
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print(f"Error: Cannot load image from {image_path}")
        else:
            pixmap = pixmap.scaled(1280, 720, Qt.KeepAspectRatioByExpanding)
            self.background_label.setPixmap(pixmap)

        self.background_label.setAlignment(Qt.AlignCenter)

        overlay_layout = QVBoxLayout(self.background_label)
        overlay_layout.setContentsMargins(10, 10, 10, 10)

        font_id = QFontDatabase.addApplicationFont(self.settings['APPLICATION_SETTINGS']['font_path'])
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        font = QFont(font_families[0], 16)
        font_name = QFont(font_families[0], 18)
        # font = QFont("Pretendard JP", 16)
        # font_name = QFont("Pretendard JP", 18)

        self.character_name_label = QLabel(f"{self.settings['CHARACTER_SETTINGS']['character_name']} | {self.settings['CHARACTER_SETTINGS']['where_character_from']}", self)
        self.character_name_label.setFont(font_name)
        self.character_name_label.setStyleSheet("""
            color: white;
            background-color: rgba(0, 0, 0, 150);
            padding: 5px;
            border-radius: 5px;
        """)
        # self.character_name_label.setFixedWidth(275)
        self.character_name_label.setFixedHeight(40)

        self.dialogue_box = QTextEdit(self)
        self.dialogue_box.setReadOnly(True)
        self.dialogue_box.setFont(font)
        self.dialogue_box.setStyleSheet("""
            background-color: rgba(0, 0, 0, 100);
            color: white;
            border-radius: 15px;
            padding: 15px;
            font-size: 25px;
        """)
        self.dialogue_box.setFixedHeight(150)

        # 사용자 입력과 음성 인식 버튼을 담을 수평 레이아웃
        input_layout = QHBoxLayout()

        # 사용자 입력창을 캐릭터 이미지 위에 반투명하게 설정
        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Enter your message...")
        self.user_input.setFixedHeight(30)
        self.user_input.setFont(font)
        self.user_input.setStyleSheet("""
            background-color: rgba(255, 255, 255, 150);
            color: black;
            border-radius: 10px;
            padding: 5px;
            font-size: 22px;
        """)
        self.user_input.returnPressed.connect(self.processUserInput)

        # 입력창과 음성 인식 버튼을 수평 레이아웃에 추가
        input_layout.addWidget(self.user_input)
        # input_layout.addWidget(self.voice_recognition_button)

        # 빈 공간 추가 -> 위쪽에 공간을 만들어서 레이아웃이 아래로 밀리도록 설정
        overlay_layout.addStretch(1)
        # 캐릭터명을 이미지 위에 추가
        overlay_layout.addWidget(self.character_name_label)

        # 대화창을 overlay_layout의 하단에 추가
        overlay_layout.addWidget(self.dialogue_box)
        overlay_layout.addLayout(input_layout)
        if self.settings['APPLICATION_SETTINGS']['print_tts_text']:
            self.jpn_label = QLabel(self)
            self.jpn_label.setFont(QFont("Arial", 12))  # 작은 폰트 크기
            self.jpn_label.setStyleSheet("""
                color: white;
                background-color: rgba(0, 0, 0, 100);
                padding: 3px;
                border-radius: 5px;
            """)
            self.jpn_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.jpn_label.move(10, 10)  # 화면 왼쪽 상단에 배치

        # 메인 레이아웃에 배경과 그 위에 겹친 대화창을 추가
        main_layout.addWidget(self.background_label)

        self.setLayout(main_layout)
        self.setWindowTitle(self.settings['CHARACTER_SETTINGS']['character_name'])
        self.setGeometry(100, 100, 1280, 720)

        # 창 크기 조절 비활성화
        self.setFixedSize(1280, 720)

        # 로딩 애니메이션을 위한 타이머 설정
        self.loading_timer = QTimer(self)
        self.loading_timer.timeout.connect(self.update_loading_message)
        self.loading_dots = 0

        # 타이핑 효과를 위한 변수 설정
        self.typing_index = 0
        self.typing_text = ""
        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self.update_typing_effect)

    def change_img_by_emotion(self, msg):
        import emotion_detection
        emotion_analyzer = emotion_detection.get_emotion_analyzer()
        emotion = emotion_detection.emotion_detection(emotion_analyzer, msg)
        print("Emotion Detection Result : ", emotion)
        emotion = random.choice(emotion)

        emotion_dict = {
            'yasu': self.settings['EMOTION_SETTINGS']['yasu_img_path'],
            'yorokobi': self.settings['EMOTION_SETTINGS']['yorokobi_img_path'],
            'suki': self.settings['EMOTION_SETTINGS']['suki_img_path'],
            'iya': self.settings['EMOTION_SETTINGS']['iya_img_path'],
            'takaburi': self.settings['EMOTION_SETTINGS']['takaburi_img_path'],
            'odoroki': self.settings['EMOTION_SETTINGS']['odoroki_img_path'],
            'haji': self.settings['EMOTION_SETTINGS']['haji_img_path'],
            'aware': self.settings['EMOTION_SETTINGS']['aware_img_path'],
            'ikari': self.settings['EMOTION_SETTINGS']['ikari_img_path'],
            'kowa': self.settings['EMOTION_SETTINGS']['kowa_img_path'],
            'default': self.settings['EMOTION_SETTINGS']['default_img_path'],
        }

        if emotion not in emotion_dict.keys():
            emotion = 'default'
        image_path = os.path.join(os.getcwd(), emotion_dict[emotion])
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print(f"Error: Cannot load image from {image_path}")
        else:
            # 이미지 크기를 1280x720으로 조정
            pixmap = pixmap.scaled(1280, 720, Qt.KeepAspectRatioByExpanding)
            self.background_label.setPixmap(pixmap)

    def processUserInput(self):
        # 사용자의 입력을 가져옴
        user_text = self.user_input.text()
        if user_text:
            # 대화창에 "호로가 생각중..." 텍스트 삽입 및 타이머 시작
            self.show_loading_message()

            # 별도 스레드에서 API 호출을 수행
            self.api_thread = ApiThread(user_text, self.holo_api)
            self.api_thread.finished.connect(self.handle_api_response)
            self.api_thread.start()

    def handle_api_response(self, response):
        response_jpn_text = self._split_jpn(response)
        response_kr_text = self._split_kr(response)

        # Emotion Detection and change img
        if self.settings['EMOTION_SETTINGS']['enabled']:
            self.change_img_by_emotion(response_jpn_text)
        self.play_sound_from_array(inference.inference_tts(self.hps, self.net_g, response_jpn_text))
        self.hide_loading_message()

        # 대화창에 글자 한자씩 출력하는 타이핑 효과 시작
        self.typing_text = response_kr_text
        self.typing_index = 0
        self.dialogue_box.clear()  # 대화창 초기화
        self.user_input.clear()
        # self.voice_recognition_button.setText("음성 인식 켜기")
        self.typing_timer.start(40)  # 50ms마다 한 글자씩 추가

        if self.settings['APPLICATION_SETTINGS']['print_tts_text']:
            self.jpn_label.setText(response_jpn_text)  # 일본어 텍스트 레이블에 설정
            self.jpn_label.adjustSize()

    def update_typing_effect(self):
        if self.typing_index < len(self.typing_text):
            self.dialogue_box.setText(self.typing_text[:self.typing_index + 1])
            self.typing_index += 1
        else:
            self.typing_timer.stop()
        

    def show_loading_message(self):
        self.loading_dots = 0
        self.dialogue_box.clear()
        self.dialogue_box.append(f"{self.settings['CHARACTER_SETTINGS']['character_name']} {self.settings['CHARACTER_SETTINGS']['character_thinking_text']}...")
        self.loading_timer.start(500)  # 0.5초마다 타이머 발생

    def update_loading_message(self):
        self.loading_dots = (self.loading_dots + 1) % 6  # 점이 3개를 넘지 않게 제한
        loading_text = f"{self.settings['CHARACTER_SETTINGS']['character_name']} {self.settings['CHARACTER_SETTINGS']['character_thinking_text']}" + "." * self.loading_dots
        self.dialogue_box.clear()
        self.dialogue_box.append(loading_text)

    def hide_loading_message(self):
        self.loading_timer.stop()
        self.dialogue_box.clear()

    def play_sound_from_array(self, audio_data, sample_rate=22050):
        sd.play(audio_data, sample_rate)

def main():
    app = QApplication(sys.argv)
    window = VisualNovelWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
