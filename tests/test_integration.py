import pytest
from mikro_napari.widgets.main_widget import MikroNapariWidget
import pytest
from .integration.utils import wait_for_http_response
from .utils import build_relative
from testcontainers.compose import DockerCompose
from PyQt5 import QtCore


@pytest.mark.integration
@pytest.fixture(scope="session")
def environment():
    with DockerCompose(
        filepath=build_relative("integration"),
        compose_file_name="docker-compose.yaml",
    ):
        wait_for_http_response("http://localhost:8019/ht", max_retries=5)
        # wait_for_http_response("http://localhost:8088/ht", max_retries=5)
        wait_for_http_response("http://localhost:8098/ht", max_retries=5)
        yield


@pytest.mark.integration
def test_can_login(make_napari_viewer, environment, qtbot):
    viewer = make_napari_viewer()
    widget = MikroNapariWidget(viewer)
    viewer.window.add_dock_widget(widget, area="left", name="Mikro")

    with qtbot.waitSignal(widget.magic_bar.configure_task.returned):
        qtbot.mouseClick(widget.magic_bar.magicb, QtCore.Qt.LeftButton)

    assert widget.magic_bar.magicb.text() == "Login", "Magic bar should be configured"

    with qtbot.waitSignal(widget.magic_bar.login_task.returned):
        qtbot.mouseClick(widget.magic_bar.magicb, QtCore.Qt.LeftButton)

    assert (
        widget.magic_bar.magicb.text() == "Provide"
    ), "Magic bar should now have login"
