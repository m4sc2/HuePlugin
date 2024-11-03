"""
Module for the Hue assist backend.
"""
from streamcontroller_plugin_tools import BackendBase
from loguru import logger as log
from phue import Bridge


class Group:
  def __init__(self, group_name, status, brightness, group_id):
    """
    Internal Hue light group
    Args:
      group_name:  name of the group
      status:      status of the lights on|off
      brightness:  brightness of the lights
      group_id:    group id in the bridge
    """
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

  def connect(self, host: str, username: str) -> str:
    """
    Initialize the connection to the Hue Bridge.

    Args:
        self: the backend
        username:   username of the Hue Bridge
        host:       ip address of the Hue Bridge

    Returns: CONNECTED in case of successful connection, else Exception to the connection establishment

    """
    self._bridge_ip = host
    self._bridge_username = username
    if self._bridge_ip == "": return "MISSING_IP"
    if self._bridge_username == "": return "MISSING_USERNAME"
    try:
      self._bridge = Bridge(ip=self._bridge_ip, username=self._bridge_username)
      log.trace(self._bridge.get_api())
    except Exception as e:
      return "Exception while connecting to the Hue Bridge: " + str(e)

    return "CONNECTED"

  def is_connected(self) -> bool:
    try:
      self._bridge.get_api()
      return True
    except Exception as e:
      return False

  def get_group_on_status(self, group_id: int) -> bool:
    return self._bridge.get_group(group_id,'on')

  def get_groups(self) -> list:
    log.trace("### Start - Loading Groups of the Hue Bridge ###")
    """
    get all groups configured in the Hue Bridge.

    Returns:
      list of groups with id status and name of the group
    """
    _groupList = []
    for group in self._bridge.groups:
      g = Group(group.name, group.on, 100, group.group_id)
      log.trace("Add group {} (status={}) to group list" , group.name , str(group.on))
      _groupList.append(g)

    log.trace("### End - Loading Groups of the Hue Bridge ###")
    return _groupList

  def get_ip(self) -> str:
    """
    Returns: returns the ip address of the Hue Bridge for the backend

    """
    return self._bridge_ip

  def get_username(self) -> str:
    """
    Returns: username of the Hue Bridge for the backend

    """
    return self._bridge_username

  def toggle_group_lights(self, group_id: int) -> None:
    """
    Toggle lights in the group.

    Args:
      self:       the backend
      group_id:   id of the group

    Returns:
      None

    """
    current_state: bool = self._bridge.get_group(group_id, 'on')
    log.trace("switch group lights to {}", not current_state)
    self._bridge.set_group(group_id, 'on', not current_state)

  def set_brightness(self, group_id:int, brightness: int) -> None:
    self._bridge.set_group(group_id,'bri', brightness)
    log.trace("Set brightness of group {} = {}", group_id, brightness)

  def get_brightness(self, group_id:int) -> int:
    _brightness = self._bridge.get_group(group_id, 'bri')
    log.trace("Get brightness of group {} = {}", group_id, _brightness)
    return _brightness


backend = HueBackend()
