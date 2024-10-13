# Import StreamController modules
from operator import index

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

class HueGroupLightToggleAction(ActionBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.groups_entries = []
    self.hue_group_row = None
    self.bridge_ip_entry = None
    self.bridge_user_entry = None

  def on_tick(self) -> None:
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
      self.plugin_base.backend.set_connection_details(settings.get("BRIDGE_IP", ""), settings.get("BRIDGE_USER", ""))

  def on_key_down(self) -> None:
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

    _config_rows = []

    self.bridge_ip_entry = Adw.EntryRow(title=self.plugin_base.lm.get("hue.gateway.ip.title"))
    self.bridge_user_entry = Adw.EntryRow(title=self.plugin_base.lm.get("hue.gateway.username.title"))

    self.hue_group_row = ItemListComboRow(self.groups_entries)


    # Connect signals

    _config_rows.append(self.bridge_ip_entry)
    _config_rows.append(self.bridge_user_entry)

    if self.plugin_base.backend.is_connected() :
      self.update_bridge_groups()
      self.hue_group_row.set_title(self.plugin_base.lm.get("hue.gateway.group.title"))


    self.load_config_defaults()
    _config_rows.append(self.hue_group_row)

    self.bridge_ip_entry.connect("notify::text", self.on_ip_changed)
    self.hue_group_row.connect("notify::selected", self.on_hue_group_change)
    self.bridge_user_entry.connect("notify::text", self.on_username_changed)

    return _config_rows

  def update_bridge_groups(self):
    _bridge_groups = self.plugin_base.backend.get_groups()
    self.groups_entries = []
    if _bridge_groups is not None:
      for Group in _bridge_groups:
        self.groups_entries.append(ItemListComboRowListItem(Group.group_id, Group.group_name))
    self.hue_group_row = ItemListComboRow(self.groups_entries)


  def load_config_defaults(self):
    """
    loads the already configured values
    Returns: already configured values or defaults

    """
    _ip = self.get_settings().get("BRIDGE_IP", "")
    _username = self.get_settings().get("BRIDGE_USER", "")

    # in case of a new created widget but the backend for the hue bridge is already initialized
    # load data from the backend and store it to the settings
    if _ip == "" and _username == "" and self.plugin_base.backend.is_connected():
      _ip = self.plugin_base.backend.get_ip()
      _username = self.plugin_base.backend.get_username()
      settings = self.get_settings()
      settings["BRIDGE_IP"] = _ip
      settings["BRIDGE_USER"] = _username
      self.set_settings(settings)

    self.bridge_ip_entry.set_text(_ip)  # Does not accept None
    self.bridge_user_entry.set_text(_username)  # Does not accept None

    if self.get_settings().get("HUE_GROUP", "") != "":
      _groupid = self.get_settings().get("HUE_GROUP", "")
      self.set_active_group(_groupid)

    else :
      if self.plugin_base.backend.is_connected():
        #store setting with the first group
        self.on_hue_group_change(self.hue_group_row)

  def on_ip_changed(self, entry, *args) -> None:
    settings = self.get_settings()
    settings["BRIDGE_IP"] = entry.get_text()
    self.set_settings(settings)
    self.plugin_base.backend.set_connection_details(settings.get("BRIDGE_IP", ""), settings.get("BRIDGE_USER", ""))
    if self.plugin_base.backend.is_connected():
      self.update_bridge_groups()

  def on_hue_group_change(self, entry, *args) -> None:
    log.info("Hue Bridge Group Changed")
    settings = self.get_settings()
    settings["HUE_GROUP"] = entry.get_selected_item().key
    self.set_settings(settings)

  def on_username_changed(self, entry, *args) -> None:
    settings = self.get_settings()
    settings["BRIDGE_USER"] = entry.get_text()
    self.set_settings(settings)
    self.plugin_base.backend.set_connection_details(settings.get("BRIDGE_IP", ""), settings.get("BRIDGE_USER", ""))
    if self.plugin_base.backend.is_connected():
      self.update_bridge_groups()

  def update_icon(self, state_new) -> None:
    match state_new:
      case 0:
        _icon_path = os.path.join(self.plugin_base.PATH, "assets", "light_off.png")
      case 1:
        _icon_path = os.path.join(self.plugin_base.PATH, "assets", "light_on.png")
      case _:
        _icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")

    self.set_media(media_path=_icon_path, size=0.60)

  def set_active_group(self, group_id) -> int:
    log.info(group_id)
    for idx, i in enumerate(self.hue_group_row.get_model()):
      log.info(i.key)
      if i.key == group_id:
        self.hue_group_row.set_selected(idx)

    return 0