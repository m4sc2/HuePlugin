# Import StreamController modules

from ..HueGroupAction.HueGroupBasicAction import HueGroupBasicAction
from GtkHelper.ItemListComboRow import ItemListComboRowListItem, ItemListComboRow

# Import python modules
import os
# Import gtk modules - used for the config rows
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from loguru import logger as log

class HueGroupLightToggleAction(HueGroupBasicAction):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.groups_entries = []
    self.hue_group_row = ItemListComboRow

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

  def load_config_action(self):
    """
    loads the already configured values
    Returns: already configured values or defaults

    """
    log.trace("### Start - Load Config Defaults ###")

    if self.get_settings().get("HUE_GROUP", "") != "":
      _group_id = self.get_settings().get("HUE_GROUP", "")
      self.set_active_group(_group_id)
    else :
      if self.plugin_base.backend.is_connected():
        #store setting with the first group
        self.on_hue_group_change(self.hue_group_row)

    log.trace("### End - Load Config Defaults ###")

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

  def set_active_group(self, group_id) -> None:
    """
    changes the active group in settings combo box
    Args:
      group_id: new active group

    Returns: None

    """
    log.trace("try to set active group to group_id ({})", group_id)
    for idx, i in enumerate(self.hue_group_row.get_model()):
      if i.key == group_id:
        self.hue_group_row.set_selected(idx)
        log.trace("finished - set active group to {}({})", i.name, group_id)
        return