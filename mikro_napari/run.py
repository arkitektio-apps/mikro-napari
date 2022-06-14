from mikro_napari.widgets.main_widget import MikroNapariWidget

import napari
import argparse


def main(**kwargs):
    viewer = napari.Viewer()
    widget = MikroNapariWidget(viewer, **kwargs)
    viewer.window.add_dock_widget(widget, area="left", name="Mikro")
    napari.run()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", help="Which config file to use", default="bergen.yaml", type=str
    )
    args = parser.parse_args()

    main(config_path=args.config)
