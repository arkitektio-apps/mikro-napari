import pytest
import napari
from mikro_napari.widgets.main_widget import MikroNapariWidget
from koil.vars import current_loop


def test_viewer_non_intrusive(make_napari_viewer):
    assert current_loop.get() is None, "There should be no loop at this point"
    viewer: napari.Viewer = make_napari_viewer(strict_qt=True)
    widget = MikroNapariWidget(viewer)
    viewer.window.add_dock_widget(widget, area="left", name="Mikro")
