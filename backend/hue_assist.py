"""
Module for the Hue assist backend.
"""
from streamcontroller_plugin_tools import BackendBase
from loguru import logger as log
from phue import Bridge


class HueBackend(BackendBase):
    def __init__(self):
        super().__init__()
        _bridge: Bridge = None
        _bridge_ip: str = ""
        _bridge_username: str = ""

    def set_connection_details(self, host: str, username: str) -> None:
        """
        Initialize the connection to the Hue Bridge.

        Args:
            self: the backend
            username:   username of the Hue Bridge
            host:       ip address of the Hue Bridge

        Returns: None

        """
        self._bridge_ip = host
        self._bridge_username = username
        if self._bridge_ip == "": return
        if self._bridge_username == "": return
        self._bridge = Bridge(ip=self._bridge_ip, username=self._bridge_username)
        log.info(self._bridge.get_api())

    def get_test(self) -> str:
        return "test"

backend = HueBackend()