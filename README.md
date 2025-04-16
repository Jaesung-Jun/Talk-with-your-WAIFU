<p align="center">
    <img src="assets/icon.png" width="512" />
</p>

# Talk with your WAIFU

## Introduction
### Talk with your WAIFU v0.1.

[ENGLISH README](./README_en.md)

이 프로젝트는 그냥 재미로만 만들어 졌습니다!

이 프로젝트는 [VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning) 레포지토리를 매우 많이 참고하였고, 수정된 [VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning)의 코드를 사용했습니다. [VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning)에 들어가서 별 한번 찍어주세요!

당신의 최애캐의 목소리를 학습시켜, 디스코드 봇으로 만들거나, PyQT 기반의 UI에서 최애캐와 대화하세요.

### 데모 영상

https://github.com/user-attachments/assets/a57e7a35-1b89-474a-92bd-3ff491ec979c
Youtube : https://www.youtube.com/watch?v=_wBLcubwFF8

## 주요 기능
### 1. ChatGPT 연동
ChatGPT Assistants의 API를 활용하도록 만들어 졌습니다.
GPT Assistants 문서를 참고하여, API를 미리 준비해주세요. -> https://platform.openai.com/docs/assistants/overview

GPT Assistants가 당신의 최애캐와 비슷한 말투로 대화하도록 설정 하는것이 매우 중요합니다.
캐릭터의 다양한 대사집/설정 정보 등을 GPT Assistants에 제공하면, 캐릭터의 말투를 잘 따라하는 API가 완성됩니다.

GPT Assistants가 대사를 출력하게 할때, 원문과 번역문을 구별자로 구분 되어 함께 출력할 수 있도록 해주세요.
```
예시 1 : 貴方が好きです。付き合ってください。[구별자]당신을 좋아합니다. 저랑 사귀어 주세요.
예시 2 : あの、私！君に伝えたいことがあるの！[구별자]저기, 나, 너에게 전해야 할 말이 있어!
```

### 2. TTS
[VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning) 레포지토리를 참고하여 만들어진 코드를 기반으로, 학습된 Weight와 Config파일만 있으면 음성을 출력할 수 있게 만들었습니다.


### 3. 일본어 감정 인식 기능
[pymlask](https://github.com/ikegami-yukino/pymlask) 라이브러리를 이용하여 일본어 감정 인식 기능을 구현했습니다! MeCab도 같이 설치하여 사용하세요.

## 사용 기술
- Python
- OpenAI GPT Assistants
- 음성 합성 : [VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning)
- PyQT5
- discord.py (선택)

## 실행 방법

### 1. 당신의 최애캐의 목소리를 학습시키세요.
[VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning)의 README를 참고하세요.
위 프로젝트의 README를 참고하여 캐릭터를 학습시켰으면, 학습된 Weight파일과 Config 파일을 미리 저장해두세요.CPU로도 빠르게 추론 되는 것을 확인하였습니다. 노트북으로도 실행이 될것입니다! (아마도)

### 2. 파이썬 패키지 들을 설치해주세요.
아래 명령어를 사용하여 필요한 파이썬 패키지를 선택해주세요. (가상 환경을 추천합니다.)
```bash
pip install -r requirements.txt
```

### 3. settings.yaml을 수정하세요.
settings_default.yaml 파일을 당신의 환경에 맞게 수정한 후, settings.yaml로 파일명을 변경하세요.
아래는 settings_default.yaml의 각 설정값의 설명 입니다.
```yaml
#########################################################
# Settings for the application
#########################################################
APPLICATION_SETTINGS:
  - weight_path: "weights/WEIGHT_PATH_HERE.pth" # VIT-fast-fine-tuning 레포지토리를 활용하여 학습시킨 Weight의 경로를 넣어주세요.
  - config_path: "weights/TTS_CONFIG_JSON_FILE.json" # VIT-fast-fine-tuning 레포지토리에서 목소리를 학습시킬 때 나온 config 파일의 경로를 적어주세요.
  - font_path: "font/FONT_FILE.ttf" # 사용할 폰트의 폰트 파일 경로를 선택합니다.
  - lang_delimiter: "\n" # 원문과 번역문을 구분하는 구별자를 선택합니다 (기본값 : 줄바꿈 문자)
  - print_tts_text: False # TTS에서 나온 원문 메세지를 UI 상단에 출력하려면 True로 변경해주세요.

API_SETTINGS:
  - openai_api_key: "" # GPT Assistants API 키를 적어주세요.
  - openai_assistant_key: "" # Asisstants Key를 적어주세요.

EMOTION_SETTINGS: # 11개의 감정을 지원합니다. 각 감정이 인식 되었을때 출력될 이미지의 경로를 각각 입력해주세요.
  - default_img_path: "img/default.jpg" # 기본 이미지는 감정 인식을 꺼도 필요합니다. 설정해주세요.
  - enabled: False # Enable하려면 MeCab과 mlask를 설치하세요.
  - yasu_img_path: "img/yasu.jpg" # 평온한
  - yorokobi_img_path: "img/yorokobi.jpg" # 즐거운
  - suki_img_path: "img/suki.jpg" # 좋아하는
  - iya_img_path: "img/iyaa.jpg" # 싫어하는
  - takaburi_img_path: "img/takaburi.jpg" # 신난
  - odoroki_img_path: "img/odoroki.jpg" # 놀란
  - haji_img_path: "img/haji.jpg" # 부끄러운
  - aware_img_path: "img/aware.jpg" # 가여운
  - ikari_img_path: "img/ikari.jpg" # 화난
  - kowa_img_path: "img/kowa.jpg" # 무서운

CHARACTER_SETTINGS:
  - character_name: "horo, the wise wolf" # 캐릭터 이름을 설정해주세요.
  - where_character_from: "Spice and Wolf" # 캐릭터가 등장한 작품 명을 적어주세요.
  - character_thinking_text: " is thinking" # API로부터 데이터를 불러오고, TTS 모델을 실행할때 출력될 메세지를 적어주세요.

DISCORD_SETTINGS:
  - bot_token: "" # 디스코드 봇으로 실행하고 싶으면 봇 토큰을 설정해주세요.
  - command_prefix: "!" # 커맨드 접두사를 적어주세요.
  - command: "speak" # 커맨드를 적어주세요 (기본 설정으로는 !speak [메세지] 가 됩니다.)
```
### 3. 실행
UI를 실행하려면 아래 명령어를 입력해주세요.
```bash
python ui.py
```
### 4. (선택) Discord Bot
디스코드 봇으로 실행하려면 아래 명령어를 입력해주세요.
```bash
pip install discord.py==2.4.0
python discord_ui.py
```

### License
Apache-2.0 License.