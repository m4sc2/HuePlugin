# Import StreamController modules
import os

from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.PluginManager.PluginBase import PluginBase
from .actions.HueGroupAction.HueGroupLightBrightnessAction import HueGroupLightBrightnessAction
from .actions.HueGroupAction.HueGroupLightToggleAction import HueGroupLightToggleAction
from .actions.HueGroupAction.HueGroupSceneToggleAction import HueGroupSceneToggleAction

from gi.repository import Gtk


# Import actions

class HuePlugin(PluginBase):
    def __init__(self):
        super().__init__()
        self.lm = self.locale_manager
        ## Launch backend
        backend_path = os.path.join(self.PATH, "backend", "hue_backend_assist.py")
        self.launch_backend(backend_path=backend_path, open_in_terminal=False)

        ## Register actions
        self.simple_action_holder = ActionHolder(
            plugin_base=self,
            action_base=HueGroupLightToggleAction,
            action_id="m4sc2::HuePluginGroupLightsToggle",  # Change this to your own plugin id
            action_name="Hue Group Action - Lights Toggle",
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
            }
        )
        self.add_action_holder(self.simple_action_holder)

        self.simple_action_holder = ActionHolder(
            plugin_base=self,
            action_base=HueGroupSceneToggleAction,
            action_id="m4sc2::HuePluginGroupSceneToggle",  # Change this to your own plugin id
            action_name="Hue Group Action - Scene Toggle",
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
            }
        )
        self.add_action_holder(self.simple_action_holder)

        self.simple_action_holder = ActionHolder(
            plugin_base=self,
            action_base=HueGroupLightBrightnessAction,
            action_id="m4sc2::HuePluginGroupLightsBrightness",  # Change this to your own plugin id
            action_name="Hue Group Action - Lights Brightness Change",
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
            }
        )
        self.add_action_holder(self.simple_action_holder)

        # Register plugin
        self.register(
            plugin_name="Hue Plugin",
            github_repo="https://github.com/m4sc2/HuePlugin",
            plugin_version="1.0.0",
            app_version="1.1.1-alpha"
        )

    def get_selector_icon(self) -> Gtk.Widget:
        return Gtk.Image(icon_name="preferences-desktop-color")
