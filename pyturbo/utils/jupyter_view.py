from typing import Any, Dict, Iterable, Union

import numpy as np
from cosapp.systems import System
from OCC.Core.TopoDS import TopoDS_Shape


class JupyterViewable:
    def jupyter_view(
        self,
        *,
        required: Union[Iterable[Union[System, str]], str] = "*",
        options: Dict[str, Dict[str, Any]] = None,
        **kwargs
    ):
        try:
            from pythonocc_helpers.render import JupyterThreeJSRenderer
        except ImportError:
            raise ImportError("Please install 'pythonocc_helpers' before using this function")

        super(System, self).__setattr__("_renderer", None)
        self._renderer = JupyterThreeJSRenderer(
            view_size=(1800, 800),
            camera_target=(1.0, 0.0, 0.0),
            camera_position=(-2.0, 1.0, 2.0),
            **kwargs
        )

        if options is None:
            options = {}

        def get_shape_options(name):
            split_name = name.split(".")
            names = [split_name[0]]
            for i in range(1, len(split_name)):
                names.append(".".join((names[-1], split_name[i])))
            opt = {}
            for n in names:
                opt.update(options.get(n, {}))
            return opt

        def add_to_renderer(name, shape):
            if isinstance(shape, TopoDS_Shape):
                opt = get_shape_options(name)
                self._renderer.add_shape(shape, uid=name, **opt)
            elif isinstance(shape, dict):
                for n, s in shape.items():
                    add_to_renderer(".".join((name, n)), s)
            else:
                raise TypeError("Unsupported type")

        for name, shape in self._to_occt().items():
            add_to_renderer(name, shape)

        return self._renderer.show()

    def update_jupyter_view(self):
        self._renderer.update_shape(self._to_occt(), uid=self.name)


def add_nacelle_brand(nacelle_geom: System, renderer, brand_path: str):
    try:
        from pythreejs import ImageTexture, MeshStandardMaterial
    except ImportError:
        raise ImportError("Please install 'pythonocc_helpers' before using this function")

    logo = ImageTexture(imageUri=brand_path)
    renderer.add_shape(
        nacelle_geom._brand_shape(),
        uid="brand",
        plot_edges=False,
        face_material=MeshStandardMaterial(
            map=logo,
            transparent=True,
            side="DoubleSide",
        ),
        uv_rotation=np.pi / 2,
    )
