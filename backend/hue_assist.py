"""
Module for the Hue assist backend.
"""
from streamcontroller_plugin_tools import BackendBase
from loguru import logger as log
from phue import Bridge


class Group:
  def __init__(self, group_name, status, brightness, group_id):
    self.group_name = group_name
    self.status = status
    self.brightness = brightness
    self.group_id = group_id

  def __str__(self):
    return f"{self.group_name}({self.status}) - groupId: {self.group_id} - brightness: {self.brightness}"


class HueBackend(BackendBase):
  def __init__(self):
    super().__init__()
    self._bridge: Bridge = None
    self._bridge_ip: str = ""
    self._bridge_username: str = ""

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

  def is_connected(self) -> bool:
    try:
      self._bridge.connect()
      return True
    except Exception as e:
      return False

  def get_groups(self) -> list:
    _groupList = []
    for group in self._bridge.groups:
      g = Group(group.name, group.on, 100, group.group_id)
      log.trace(group.name + " " + str(group.on))
      _groupList.append(g)
    return _groupList

  def toggle_group_lights(self, group_id: int) -> None:
    """
    Toggle lights on the group.

    Args:
      self: the backend
      group_id:  id of the group

    Returns:
      None

    """
    current_state: bool = self._bridge.get_group(group_id, 'on')
    self._bridge.set_group(group_id, 'on', not current_state)


backend = HueBackend()
