# Import StreamController modules

# Import python modules
import os

# Import gtk modules - used for the config rows
import gi

from ..HueGroupAction.HueGroupBasicAction import HueGroupBasicAction

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from loguru import logger as log

class HueGroupLightToggleAction(HueGroupBasicAction):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def on_tick(self) -> None:
    """
    regular update

    will check if the group lights are on|off and change the icon accordingly
    Returns: None

    """
    on = False
    if self.plugin_base.backend.is_connected() :
      if self.get_settings().get("HUE_GROUP", -1) != -1:
        on = self.plugin_base.backend.get_group_on_status(self.get_settings().get("HUE_GROUP", -1))
    else:
      log.error("Hue Bridge Not Connected")

    if on:
      state_new = 1
    else:
      state_new = 0

    self.update_icon(state_new)

  def on_ready(self) -> None:
    """
    initialize the action
    Returns: None

    """
    icon_path = os.path.join(self.plugin_base.PATH, "assets", "light_on.png")
    self.set_media(media_path=icon_path, size=0.60)
    settings = self.get_settings()
    if not self.plugin_base.backend.is_connected() :
      self.plugin_base.backend.connect(settings.get("BRIDGE_IP", ""), settings.get("BRIDGE_USER", ""))

  def on_key_down(self) -> None:
    """
    will toggle the lights from on->off->on->...
    Returns: None

    """
    log.trace("Key Down")
    if self.plugin_base.backend.is_connected() :
      self.plugin_base.backend.toggle_group_lights(self.get_settings().get("HUE_GROUP", -1))
    else:
      log.error("Hue Bridge Not Connected")

  def get_config_rows(self) -> list:
    """
    provides the config entries for the plugin
    Returns: config entries as list

    """

    _config_rows = super().get_config_rows()

    return [*_config_rows]

  def update_icon(self, state_new) -> None:
    """
    update the icon based on the state of the group
    Args:
      state_new: new state of the group action

    Returns: None

    """
    match state_new:
      case 0:
        _icon_path = os.path.join(self.plugin_base.PATH, "assets", "light_off.png")
      case 1:
        _icon_path = os.path.join(self.plugin_base.PATH, "assets", "light_on.png")
      case _:
        _icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
    self.set_media(media_path=_icon_path, size=0.60)

