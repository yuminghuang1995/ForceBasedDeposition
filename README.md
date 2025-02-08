# Force Based Adaptive Deposition

This paper presents a force-based adaptive deposition method for controlling porosity in filament-based multi-axis additive manufacturing. Porosity often arises in 3D printed structures with curved layers due to non-uniform layer thickness, unstable material extrusion, and significant curvature variations across different regions of a model. Our closed-loop control approach dynamically adjusts the local material deposition rate by modulating the printer head motion in response to force feedback while maintaining a constant extrusion speed.

This project contains data for all models in paper, including obj files in **models** folder.
The geometry-based and force-based deposition files are under the **toolpaths** folder. The format is:

Three-dimensional coordinates of nodes in the toolpath: **x y z**.

Normal of nodes in the toolpath: **nx ny nz**.

Extrusion volume: **e**.

Layer number: **l**.
