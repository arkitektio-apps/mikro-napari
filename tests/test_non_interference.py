import pytest
import napari
from mikro_napari.widgets.main_widget import MikroNapariWidget
from koil.vars import current_loop


@pytest.fixture()
def viewer():
    return napari.Viewer()



def test_viewer_non_intrusive(napari, qtbot):
    widget = MikroNapariWidget(viewer)
    viewer.window.add_dock_widget(widget, area="left", name="Mikro")


