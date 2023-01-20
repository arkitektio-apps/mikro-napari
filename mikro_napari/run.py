from arkitekt.apps.connected import ConnectedApp
from arkitekt.apps.fakts import ArkitektFakts
from arkitekt.apps.rekuest import ArkitektRekuest
from fakts.discovery.qt.selectable_beacon import (
    QtSelectableDiscovery,
    SelectBeaconWidget,
)
from fakts.grants.meta.failsafe import FailsafeGrant
from mikro_napari.widgets.main_widget import MikroNapariWidget
from fakts.grants.remote.retrieve import RetrieveGrant
from fakts.grants import CacheGrant
import napari
import argparse
from skimage.data import astronaut

from mikro_napari.widgets.sidebar.sidebar import SidebarWidget
import os
from fakts.discovery.static import StaticDiscovery
from herre import Herre
from herre.grants import CacheGrant as HerreCacheGrant
from herre.grants.oauth2.refresh import RefreshGrant
from herre.grants.fakts import FaktsGrant
from herre.grants.fakts.fakts_login_screen import FaktsQtLoginScreen, LoginWidget
from arkitekt.builders import publicqt

def main(**kwargs):

    os.environ["NAPARI_ASYNC"] = "1"

    identifier = "github.io.jhnnsrs.mikro_napari"
    version = "v0.0.1"

    viewer = napari.Viewer()


    app = publicqt(identifier, version, parent=viewer.window.qt_viewer)

    widget = MikroNapariWidget(viewer, app, **kwargs)
    sidebar = SidebarWidget(viewer, app, **kwargs)
    viewer.window.add_dock_widget(widget, area="left", name="Mikro")
    viewer.window.add_dock_widget(sidebar, area="right", name="Mikro")
    # viewer.add_image(astronaut(), name="astronaut")

    with app:
        napari.run()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", help="Which config file to use", default="bergen.yaml", type=str
    )
    args = parser.parse_args()

    main(config_path=args.config)
