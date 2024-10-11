# Import StreamController modules

from GtkHelper.ItemListComboRow import ItemListComboRowListItem, ItemListComboRow

from src.backend.PluginManager.ActionBase import ActionBase
# Import python modules
import os
# Import gtk modules - used for the config rows
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

from loguru import logger as log


class HueGroupAction(ActionBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.groups_entries = None
    self.hue_group_row = None
    self.bridge_ip_entry = None
    self.bridge_user_entry = None

  def on_ready(self) -> None:
    """
    initialize the action
    Returns: None

    """
    icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
    self.set_media(media_path=icon_path, size=0.75)
    settings = self.get_settings()
    self.plugin_base.backend.set_connection_details(settings.get("BRIDGE_IP", ""), settings.get("BRIDGE_USER", ""))

  def on_key_down(self) -> None:
    log.trace("Key Down")
    self.plugin_base.backend.toggle_group_lights(self.get_settings().get("HUE_GROUP", -1))

  def on_key_up(self) -> None:
    log.info("Key up")

  def get_config_rows(self) -> list:
    """
    provides the config entries for the plugin
    Returns: config entries as list

    """
    self.bridge_ip_entry = Adw.EntryRow(title=self.plugin_base.lm.get("hue.gateway.ip.title"))
    self.bridge_user_entry = Adw.EntryRow(title=self.plugin_base.lm.get("hue.gateway.username.title"))

    _bridge_groups = self.plugin_base.backend.get_groups()
    self.groups_entries = []

    if _bridge_groups is not None:
      for Group in _bridge_groups:
        self.groups_entries.append(ItemListComboRowListItem(Group.group_id, Group.group_name))

    self.hue_group_row = ItemListComboRow(items=self.groups_entries)
    self.hue_group_row.set_title(self.plugin_base.lm.get("hue.gateway.group.title"))

    self.load_config_defaults()

    # Connect signals
    self.bridge_ip_entry.connect("notify::text", self.on_ip_changed)
    self.bridge_user_entry.connect("notify::text", self.on_username_changed)
    self.hue_group_row.connect("notify::selected", self.on_hue_group_change)

    return [self.bridge_ip_entry, self.bridge_user_entry, self.hue_group_row]

  def load_config_defaults(self):
    """
    loads the already configured values
    Returns: already configured values or defaults

    """
    self.bridge_ip_entry.set_text(self.get_settings().get("BRIDGE_IP", ""))  # Does not accept None
    self.bridge_user_entry.set_text(self.get_settings().get("BRIDGE_USER", ""))  # Does not accept None
    if self.get_settings().get("HUE_GROUP", "") != "":
      self.hue_group_row.set_selected_item_by_key(self.get_settings().get("HUE_GROUP", ""))

  def on_ip_changed(self, entry, *args):
    settings = self.get_settings()
    settings["BRIDGE_IP"] = entry.get_text()
    self.set_settings(settings)
    self.plugin_base.backend.set_connection_details(settings.get("BRIDGE_IP", ""), settings.get("BRIDGE_USER", ""))

  def on_hue_group_change(self, entry, *args):
    settings = self.get_settings()
    settings["HUE_GROUP"] = entry.get_selected_item().key
    self.set_settings(settings)

  def on_username_changed(self, entry, *args):
    settings = self.get_settings()
    settings["BRIDGE_USER"] = entry.get_text()
    self.set_settings(settings)
    self.plugin_base.backend.set_connection_details(settings.get("BRIDGE_IP", ""), settings.get("BRIDGE_USER", ""))
