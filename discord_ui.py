import discord
from scipy.io.wavfile import write as write_wav
from character_tts import inference  # Holo TTS 모듈 (TTS 변환 함수 포함)
from gpt_api import API       # API 호출 모듈
import parse_settings
import os

# FFmpeg 옵션 (필요시 볼륨 조절 옵션 추가 가능)
ffmpeg_opts = {'options': '-vn'}
# 디스코드 클라이언트 생성 (모든 인텐트를 활성화)
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = discord.Client(intents=intents)

# 텍스트 분리 함수
def split_jpn(message):
    return message.split("\n")[0]

def split_kr(message):
    return "".join(message.split("\n")[1:])

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    # 봇 자신의 메시지는 무시
    if message.author == client.user:
        return

    content = message.content.strip()
    # "!!호로" 명령어 처리
    if content.startswith(f"{SETTINGS['DISCORD_SETTINGS']['command_prefix']}{SETTINGS['DISCORD_SETTINGS']['command']}"):
        # 명령어 접두어 이후의 텍스트 추출 (예: "너는 무슨생각해?")
        query = content[len(f"{SETTINGS['DISCORD_SETTINGS']['command_prefix']}{SETTINGS['DISCORD_SETTINGS']['command']}"):].strip()
        if not query:
            await message.channel.send("Enter your message after the command!")
            return

        # API 호출하여 응답 문자열 받기
        response = CHAR_API.get_serifu_from_message(query)
        response_jpn_text = split_jpn(response)
        response_kr_text = split_kr(response)

        # TTS 변환: 일본어 텍스트를 Holo의 음성으로 변환 (numpy 배열 형태)
        audio_array = inference.inference_tts(HPS, NET_G, response_jpn_text)
        sample_rate = 22050
        temp_filename = "temp.wav"
        # numpy 배열을 임시 WAV 파일로 저장 (디스코드 음성 재생용)
        write_wav(temp_filename, sample_rate, audio_array)

        # 사용자가 음성 채널에 접속해 있는지 확인
        if message.author.voice and message.author.voice.channel:
            voice_channel = message.author.voice.channel
            voice_client = message.guild.voice_client
            if voice_client is None:
                voice_client = await voice_channel.connect()
            elif voice_client.channel != voice_channel:
                await voice_client.move_to(voice_channel)

            # 음성 파일 재생 (음성 재생 중 다른 명령어에 의해 중단되지 않도록 독립적으로 실행)
            source = discord.FFmpegPCMAudio(temp_filename, **ffmpeg_opts)
            voice_client.play(source)
        else:
            await message.channel.send(f"Enter a voice channel to talk with {SETTINGS['CHARACTER_SETTINGS']['character_name']}!")
            return

        # 채팅창에 번역된 텍스트 출력
        await message.channel.send(f"{SETTINGS['CHARACTER_SETTINGS']['character_name']} : {response_kr_text}")

if __name__ == '__main__':
    SETTINGS = parse_settings.parse_settings("settings.yaml")
    os.environ["OPENAI_API_KEY"] = SETTINGS['API_SETTINGS']['openai_api_key']
    CHAR_API = API(SETTINGS["API_SETTINGS"]["openai_assistant_key"])
    HPS, NET_G = inference.load_model_and_config(
        SETTINGS['APPLICATION_SETTINGS']['config_path'],
        SETTINGS['APPLICATION_SETTINGS']['weight_path']
    )

    client.run(SETTINGS["DISCORD_SETTINGS"]["bot_token"])