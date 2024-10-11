# Import StreamController modules
from GtkHelper.GtkHelper import ComboRow

from src.backend.PluginManager.ActionBase import ActionBase
# Import python modules
import os
# Import gtk modules - used for the config rows
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Pango

from loguru import logger as log


class HueGroupAction(ActionBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.bridge_ip_entry = None
    self.bridge_user_entry = None
    self.bridge_groups = None

  def on_ready(self) -> None:
    """
    initialize the action
    Returns: None

    """
    icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
    self.set_media(media_path=icon_path, size=0.75)
    settings = self.get_settings()
    self.plugin_base.backend.set_connection_details(settings.get("BRIDGE_IP", ""), settings.get("BRIDGE_USER", ""))
    self.bridge_groups = self.plugin_base.backend.get_groups()

  def on_key_down(self) -> None:
    log.trace("Key Down")
    self.plugin_base.backend.toggle_group_lights(1)

  def on_key_up(self) -> None:
    log.info("Key up")

  def get_config_rows(self) -> list:
    """
    provides the config entries for the plugin
    Returns: config entries as list

    """
    self.bridge_ip_entry = Adw.EntryRow(title=self.plugin_base.lm.get("hue.gateway.ip.title"))
    self.bridge_user_entry = Adw.EntryRow(title=self.plugin_base.lm.get("hue.gateway.username.title"))

    self.device_display_name = Gtk.ListStore.new([str])

    self.device_A_row = ComboRow(title=self.plugin_base.lm.get("hue.gateway.group.title"),
                                 model=self.device_display_name)
    self.device_cell_renderer = Gtk.CellRendererText(ellipsize=Pango.EllipsizeMode.END, max_width_chars=60)
    self.device_A_row.combo_box.pack_start(self.device_cell_renderer, True)
    self.device_A_row.combo_box.add_attribute(self.device_cell_renderer, "text", 0)

    self.load_config_defaults()

    # Connect signals
    self.bridge_ip_entry.connect("notify::text", self.on_ip_changed)
    self.bridge_user_entry.connect("notify::text", self.on_username_changed)

    return [self.bridge_ip_entry, self.bridge_user_entry, self.device_A_row]

  def load_config_defaults(self):
    """
    loads the already configured values
    Returns: already configured values or defaults

    """
    self.bridge_ip_entry.set_text(self.get_settings().get("BRIDGE_IP", ""))  # Does not accept None
    self.bridge_user_entry.set_text(self.get_settings().get("BRIDGE_USER", ""))  # Does not accept None

  def on_ip_changed(self, entry, *args):
    settings = self.get_settings()
    settings["BRIDGE_IP"] = entry.get_text()
    self.set_settings(settings)
    self.plugin_base.backend.set_connection_details(settings.get("BRIDGE_IP", ""), settings.get("BRIDGE_USER", ""))

  def on_username_changed(self, entry, *args):
    settings = self.get_settings()
    settings["BRIDGE_USER"] = entry.get_text()
    self.set_settings(settings)
    self.plugin_base.backend.set_connection_details(settings.get("BRIDGE_IP", ""), settings.get("BRIDGE_USER", ""))
