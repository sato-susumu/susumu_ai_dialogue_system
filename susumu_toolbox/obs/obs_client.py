from queue import Empty

from obswebsocket import obsws, requests
from six.moves import queue

from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic,PyShadowingNames
class OBSClient:
    """OBS WebSocket Client

    利用にはOBS Studioの設定変更が必要です。
      ツール > Websocket設定 > 「WebSocketサーバーを有効にする」をON

    サポートしているobs-websocket protocolは 4.9.1 のみです。
    最新のOBS Studioを利用している場合は、プラグインのインストールが必要です。
    https://github.com/obsproject/obs-websocket/releases/tag/4.9.1-compat

    参考資料：
    obs-websocket 4.9.1 protocol reference
    https://github.com/obsproject/obs-websocket/blob/4.x-compat/docs/generated/protocol.md

    obs-websocket latest Protocol
    https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md
    """

    def __init__(self, config: Config):
        self._config = config
        self._ws = None
        self._connection_waiting_queue = queue.Queue()

    def _on_connect(self, ws_app) -> None:
        print("on_connect({})".format(ws_app))
        self._connection_waiting_queue.put(True)

    def _on_disconnect(self, ws_app) -> None:
        print("on_disconnect({})".format(ws_app))

    def connect(self) -> None:
        host = self._config.get_obs_host()
        port_no = self._config.get_obs_port_no()
        password = self._config.get_obs_password()
        self._ws = obsws(host, port_no, password, authreconnect=1,
                         on_connect=self._on_connect, on_disconnect=self._on_disconnect)

        while not self._connection_waiting_queue.empty():
            self._connection_waiting_queue.get(block=False)

        self._ws.connect()
        try:
            self._connection_waiting_queue.get(block=True, timeout=3)
        except Empty:
            raise ConnectionError("OBS 接続失敗") from None

    def disconnect(self) -> None:
        self._ws.disconnect()

    def set_text(self, scene_name: str, source: str, text: str) -> None:
        self._ws.call(
            requests.SetTextGDIPlusProperties(scene_name=scene_name, source=source, text=text))
