# CPU環境だと遅いため無効化
# import numpy as np
# import torch
# from susumu_ai_dialogue_system.vad.base_vad import BaseVad
#
#
# # noinspection PyMethodMayBeStatic
# class SileroVAD(BaseVad):
#     def __init__(self, threshold: float = 0.6):
#         super().__init__()
#         # noinspection SpellCheckingInspection
#         self._vad_model, _ = torch.hub.load(repo_or_dir="snakers4/silero-vad", model="silero_vad", onnx=False)
#         self._threshold = threshold
#
#     def get_threshold(self) -> float:
#         return self._threshold
#
#     def detect(self, audio_chunk) -> float:
#         audio_int16 = np.frombuffer(audio_chunk, np.int16)
#         audio_float32 = self.int2float(audio_int16)
#         # before = time.perf_counter()
#         confidence = self._vad_model(torch.from_numpy(audio_float32), 16000).item()
#         # after = time.perf_counter()
#         # logger.debug(f"{after - before:.3f} s")
#
#         return confidence
#
#     def int2float(self, sound) -> np.ndarray:
#         # サンプルのまんま
#         abs_max = np.abs(sound).max()
#         sound = sound.astype('float32')
#         if abs_max > 0:
#             sound *= 1 / abs_max
#         sound = sound.squeeze()
#         return sound
#
