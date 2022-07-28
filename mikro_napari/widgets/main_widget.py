from tracemalloc import Statistic
import napari
from arkitekt.compositions.base import Arkitekt
from arkitekt.structures.registry import StructureRegistry
from arkitekt.widgets import SearchWidget
from fakts.fakts import Fakts
from fakts.grants.meta.failsafe import FailsafeGrant
from fakts.grants.remote.claim import ClaimGrant
from fakts.grants.remote.public_redirect_grant import PublicRedirectGrant
from koil.qt import QtRunner
from mikro.api.schema import (
    RepresentationVariety,
    Search_representationQuery,
    afrom_xarray,
    from_xarray,
)
from mikro_napari.api.schema import (
    RepresentationFragment,
    aget_representation,
)
from qtpy import QtWidgets
from qtpy import QtCore
from mikro.arkitekt import ConnectedApp
from koil.composition.qt import QtPedanticKoil
from herre.fakts import FaktsHerre
from arkitekt.qt.magic_bar import AppState, MagicBar
from arkitekt.qt.builders import QtInLoopBuilder
from mikro_napari.models.representation import RepresentationQtModel
from mikro_napari.widgets.dialogs.open_image import OpenImageDialog
from fakts.grants.remote.base import StaticDiscovery
import xarray as xr


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
    "@mikro/representation",
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
                        PublicRedirectGrant(name="Napari", scopes=["openid"]),
                    ]
                ),
                assert_groups={"mikro", "arkitekt"},
            ),
            herre=FaktsHerre(),
        )
        self.viewer.window.app = self.app

        self.app.enter()

        self.magic_bar = MagicBar(self.app, dark_mode=True)
        self.magic_bar.app_up.connect(self.on_app_up)
        self.magic_bar.app_down.connect(self.on_app_down)

        self.representation_controller = RepresentationQtModel(self.app, self.viewer)

        self.upload_task = QtRunner(afrom_xarray)
        self.upload_task.errored.connect(self.on_error)
        self.upload_task.returned.connect(
            self.representation_controller.on_image_loaded
        )

        self.task = None
        self.stask = None

        self.open_image_button = QtWidgets.QPushButton("Open Image")
        self.open_image_button.clicked.connect(self.cause_image_load)
        self.open_image_button.setEnabled(False)

        self.upload_image_button = QtWidgets.QPushButton("Upload Image")
        self.upload_image_button.clicked.connect(self.cause_upload)
        self.upload_image_button.setEnabled(False)

        self.active_non_mikro_layers = []
        self.active_mikro_layers = []
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.open_image_button)
        self.layout.addWidget(self.upload_image_button)
        self.layout.addWidget(self.magic_bar)

        self.setWindowTitle("My Own Title")
        self.setLayout(self.layout)

        self.viewer.layers.selection.events.active.connect(self.on_selection_changed)

        self.app.arkitekt.register(builder=QtInLoopBuilder, interfaces=["show"])(
            self.representation_controller.on_image_loaded
        )

        self.app.arkitekt.register(builder=QtInLoopBuilder, interfaces=["show"])(
            self.representation_controller.show_images
        )

        self.app.arkitekt.register(interfaces=["producer"])(self.upload_layer)

    def on_app_up(self):
        self.open_image_button.setEnabled(True)
        self.on_selection_changed()  # TRIGGER ALSO HERE

    def on_app_down(self):
        self.open_image_button.setEnabled(False)

    def on_selection_changed(self):
        print("Selection Changed")
        self.active_non_mikro_layers = [
            layer
            for layer in self.viewer.layers.selection
            if not layer.metadata.get("mikro")
        ]
        self.active_mikro_layers = [
            layer
            for layer in self.viewer.layers.selection
            if layer.metadata.get("mikro")
        ]

        print(self.active_mikro_layers, self.active_mikro_layers)
        if self.active_non_mikro_layers and not self.active_mikro_layers:
            self.upload_image_button.setText(f"Upload Layer")
            self.upload_image_button.setEnabled(self.magic_bar.state == AppState.UP)
        else:
            self.upload_image_button.setText(f"Upload Layer")
            self.upload_image_button.setEnabled(False)

    async def upload_layer(self, name: str = "") -> RepresentationFragment:
        """Upload Napari Layer

        Upload the current image to the server.

        Args:
            name (str, optional): Overwrite the layer name. Defaults to None.

        Returns:
            RepresentationFragment: The uploaded image
        """
        if not self.active_non_mikro_layers:
            raise Exception("No active layer")

        image_layer = self.active_non_mikro_layers[0]

        variety = RepresentationVariety.VOXEL

        if image_layer.ndim == 2:
            if image_layer.rgb:
                xarray = xr.DataArray(image_layer.data, dims=list("xyc"))
                variety = RepresentationVariety.RGB
            else:
                xarray = xr.DataArray(image_layer.data, dims=list("xy"))

        if image_layer.ndim == 3:
            xarray = xr.DataArray(image_layer.data, dims=list("zxy"))

        if image_layer.ndim == 4:
            xarray = xr.DataArray(image_layer.data, dims=list("tzxy"))

        if image_layer.ndim == 5:
            xarray = xr.DataArray(image_layer.data, dims=list("tzxyc"))

        return await afrom_xarray(
            xarray, name=name or image_layer.name, variety=variety
        )

    def cause_upload(self):
        for image_layer in self.active_non_mikro_layers:
            variety = RepresentationVariety.VOXEL

            if image_layer.ndim == 2:
                if image_layer.rgb:
                    xarray = xr.DataArray(image_layer.data, dims=list("xyc"))
                    variety = RepresentationVariety.RGB
                else:
                    xarray = xr.DataArray(image_layer.data, dims=list("xy"))

            if image_layer.ndim == 3:
                xarray = xr.DataArray(image_layer.data, dims=list("zxy"))

            if image_layer.ndim == 4:
                xarray = xr.DataArray(image_layer.data, dims=list("tzxy"))

            if image_layer.ndim == 5:
                xarray = xr.DataArray(image_layer.data, dims=list("tzxyc"))

            self.upload_task.run(xarray, name=image_layer.name, variety=variety)
            self.upload_image_button.setText(f"Uploading {image_layer.name}...")
            self.upload_image_button.setEnabled(False)

    def on_upload_finished(self, image):
        self.on_selection_changed()

    def cause_image_load(self):

        rep_dialog = OpenImageDialog(self)
        x = rep_dialog.exec()
        print(x)
        if x:
            self.representation_controller.active_representation = (
                rep_dialog.selected_representation
            )

    def on_error(self, error):
        print(error)
