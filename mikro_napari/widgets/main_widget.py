from typing import List

import napari
from arkitekt.compositions.base import Arkitekt
from arkitekt.structures.registry import StructureRegistry
from arkitekt.widgets import SearchWidget
from fakts.fakts import Fakts
from koil.qt import QtRunner
from mikro_napari.api.schema import (
    ROIFragment,
    RepresentationFragment,
    aget_representation,
)
from qtpy import QtWidgets
from fakts.grants.qt.qtbeacon import QtSelectableBeaconGrant, SelectBeaconWidget
from qtpy import QtCore
from mikro.arkitekt import ConnectedApp
from koil.composition.qt import QtPedanticKoil
from herre.fakts import FaktsHerre
from arkitekt.qt.magic_bar import MagicBar
from arkitekt.qt.builders import QtInLoopBuilder
from mikro_napari.models.representation import RepresentationQtModel
from mikro_napari.widgets.dialogs.open_image import OpenImageDialog

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
    RepresentationFragment, "representation", aget_representation
)


class MikroNapariWidget(QtWidgets.QWidget):
    emit_image: QtCore.Signal = QtCore.Signal(object)

    def __init__(self, viewer: napari.Viewer, *args, **kwargs):
        super(MikroNapariWidget, self).__init__(*args, **kwargs)
        self.viewer = viewer

        self.app = ConnectedApp(
            koil=QtPedanticKoil(uvify=False, auto_connect=True, parent=self),
            arkitekt=Arkitekt(structure_registry=stregistry),
            fakts=Fakts(
                subapp="napari",
                grants=[
                    QtSelectableBeaconGrant(widget=SelectBeaconWidget(parent=self))
                ],
                assert_groups={"mikro"},
            ),
            herre=FaktsHerre(login_on_enter=False),
        )
        self.app.koil.connect()

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
        active_layers = [layer for layer in self.viewer.layers if layer.active]

    def cause_image_load(self):

        rep_dialog = OpenImageDialog(self)
        x = rep_dialog.exec()
        if x:
            self.representation_controller.active_representation = (
                rep_dialog.selected_representation
            )

    def on_error(self, error):
        print(error)
