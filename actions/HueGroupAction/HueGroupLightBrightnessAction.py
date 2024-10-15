# Import StreamController modules
from gi.repository.Adw import PreferencesGroup
from GtkHelper.GtkHelper import ScaleRow

from ..HueGroupAction.HueGroupBasicAction import HueGroupBasicAction
from GtkHelper.ItemListComboRow import ItemListComboRowListItem, ItemListComboRow

# Import python modules
import os
# Import gtk modules - used for the config rows
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from loguru import logger as log

class HueGroupLightBrightnessAction(HueGroupBasicAction):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.brightness_adjust_scale = ScaleRow

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

    self.brightness_adjust_scale = ScaleRow(title=self.plugin_base.lm.get("hue.action.group.brightness.adjust"),
                                            value=0,
                                            min=-50,
                                            max=50,
                                            step=1,
                                            text_left="-50",
                                            text_right="50"
                                            )
    self.brightness_adjust_scale.scale.set_draw_value(True)
    self.brightness_adjust_scale.scale.connect("value-changed", self.on_brightness_adjust_changed)

    _config_rows = super().get_config_rows()

    _group = PreferencesGroup()
    _group.set_title(self.plugin_base.lm.get("hue.action.settings.title"))
    _group.set_margin_top(20)
    _group.add(self.brightness_adjust_scale)



    return [*_config_rows, _group]

  def on_brightness_adjust_changed(self):
    log.trace("Brightness Adjust")


  def load_config_action(self):
    """
    loads the already configured values
    Returns: already configured values or defaults

    """
    log.trace("### Start - Load Config Defaults ###")

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
        _icon_path = os.path.join(self.plugin_base.PATH, "assets", "light_decrease.png")
      case 1:
        _icon_path = os.path.join(self.plugin_base.PATH, "assets", "light_increase.png")
      case _:
        _icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
    self.set_media(media_path=_icon_path, size=0.60)

