"""该模块用于生成VITS文件
使用方法

python cmd_inference.py -m 模型路径 -c 配置文件路径 -o 输出文件路径 -l 输入的语言 -t 输入文本 -s 合成目标说话人名称

可选参数
-ns 感情变化程度
-nsw 音素发音长度
-ls 整体语速
-on 输出文件的名称

"""

# from pathlib import Path
from character_tts import utils
from character_tts.models import SynthesizerTrn
import torch
from torch import no_grad, LongTensor
from character_tts.text import text_to_sequence #, _clean_text
from character_tts import commons

device = "cuda:0" if torch.cuda.is_available() else "cpu"

language_marks = {
    "Japanese": "",
    "日本語": "[JA]",
    "简体中文": "[ZH]",
    "English": "[EN]",
    "Mix": "",
}


def load_model_and_config(config_path, model_path):
    hps = utils.get_hparams_from_file(config_path)
    net_g = SynthesizerTrn(
        len(hps.symbols),
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=hps.data.n_speakers,
        **hps.model).to(device)
    _ = net_g.eval()
    _ = utils.load_checkpoint(model_path, net_g, None)

    return hps, net_g

def get_text(text, hps, is_symbol):
    text_norm = text_to_sequence(text, hps.symbols, [] if is_symbol else hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm

def inference_tts(hps,
                  net_g,
                  text,
                  noise_scale=.667,
                  noise_scale_w=0.6,
                  length_scale=1,
                  language="日本語",
                  spk='holo'):
    speaker_ids = hps.speakers
    if language in list(language_marks.keys()):
        text = language_marks[language] + text + language_marks[language]
        speaker_id = speaker_ids[spk]
        stn_tst = get_text(text, hps, False)
        with no_grad():
            x_tst = stn_tst.unsqueeze(0).to(device)
            x_tst_lengths = LongTensor([stn_tst.size(0)]).to(device)
            sid = LongTensor([speaker_id]).to(device)
            audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale, noise_scale_w=noise_scale_w,
                                length_scale=1.0 / length_scale)[0][0, 0].data.cpu().float().numpy()
        del stn_tst, x_tst, x_tst_lengths, sid

        return audio
    else:
        raise ValueError("Language not supported.")