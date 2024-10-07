# Import StreamController modules
# Import python modules
import os

# Import gtk modules - used for the config rows
import gi

from src.backend.PluginManager.ActionBase import ActionBase

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

class HueGroupAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bridge_ip_entry = None
        self.bridge_user_entry = None

    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)

    def on_key_down(self) -> None:
        print("Key down 2")

    def on_key_up(self) -> None:
        print("Key up")

    def get_config_rows(self) -> list:
        self.bridge_ip_entry = Adw.EntryRow(title=self.plugin_base.lm.get("hue.gateway.ip.title"))
        self.bridge_user_entry = Adw.EntryRow(title=self.plugin_base.lm.get("hue.gateway.username.title"))

        self.load_config_defaults()

        # Connect signals
        self.bridge_ip_entry.connect("notify::text", self.on_url_changed)
        self.bridge_user_entry.connect("notify::text", self.on_json_changed)

        return [self.bridge_ip_entry, self.bridge_user_entry]

    def load_config_defaults(self):
        self.bridge_ip_entry.set_text(self.get_settings().get("BRIDGE_IP", ""))  # Does not accept None
        self.bridge_user_entry.set_text(self.get_settings().get("BRIDGE_USER", ""))  # Does not accept None

    def on_url_changed(self, entry, *args):
        settings = self.get_settings()
        settings["BRIDGE_IP"] = entry.get_text()
        self.set_settings(settings)

    def on_json_changed(self, entry, *args):
        settings = self.get_settings()
        settings["BRIDGE_USER"] = entry.get_text()
        self.set_settings(settings)
