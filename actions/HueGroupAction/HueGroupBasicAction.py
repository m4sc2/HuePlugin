# Import StreamController modules

from gi.repository.Adw import PreferencesGroup

from ..HueBasicAction.HueAssistBasicAction import HueAssistBasicAction
from GtkHelper.ItemListComboRow import ItemListComboRowListItem, ItemListComboRow

# Import python modules
# Import gtk modules - used for the config rows
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from loguru import logger as log

class HueGroupBasicAction(HueAssistBasicAction):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.groups_entries = []
    self.hue_group_row = ItemListComboRow

  def get_config_rows(self) -> list:
    """
    provides the config entries for the plugin
    Returns: config entries as list

    """

    _config_rows = super().get_config_rows()

    self.hue_group_row = ItemListComboRow(self.groups_entries)

    if self.plugin_base.backend.is_connected() :
      self.update_bridge_groups()
      self.hue_group_row.set_title(self.plugin_base.lm.get("hue.gateway.group.title"))

    self.load_config_action()

    self.hue_group_row.connect("notify::selected", self.on_hue_group_change)

    _group = PreferencesGroup()
    _group.set_title(self.plugin_base.lm.get("hue.action.toggle.group.title"))
    _group.set_margin_top(20)
    _group.add(self.hue_group_row)

    return [*_config_rows, _group]

  def update_bridge_groups(self):
    """
    function to update the bridge groups will add all groups from the hue bridge to the combo box for selection of the
    group
    Returns:

    """
    _bridge_groups = self.plugin_base.backend.get_groups()
    self.groups_entries = []
    if _bridge_groups is not None:
      for Group in _bridge_groups:
        self.groups_entries.append(ItemListComboRowListItem(Group.group_id, Group.group_name))
    self.hue_group_row = ItemListComboRow(self.groups_entries)


  def load_config_action(self):
    """
    loads the already configured values
    Returns: already configured values or defaults

    """
    log.trace("### Start - Load Config Defaults ###")

    if self.get_settings().get("HUE_GROUP", "") != "":
      _group_id = self.get_settings().get("HUE_GROUP", "")
      self.set_active_group(_group_id)
    else :
      if self.plugin_base.backend.is_connected():
        #store setting with the first group
        self.on_hue_group_change(self.hue_group_row)

    log.trace("### End - Load Config Defaults ###")

  def on_hue_group_change(self, entry, *args) -> None:
    log.info("Hue Bridge Group Changed")
    settings = self.get_settings()
    settings["HUE_GROUP"] = entry.get_selected_item().key
    self.set_settings(settings)

  def set_active_group(self, group_id) -> None:
    """
    changes the active group in settings combo box
    Args:
      group_id: new active group

    Returns: None

    """
    log.trace("try to set active group to group_id ({})", group_id)
    for idx, i in enumerate(self.hue_group_row.get_model()):
      if i.key == group_id:
        self.hue_group_row.set_selected(idx)
        log.trace("finished - set active group to {}({})", i.name, group_id)
        return