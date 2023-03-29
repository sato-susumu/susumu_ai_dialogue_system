import logging

import pyaudio


# noinspection PyMethodMayBeStatic
class PyAudioUtility:
    HOST_API_NAME = "host_api_name"
    DEVICE_NAME = "device_name"
    DEVICE_ID = "device_id"
    MAX_OUTPUT_CH = "max_output_ch"
    DEFAULT_SAMPLE_RATE = "defaultSampleRate"

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_speaker_id(self, part_of_host_api_name: str, part_of_device_name: str) -> int:
        speaker_list = self.get_speaker_list()
        for speaker in speaker_list:
            if part_of_host_api_name in speaker[self.HOST_API_NAME] \
                    and part_of_device_name in speaker[self.DEVICE_NAME]:
                return speaker[self.DEVICE_ID]
        return -1

    def get_speaker_list(self) -> list:
        speaker_list = []
        pa = pyaudio.PyAudio()
        for host_index in range(pa.get_host_api_count()):
            host_api_info = pa.get_host_api_info_by_index(host_index)
            host_api_name = host_api_info['name']
            for device_index in range(pa.get_host_api_info_by_index(host_index)['deviceCount']):
                device_info = pa.get_device_info_by_host_api_device_index(host_index, device_index)
                index_no = device_info["index"]
                device_name = device_info["name"]
                max_output_ch = device_info["maxOutputChannels"]
                default_sample_rate = device_info["defaultSampleRate"]
                if max_output_ch > 0:
                    speaker_list.append({
                        self.DEVICE_ID: index_no,
                        self.HOST_API_NAME: host_api_name,
                        self.DEVICE_NAME: device_name,
                        self.MAX_OUTPUT_CH: max_output_ch,
                        self.DEFAULT_SAMPLE_RATE: default_sample_rate,
                    })
        return speaker_list

    def print_speaker_list(self) -> None:
        self._logger.debug(self.get_speaker_list())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    PyAudioUtility().print_speaker_list()
