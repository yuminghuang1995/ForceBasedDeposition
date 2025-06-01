# Force-Based Adaptive Deposition in Multi-Axis Additive Manufacturing: Low Porosity for Enhanced Strength

[![Watch the video](./my-cover.png)](https://youtu.be/i_Gpd3_gRxA)

![Pipeline Figure](Figure_pipline.png)

This paper presents a force-based adaptive deposition method for controlling porosity in filament-based multi-axis additive manufacturing. Porosity often arises in 3D printed structures with curved layers due to non-uniform layer thickness, unstable material extrusion, and significant curvature variations across different regions of a model. Our closed-loop control approach dynamically adjusts the local material deposition rate by modulating the printer head motion in response to force feedback while maintaining a constant extrusion speed.

This project contains data for all models in paper, including obj files in **models** folder.

The geometry-based and force-based adaptive deposition files are under the **toolpaths** folder. The format is:

\# List of geometric vertices, with **(x, y, z)** coordinates.

v 6.552 	46.460 	21.690

v ...

...

\# List of vertex normals in **(nx, ny, nz)** form.

vn 0.099 	0.037 	0.994

vn ...

...

\# List of extrusion volume corresponding to every vertex in **(e)** form.

e 0.219

e ...

...



