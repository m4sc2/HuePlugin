# Import StreamController modules

# Import python modules
import os

# Import gtk modules - used for the config rows
import gi
from gi.repository.Adw import PreferencesGroup

from GtkHelper.ItemListComboRow import ItemListComboRow, ItemListComboRowListItem
from ..HueGroupAction.HueGroupBasicAction import HueGroupBasicAction

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from loguru import logger as log

class HueGroupSceneToggleAction(HueGroupBasicAction):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.hue_scene_row = None
    self.scene_entries = []
    self._sceneId = None

  def on_tick(self) -> None:
    """
    regular update

    will check if the group lights are on|off and change the icon accordingly
    Returns: None

    """


  def on_ready(self) -> None:
    """
    initialize the action
    Returns: None

    """
    super().load_settings()
    icon_path = os.path.join(self.plugin_base.PATH, "assets", "light_on.png")
    self.set_media(media_path=icon_path, size=0.60)
    self.connect_to_bridge()

  def on_key_down(self) -> None:
    """
    will change the scene for the configured group
    Returns: None

    """
    log.trace("Key Down")
    if self.plugin_base.backend.is_connected() :
      self.plugin_base.backend.activate_scene(self._groupId, self._sceneId)
    else:
      log.error("Hue Bridge Not Connected")

  def get_config_rows(self) -> list:
    """
    provides the config entries for the plugin
    Returns: config entries as a list

    """

    _config_rows = super().get_config_rows()

    self.hue_scene_row = ItemListComboRow(self.scene_entries)

    if self.plugin_base.backend.is_connected() :
      self.update_bridge_scenes()
      self.hue_scene_row.set_title(self.plugin_base.lm.get("hue.gateway.scene.title"))

    self.load_config_row_settings()

    self.hue_scene_row.connect("notify::selected", self.on_hue_scene_change)

    if self._sceneId is not None:
      self.set_active_scene(self._sceneId)

    _group = PreferencesGroup()
    _group.set_title(self.plugin_base.lm.get("hue.action.toggle.scene.title"))
    _group.set_margin_top(20)
    _group.add(self.hue_scene_row)

    return [*_config_rows, _group]

  def set_active_scene(self, scene_id) -> None:
    """
    changes the active group in settings combo box
    Args:
      scene_id: new scene group

    Returns: None

    """
    log.trace("try to set active group to group_id ({})", scene_id)
    for idx, i in enumerate(self.hue_scene_row.get_model()): # type: ItemListComboRowListItem
      if i.key == scene_id:
        self.hue_scene_row.set_selected(position=idx)
        log.trace("finished - set active group to {}({})", i.name, scene_id)
        return

  def load_config_row_settings(self):
      """
      loads the already configured values
      Returns: already configured values or defaults

      """
      self.load_settings()
      super().load_config_row_settings()

  def load_settings(self):
    """
    loads the already configured values
    Returns: already configured values or defaults

    """
    super().load_settings()
    self._sceneId = self.get_settings().get("HUE_SCENE", "")

  def on_hue_scene_change(self, entry, *args) -> None:
    log.info("Hue Bridge Scene Changed {}", args)
    settings = self.get_settings()
    settings["HUE_SCENE"] = entry.get_selected_item().key
    self._sceneId = self.get_settings().get("HUE_SCENE", "")
    self.set_settings(settings)

  def update_bridge_scenes(self):
    """
    the function to update the bridge groups will add all groups from the hue bridge to the combo box for selection of the
    group
    Returns:

    """
    _bridge_scenes = self.plugin_base.backend.get_scenes()
    self.scene_entries = []
    if _bridge_scenes is not None:
      for Scene in _bridge_scenes:
        self.scene_entries.append(ItemListComboRowListItem(Scene.scene_id, Scene.scene_name))
    self.hue_scene_row = ItemListComboRow(self.scene_entries)
