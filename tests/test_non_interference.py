import pytest
import napari
from mikro_napari.widgets.main_widget import MikroNapariWidget
from koil.vars import current_loop


@pytest.mark.qt
def test_viewer_non_intrusive(make_napari_viewer, qtbot):
    viewer = make_napari_viewer()
    widget = MikroNapariWidget(viewer)
    viewer.window.add_dock_widget(widget, area="left", name="Mikro")


