from arkitekt import App
from .manifest import identifier, version, logo
from arkitekt.builders import publicscheduleqt
from qtpy import QtCore

global_app = None


def get_app_or_build_for_widget(widget) -> App:
    """Get the app for the widget or build a new one if it does not exist
    This is a necessary step because we need to attach the app to an existing
    widget. (As opposed to building a new app for each widget) Preferabley
    this would attach directly to the qtviewer, but that is currently deprecated"""
    print("Accessing Global App")
    global global_app
    if global_app is None:
        settings = QtCore.QSettings("napari", f"{identifier}:{version}")

        global_app = publicscheduleqt(
            identifier, version, parent=widget, logo=logo, settings=settings
        )
    return global_app
