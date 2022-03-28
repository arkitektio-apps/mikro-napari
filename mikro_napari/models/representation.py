from typing import Dict, List, Optional
from qtpy import QtCore
from koil.qt import QtRunner, QtGeneratorRunner
from mikro.api.schema import InputVector
from mikro_napari.api.schema import (
    DetailLabelFragment,
    ROIFragment,
    RepresentationFragment,
    ListRepresentationFragment,
    RepresentationVariety,
    RoiTypeInput,
    Watch_roisSubscriptionRois,
    aget_label_for,
    aget_rois,
    awatch_rois,
    create_roi,
    delete_roi,
)

from napari.layers.shapes._shapes_constants import Mode

DESIGN_MODE_MAP = {
    Mode.ADD_RECTANGLE: RoiTypeInput.RECTANGLE,
    Mode.ADD_ELLIPSE: RoiTypeInput.ELLIPSIS,
    Mode.ADD_LINE: RoiTypeInput.LINE,
}


class RepresentationQtModel(QtCore.QObject):
    def __init__(self, app, viewer, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app = app
        self.viewer = viewer

        self.get_rois_query = QtRunner(aget_rois)
        self.get_rois_query.returned.connect(self.on_rois_loaded)

        self.watch_rois_subscription = QtGeneratorRunner(awatch_rois)
        self.watch_rois_subscription.yielded.connect(self.on_rois_updated)

        self.get_label_query = QtRunner(aget_label_for)
        self.get_label_query.returned.connect(self.on_label_loaded)
        self.get_label_query.errored.connect(print)

        self._active_representation = None
        self._watchroistask = None
        self._getroistask = None
        self._getlabeltask = None

        self._image_layer = None
        self._roi_layer = None
        self._roi_state: Dict[str, ROIFragment] = {}

    @property
    def active_representation(self) -> Optional[RepresentationFragment]:
        return self._active_representation

    @active_representation.setter
    def active_representation(self, value: RepresentationFragment):
        if self._getroistask and not self._getroistask.done():
            self._getroistask.cancel()
            self._getroistask.result(swallow_cancel=True)

        if self._watchroistask and not self._watchroistask.done():
            self._watchroistask.cancel()
            self._watchroistask.result(swallow_cancel=True)

        self._getroistask = self.get_rois_query.run(representation=value.id)
        self._watchroistask = self.watch_rois_subscription.run(representation=value.id)
        self._active_representation = value

        if self._image_layer:
            self._image_layer.data = value.data.transpose(*list("tzxyc"))
        else:
            self._image_layer = self.viewer.add_image(
                value.data.transpose(*list("tzxyc"))
            )
            self._image_layer.mouse_drag_callbacks.append(self.on_drag_image_layer)

        self._image_layer.name = value.name

    def on_image_loaded(self, rep: RepresentationFragment):
        """Shows beauitful Images

        Loads the image into the viewer

        Args:
            rep (RepresentationFragment): The Image
        """
        self.active_representation = rep

    def on_label_loaded(self, label: DetailLabelFragment):
        """Shows beauitful Images

        Loads the image into the viewer

        Args:
            rep (RepresentationFragment): The Image
        """
        print("This is the label", label)

    def on_rois_loaded(self, rois: List[ROIFragment]):
        self.roi_state = {roi.id: roi for roi in rois}
        self.update_roi_layer()

    def on_rois_updated(self, ev: Watch_roisSubscriptionRois):
        if ev.create:
            self.roi_state[ev.create.id] = ev.create

        if ev.delete:
            del self.roi_state[ev.delete]

        self.update_roi_layer()

    def on_drag_image_layer(self, layer, event):
        while event.type != "mouse_release":
            yield

        print("Fired")
        print(self.active_representation.variety)
        if self.active_representation.variety == RepresentationVariety.MASK:
            if self._getlabeltask and not self._getlabeltask.done():
                self._getlabeltask.cancel(wait=True)

            value = layer.get_value(event.position)
            print(value)
            if value:
                self._getlabeltask = self.get_label_query.run(
                    representation=self.active_representation.id, instance=int(value)
                )

    def on_drag_roi_layer(self, layer, event):
        while event.type != "mouse_release":
            yield

        print("Fired")

        if layer.mode in DESIGN_MODE_MAP:
            if len(self._roi_layer.data) > len(self.roi_state.items()):
                create_roi(
                    representation=self._active_representation.id,
                    vectors=InputVector.list_from_numpyarray(self._roi_layer.data[-1]),
                    type=DESIGN_MODE_MAP[layer.mode],
                )

        if len(self._roi_layer.data) < len(self.roi_state.items()):
            there_rois = set([f for f in self._roi_layer.features[0]])
            state_rois = set(self.roi_state.keys())
            difference_rois = state_rois - there_rois
            for roi_id in difference_rois:
                delete_roi(roi_id)

    def update_roi_layer(self):

        if not self._roi_layer:

            self._roi_layer = self.viewer.add_shapes()
            self._roi_layer.mouse_drag_callbacks.append(self.on_drag_roi_layer)

        self._roi_layer.data = []
        self._roi_layer.name = f"ROIs for {self._active_representation.name}"

        self._roi_layer.add(
            [r.vector_data for key, r in self.roi_state.items()],
            shape_type=[r.type.value.lower() for key, r in self.roi_state.items()],
            edge_width=1,
            edge_color="white",
            face_color=[r.creator.color for key, r in self.roi_state.items()],
        )

        self._roi_layer.features = [
            [r.id, r.creator.id] for key, r in self.roi_state.items()
        ]
