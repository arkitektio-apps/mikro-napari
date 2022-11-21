from arkitekt.apps.fakts import ArkitektFakts
from mikro_napari.widgets.main_widget import MikroNapariWidget
from arkitekt.apps.connected import ConnectedApp
from arkitekt.apps.rekuest import ArkitektRekuest
from fakts.fakts import Fakts
from fakts.grants.meta.failsafe import FailsafeGrant
from fakts.grants.remote.public_redirect_grant import PublicRedirectGrant
from herre.fakts.herre import FaktsHerre
from koil.composition.qt import QtPedanticKoil
from fakts.discovery.qt.selectable_beacon import (
    QtSelectableDiscovery,
    SelectBeaconWidget,
)
from fakts.grants.remote.static import StaticGrant
from fakts.grants.remote.retrieve import RetrieveGrant
from fakts.discovery import StaticDiscovery
from fakts.grants import CacheGrant


class ArkitektPluginWidget(MikroNapariWidget):
    def __init__(self, viewer: "napari.viewer.Viewer"):

        x = SelectBeaconWidget()

        app = ConnectedApp(
            koil=QtPedanticKoil(parent=self),
            rekuest=ArkitektRekuest(),
            fakts=ArkitektFakts(
                grant=CacheGrant(
                    cache_file="mikro_napari_cache.json",
                    grant=FailsafeGrant(
                        grants=[
                            RetrieveGrant(
                                identifier="jhnnsrs.github.io/mikro_napari",
                                version="v0.0.1",
                                redirect_uri="http://localhost:6767",
                                discovery=StaticDiscovery(
                                    base_url="http://localhost:8000/f/"
                                ),
                            ),
                        ]
                    ),
                ),
                assert_groups={"mikro", "rekuest"},
            ),
            herre=FaktsHerre(),
        )

        super(ArkitektPluginWidget, self).__init__(viewer, app)

        app.enter()
