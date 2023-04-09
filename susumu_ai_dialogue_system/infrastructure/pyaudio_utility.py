from dataclasses import dataclass
from typing import List

import pyaudio
from loguru import logger


@dataclass
class PyAudioDevice:
    host_api_name: str
    device_name: str
    device_id: int
    max_output_ch: int
    default_sample_rate: int


# noinspection PyMethodMayBeStatic
class PyAudioUtility:
    def __init__(self):
        pass

    def get_speaker_id(self, part_of_host_api_name: str, part_of_device_name: str) -> int:
        speaker_list = self.get_speaker_list()
        for speaker in speaker_list:
            if part_of_host_api_name in speaker.host_api_name \
                    and part_of_device_name in speaker.device_name:
                logger.debug(f"2nd speaker: speaker_id={speaker.device_id} api_name={speaker.host_api_name} \
                    device_name={speaker.device_name}")
                return speaker.device_id
        return -1

    def get_speaker_list(self) -> List[PyAudioDevice]:
        speaker_list = []
        pa = pyaudio.PyAudio()
        for host_index in range(pa.get_host_api_count()):
            host_api_info = pa.get_host_api_info_by_index(host_index)
            host_api_name = host_api_info['name']
            devices = [pa.get_device_info_by_host_api_device_index(host_index, device_index) for device_index in
                       range(host_api_info['deviceCount'])]
            for device_info in devices:
                if device_info["maxOutputChannels"] <= 0:
                    continue
                device = PyAudioDevice(host_api_name=host_api_name,
                                       device_name=device_info["name"],
                                       device_id=int(device_info["index"]),
                                       max_output_ch=int(device_info["maxOutputChannels"]),
                                       default_sample_rate=int(device_info["defaultSampleRate"]))
                speaker_list.append(device)
        return speaker_list

    def print_speaker_list(self) -> None:
        speaker_list = self.get_speaker_list()
        for speaker in speaker_list:
            logger.debug(speaker)


if __name__ == '__main__':
    PyAudioUtility().print_speaker_list()
