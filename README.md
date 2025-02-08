# Force Based Adaptive Deposition

This paper presents a force-based adaptive deposition method for controlling porosity in filament-based multi-axis additive manufacturing. Porosity often arises in 3D printed structures with curved layers due to non-uniform layer thickness, unstable material extrusion, and significant curvature variations across different regions of a model. Our closed-loop control approach dynamically adjusts the local material deposition rate by modulating the printer head motion in response to force feedback while maintaining a constant extrusion speed.

This project contains data for all models in paper, including obj files in **models** folder.

The geometry-based and force-based adaptive deposition files are under the **toolpaths** folder. The format is:

List of geometric vertices, with (x, y, z) coordinates.

v 0.123 0.234 0.345 1.0

v ...

...

List of vertex normals in (x,y,z) form.

vn 0.707 0.000 0.707

vn ...

...

Extrusion volume in (e) form.

e 0.32

e ...

...

