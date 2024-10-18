# Import StreamController modules
from operator import index

from gi.repository.Adw import EntryRow, ExpanderRow, PasswordEntryRow, PreferencesGroup, SwitchRow
from GtkHelper.ItemListComboRow import ItemListComboRowListItem, ItemListComboRow

from src.backend.PluginManager.ActionBase import ActionBase
# Import python modules
import os
# Import gtk modules - used for the config rows
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")


from loguru import logger as log

class HueAssistBasicAction(ActionBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._username = None
    self.bridge_ip_entry = EntryRow
    self.bridge_user_entry = PasswordEntryRow
    self.connection_status_entry = EntryRow
    self.settings_expander_entry: ExpanderRow
    self._ip = None

  def get_config_rows(self) -> list:
    """
    provides the config entries for the plugin
    Returns: config entries as list

    """

    self.bridge_ip_entry = EntryRow(title=self.plugin_base.lm.get("hue.gateway.ip.title"))
    self.bridge_user_entry = PasswordEntryRow(title=self.plugin_base.lm.get("hue.gateway.username.title"))

    self.connection_status_entry = EntryRow(title="Connection status:")
    self.connection_status_entry.set_editable(False)
    self.connection_status_entry.set_text(
      "CONNECTED" if self.plugin_base.backend.is_connected() else "NOT_CONNECTED")

    self.load_config_defaults()

    self.bridge_ip_entry.connect("notify::text", self.on_ip_changed)
    self.bridge_user_entry.connect("notify::text", self.on_username_changed)

    self.settings_expander_entry = ExpanderRow(title=self.plugin_base.lm.get("hue.gateway.connection.preferences.settings"))
    self.settings_expander_entry.add_row(self.bridge_ip_entry)
    self.settings_expander_entry.add_row(self.bridge_user_entry)


    group = PreferencesGroup()
    group.set_title(self.plugin_base.lm.get("hue.gateway.connection.preferences.title"))
    group.set_margin_top(20)
    group.add(self.settings_expander_entry)
    group.add(self.connection_status_entry)

    return [group]

  def load_settings(self):
    self._ip = self.get_settings().get("BRIDGE_IP", "")
    self._username = self.get_settings().get("BRIDGE_USER", "")

    # in case of a new created widget but the backend for the hue bridge is already initialized
    # load data from the backend and store it to the settings
    if self._ip == "" and self._username == "" and self.plugin_base.backend.is_connected():
      self._ip = self.plugin_base.backend.get_ip()
      self._username = self.plugin_base.backend.get_username()
      settings = self.get_settings()
      settings["BRIDGE_IP"] = self._ip
      settings["BRIDGE_USER"] = self._username
      self.set_settings(settings)

  def load_config_defaults(self):
    """
    loads the already configured values
    Returns: already configured values or defaults

    """
    self.load_settings()

    log.trace("### Start - Load Config Defaults ###")

    self.bridge_ip_entry.set_text(self._ip)  # Does not accept None
    self.bridge_user_entry.set_text(self._username)  # Does not accept None

    log.trace("### End - Load Config Defaults ###")

  def on_ip_changed(self, entry, *args) -> None:
    settings = self.get_settings()
    settings["BRIDGE_IP"] = entry.get_text()
    self.set_settings(settings)
    self.plugin_base.backend.connect(settings.get("BRIDGE_IP", ""), settings.get("BRIDGE_USER", ""))

  def on_username_changed(self, entry, *args) -> None:
    settings = self.get_settings()
    settings["BRIDGE_USER"] = entry.get_text()
    self.set_settings(settings)
    self.plugin_base.backend.connect(settings.get("BRIDGE_IP", ""), settings.get("BRIDGE_USER", ""))