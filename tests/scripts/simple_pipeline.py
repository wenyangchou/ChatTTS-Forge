from modules.core.handler.datacls.audio_model import AdjustConfig
from modules.core.handler.datacls.chattts_model import ChatTTSConfig, InferConfig
from modules.core.handler.datacls.enhancer_model import EnhancerConfig
from modules.core.handler.datacls.tn_model import TNConfig
from modules.core.pipeline.factory import PipelineFactory
from modules.core.pipeline.processor import TTSPipelineContext
from modules.core.speaker import speaker_mgr

import soundfile as sf

context = TTSPipelineContext(
    text="Hello, world!",
    spk=speaker_mgr.get_speaker("female2"),
    tts_config=ChatTTSConfig(),
    infer_config=InferConfig(),
    adjust_config=AdjustConfig(),
    enhancer_config=EnhancerConfig(),
    tn_config=TNConfig(),
)

pipeline = PipelineFactory.create(context)

with open("output.wav", "wb") as f:
    sr, audio = pipeline.generate()
    sf.write(f, audio, sr)

with open("output_stream.wav", "wb") as f:
    for sr, audio in pipeline.generate_stream():
        sf.write(f, audio, sr)
