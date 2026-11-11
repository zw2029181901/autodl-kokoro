import functools
from pathlib import Path
from runtime.common import device, guarded, model_path, output_path, page_header


@functools.lru_cache(maxsize=1)
def model():
    from kokoro import KModel
    directory = Path(model_path())
    return KModel(config=str(directory / "config.json"), model=str(directory / "kokoro-v1_0.pth")).to(device()).eval()


@functools.lru_cache(maxsize=2)
def pipeline(language):
    from kokoro import KPipeline
    return KPipeline(lang_code=language, model=model())


@guarded
def synthesize(text, language, speed):
    import numpy as np
    import soundfile as sf
    if not text.strip() or len(text) > 1500:
        raise ValueError("请输入1至1500个字符")
    code, voice = {"中文女声": ("z", "zf_xiaobei"), "美式英文女声": ("a", "af_heart")}[language]
    voice_path = str(Path(model_path()) / "voices" / f"{voice}.pt")
    chunks = []
    for _, _, audio in pipeline(code)(text, voice=voice_path, speed=float(speed), split_pattern=r"\n+"):
        chunks.append(audio.detach().cpu().numpy() if hasattr(audio, "detach") else np.asarray(audio))
    if not chunks:
        raise ValueError("没有生成音频，请检查输入文本")
    destination = output_path(".wav")
    sf.write(destination, np.concatenate(chunks), 24000)
    return str(destination), str(destination)


def build_ui():
    import gradio as gr
    with gr.Blocks(title="Kokoro 配音") as ui:
        page_header()
        text = gr.Textbox(label="配音文本", value="你好，欢迎使用语音合成工具。", lines=5, max_lines=10)
        language = gr.Radio(["中文女声", "美式英文女声"], value="中文女声", label="预设音色")
        speed = gr.Slider(0.7, 1.4, value=1.0, step=0.05, label="语速")
        button = gr.Button("生成配音", variant="primary")
        audio = gr.Audio(label="试听")
        file = gr.File(label="下载 WAV")
        button.click(synthesize, [text, language, speed], [audio, file], api_name="synthesize")
    return ui
