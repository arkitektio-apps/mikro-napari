
from tracemalloc import Statistic
import napari
from arkitekt.compositions.base import Arkitekt
from arkitekt.structures.registry import StructureRegistry
from arkitekt.widgets import SearchWidget
from fakts.fakts import Fakts
from fakts.grants.meta.failsafe import FailsafeGrant
from fakts.grants.remote.claim import ClaimGrant
from fakts.grants.remote.public_redirect_grant import PublicRedirectGrant
from mikro.api.schema import Search_representationQuery
from mikro_napari.api.schema import (
    RepresentationFragment,
    aget_representation,
)
from qtpy import QtWidgets
from qtpy import QtCore
from mikro.arkitekt import ConnectedApp
from koil.composition.qt import QtPedanticKoil
from herre.fakts import FaktsHerre
from arkitekt.qt.magic_bar import MagicBar
from arkitekt.qt.builders import QtInLoopBuilder
from mikro_napari.models.representation import RepresentationQtModel
from mikro_napari.widgets.dialogs.open_image import OpenImageDialog
from fakts.grants.remote.base import StaticDiscovery

SMLM_REPRESENTATIONS = SearchWidget(
    query="""
    query Search($search: String){
        options: representations(name: $search, tags: ["smlm"]){
            value: id
            label: name
        }
    }
    """
)  #


MULTISCALE_REPRESENTATIONS = SearchWidget(
    query="""
        query Search($search: String){
            options: representations(name: $search, derivedTags: ["multiscale"]){
                value: id
                label: name
            }
        }
        """
)

stregistry = StructureRegistry()


stregistry.register_as_structure(
    RepresentationFragment,
    "representation",
    aget_representation,
    default_widget=SearchWidget(query=Search_representationQuery.Meta.document),
)


class MikroNapariWidget(QtWidgets.QWidget):
    emit_image: QtCore.Signal = QtCore.Signal(object)

    def __init__(self, viewer: napari.Viewer, *args, **kwargs):
        super(MikroNapariWidget, self).__init__(*args, **kwargs)
        self.viewer = viewer

        self.app = ConnectedApp(
            koil=QtPedanticKoil(uvify=False, parent=self),
            arkitekt=Arkitekt(structure_registry=stregistry),
            fakts=Fakts(
                subapp="napari",
                grant=FailsafeGrant(
                        grants=[
                            ClaimGrant(
                        client_id="DSNwVKbSmvKuIUln36FmpWNVE2KrbS2oRX0ke8PJ",
                        client_secret="Gp3VldiWUmHgKkIxZjL2aEjVmNwnSyIGHWbQJo6bWMDoIUlBqvUyoGWUWAe6jI3KRXDOsD13gkYVCZR0po1BLFO9QT4lktKODHDs0GyyJEzmIjkpEOItfdCC4zIa3Qzu",
                        discovery=StaticDiscovery(base_url="http://localhost:8019/f/"),
                        graph="localhost",
                        ),  
                        PublicRedirectGrant(name="Napari", scopes=["openid"]),
                    ]
                ),
                force_refresh=True,
                assert_groups={"mikro", "arkitekt"},
            ),
            herre=FaktsHerre(),
        )
        self.viewer.window.app = self.app

        self.app.enter()

        self.magic_bar = MagicBar(self.app, dark_mode=True)

        self.representation_controller = RepresentationQtModel(self.app, self.viewer)

        self.task = None
        self.stask = None

        self.open_image = QtWidgets.QPushButton("Open Image")
        self.open_image.clicked.connect(self.cause_image_load)

        self.upload_image = QtWidgets.QPushButton("Upload Image")
        self.upload_image.clicked.connect(self.cause_upload)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.open_image)
        self.layout.addWidget(self.upload_image)
        self.layout.addWidget(self.magic_bar)

        self.setWindowTitle("My Own Title")
        self.setLayout(self.layout)

        self.app.arkitekt.register(builder=QtInLoopBuilder)(
            self.representation_controller.on_image_loaded
        )

    def cause_upload(self):
        with open("napi.json", "w") as f:
            f.write(self.app.json(exclude_none=True, indent=4))

    def cause_image_load(self):

        rep_dialog = OpenImageDialog(self)
        x = rep_dialog.exec()
        if x:
            self.representation_controller.active_representation = (
                rep_dialog.selected_representation
            )

    def on_error(self, error):
        print(error)
