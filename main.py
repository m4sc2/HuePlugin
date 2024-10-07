# Import StreamController modules
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.PluginBase import PluginBase
from .actions.HueGroupAction.HueGroupAction import HueGroupAction
from .backend.hue_assist import HueBackend


# Import actions

class PluginTemplate(PluginBase):
    def __init__(self):
        super().__init__()

        self.lm = self.locale_manager
        ## Register actions
        self.simple_action_holder = ActionHolder(
            plugin_base = self,
            action_base = HueGroupAction,
            action_id = "m4sc2::HuePlugin", # Change this to your own plugin id
            action_name = "Hue Group Action",
        )
        self.add_action_holder(self.simple_action_holder)

        settings = self.get_settings()
        host = settings.get("BRIDGE_IP", "")
        username = settings.get("BRIDGE_USER", "")

        self.backend = HueBackend()
        self.backend.set_connection_details(host, username)

        # Register plugin
        self.register(
            plugin_name = "Hue Plugin",
            github_repo = "https://github.com/m4sc2/HuePlugin",
            plugin_version = "1.0.0",
            app_version = "1.1.1-alpha"
        )