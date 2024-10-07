# Import StreamController modules
import os

from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.PluginBase import PluginBase
from .actions.HueGroupAction.HueGroupAction import HueGroupAction

# Import actions

class PluginTemplate(PluginBase):
    def __init__(self):
        super().__init__()
        self.lm = self.locale_manager
        ## Launch backend
        backend_path = os.path.join(self.PATH, "backend", "hue_assist.py")
        self.launch_backend(backend_path=backend_path, open_in_terminal=False)

        ## Register actions
        self.simple_action_holder = ActionHolder(
            plugin_base = self,
            action_base = HueGroupAction,
            action_id = "m4sc2::HuePlugin", # Change this to your own plugin id
            action_name = "Hue Group Action",
        )
        self.add_action_holder(self.simple_action_holder)

        # Register plugin
        self.register(
            plugin_name = "Hue Plugin",
            github_repo = "https://github.com/m4sc2/HuePlugin",
            plugin_version = "1.0.0",
            app_version = "1.1.1-alpha"
        )