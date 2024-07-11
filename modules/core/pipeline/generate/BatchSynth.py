import threading
from typing import Union
from modules.core.models.TTSModel import TTSModel
from modules.core.pipeline.dcls import TTSPipelineContext, TTSSegment
from modules.core.pipeline.generate.BatchGenerate import BatchGenerate
from modules.core.pipeline.generate.Bucketizer import Bucketizer
from modules.core.pipeline.generate.SynthSteamer import SynthStreamer
from modules.core.pipeline.generate.dcls import SynthAudio


class BatchSynth:
    def __init__(
        self,
        input_segments: list[TTSSegment],
        context: TTSPipelineContext,
        model: TTSModel,
    ) -> None:
        self.segments = [SynthAudio(segment=segment) for segment in input_segments]
        self.streamer = SynthStreamer(
            segments=self.segments, context=context, model=model
        )
        self.bucketizer = Bucketizer(segments=self.segments)
        self.buckets = self.bucketizer.build_buckets()
        self.generator = BatchGenerate(
            buckets=self.buckets, context=context, model=model
        )

        self.thread1 = None

    def wait_done(self, timeout: Union[float, None] = None):
        self.generator.done.wait(timeout=timeout)

    def is_done(self):
        return self.generator.is_done()

    def sr(self):
        return self.segments[0].sr

    def read(self):
        return self.streamer.read()

    def start_generate(self):
        if self.thread1 is not None:
            return
        gen_t1 = threading.Thread(target=self.generator.generate, args=(), daemon=True)
        gen_t1.start()
        self.thread1 = gen_t1
        return gen_t1
