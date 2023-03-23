from susumu_toolbox.infrastructure.pyaudio_utility import PyAudioUtility


def test_print_speaker_list():
    PyAudioUtility().print_speaker_list()


def test_get_speaker_id():
    utility = PyAudioUtility()
    speaker_list = utility.get_speaker_list()
    if len(speaker_list) >= 3:
        target_device_id = speaker_list[2][utility.DEVICE_ID]
        index = 2
    elif len(speaker_list) >= 1:
        target_device_id = speaker_list[0][utility.DEVICE_ID]
        index = 0
    else:
        return
    target_host_name = speaker_list[index][utility.HOST_API_NAME]
    target_device_name = speaker_list[index][utility.DEVICE_NAME]
    result_device_id = utility.get_speaker_id(target_host_name, target_device_name)
    assert result_device_id == target_device_id
