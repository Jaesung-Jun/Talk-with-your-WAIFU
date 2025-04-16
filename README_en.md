<p align="center">
    <img src="assets/icon.png" width="512" />
</p>

# Talk with your WAIFU

## Introduction
### Talk with your WAIFU v0.1.

This project was created just for fun!

This project is heavily based on the [VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning) repository, and uses the modified code from [VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning). Please consider starring [VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning)!

Train your favorite character's voice and interact with them via a Discord bot or a PyQT-based UI.

### Demo Video

https://github.com/user-attachments/assets/a57e7a35-1b89-474a-92bd-3ff491ec979c  
Youtube : https://www.youtube.com/watch?v=_wBLcubwFF8

## Features
### 1. GPT Assistants Integrations
This project is designed to work with the ChatGPT Assistants API.  
Please refer to the GPT Assistants documentation and prepare the API in advance. -> https://platform.openai.com/docs/assistants/overview

It is very important to configure the GPT Assistant to speak in a tone similar to your favorite character.  
If you provide a rich set of character lines and background settings to the Assistant, it can emulate the character's speech style more naturally.

When GPT Assistants generate lines, make sure it outputs the original and the translation separated by a delimiter.  
```
예시 1 : 貴方が好きです。付き合ってください。[Delimeter]I like you. Please go out with me.
예시 2 : あの、私！君に伝えたいことがあるの！[Delimeter]Um, I! I have something to tell you!
```

### 2. TTS
Based on the code from [VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning), it allows you to generate speech using only the trained weights and config files.

### 3. Japanese Emotion Detection
Implemented Japanese emotion recognition using the [pymlask](https://github.com/ikegami-yukino/pymlask) library!  
Please install MeCab as well to use this feature.

## Technologies
- Python  
- OpenAI GPT Assistants  
- Speech synthesis: [VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning)  
- PyQT5  
- discord.py (optional)  

## How to execute?

### 1. Train your WAIFU's voice
Refer to the README of [VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning).  
Once your character is trained, save the trained weight and config files in advance.  
It has been confirmed to run quickly even on CPU — likely to run on laptops too! (Probably)

### 2. Install Python Requirements
Use the command below to install the required Python packages. (Using a virtual environment is recommended.)
```bash
pip install -r requirements.txt
```

### 3. Modify settings.yaml
Edit the `settings_default.yaml` file to suit your environment, then rename it to `settings.yaml`.  
Below is a description of each setting in `settings_default.yaml`:
```yaml
#########################################################
# Settings for the application
#########################################################
APPLICATION_SETTINGS:
  - weight_path: "weights/WEIGHT_PATH_HERE.pth" # Enter the path of the weight file trained using the VIT-fast-fine-tuning repository.
  - config_path: "weights/TTS_CONFIG_JSON_FILE.json" # Enter the path of the config file generated during training in the VIT-fast-fine-tuning repository.
  - font_path: "font/FONT_FILE.ttf" # Specify the path to the font file to be used.
  - lang_delimiter: "\n" # Select the delimiter to separate original and translated text (default: newline character).
  - print_tts_text: False # Set to True to display the TTS-generated original message at the top of the UI.

API_SETTINGS:
  - openai_api_key: "" # Enter your GPT Assistants API key.
  - openai_assistant_key: "" # Enter your Assistant key.

EMOTION_SETTINGS: # Supports 11 emotions. Specify the image path for each recognized emotion.
  - default_img_path: "img/default.jpg" # The default image is required even if emotion recognition is disabled.
  - enabled: False # To enable, install MeCab and mlask.
  - yasu_img_path: "img/yasu.jpg" # calm
  - yorokobi_img_path: "img/yorokobi.jpg" # happy
  - suki_img_path: "img/suki.jpg" # affectionate
  - iya_img_path: "img/iyaa.jpg" # dislike
  - takaburi_img_path: "img/takaburi.jpg" # excited
  - odoroki_img_path: "img/odoroki.jpg" # surprised
  - haji_img_path: "img/haji.jpg" # embarrassed
  - aware_img_path: "img/aware.jpg" # pitiful
  - ikari_img_path: "img/ikari.jpg" # angry
  - kowa_img_path: "img/kowa.jpg" # scared

CHARACTER_SETTINGS:
  - character_name: "horo, the wise wolf" # Set the character's name.
  - where_character_from: "Spice and Wolf" # Name of the work the character is from.
  - character_thinking_text: " is thinking" # Message to display while fetching data from the API or running TTS.

DISCORD_SETTINGS:
  - bot_token: "" # If you want to run it as a Discord bot, set the bot token.
  - command_prefix: "!" # Set the command prefix.
  - command: "speak" # Set the command (by default, this becomes !speak [message]).
```

### 3. Execute
To launch the UI, run the following command:
```bash
python ui.py
```

### 4. (Optional) Discord Bot
To run as a Discord bot, use the following commands:
```bash
pip install discord.py==2.4.0
python discord_ui.py
```

### License
Apache-2.0 License.