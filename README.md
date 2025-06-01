# Force-Based Adaptive Deposition in Multi-Axis Additive Manufacturing: Low Porosity for Enhanced Strength

[![Watch the video](./video_cover.png)](https://youtu.be/i_Gpd3_gRxA)

**Force-Based Adaptive Deposition for Curved 3D Printing**

This project addresses the challenge of achieving consistent material deposition in filament-based multi-axis additive manufacturing when printing curved layers. In conventional planar 3D printing, a fixed layer height allows a constant optimal extrusion rate and print speed, ensuring uniform material distribution. However, when layers follow complex curved geometries, local layer thickness varies continuously and deposition angles change across the surface. These variations commonly lead to under-filled regions, visible as porosity, and weaken inter-layer bonding. As porosity errors accumulate over successive layers—particularly in models with many curved layers—parts become prone to reduced mechanical strength, delamination, or fracture.

**Adaptive Deposition through Real-Time Force Sensing**

![Pipeline Figure](Figure_pipline.png)

To overcome these issues, we propose a force-based sensing approach that integrates a compact force sensor into the printhead. By monitoring the resistant force exerted by freshly deposited material in real time, we establish a closed-loop control strategy that dynamically adjusts the printhead feedrate while keeping the filament feed rate constant. Rather than changing extrusion speed—which often suffers from delays due to stepper motor response limits or pressure changes in the melt cavity—our method regulates the printhead’s motion to maintain a target resistant force during printing. Whenever the sensed force falls below the calibrated reference (indicating under-extrusion or sparse filling), the system slows down the printhead locally to deposit extra material. Conversely, when the force exceeds the reference (suggesting over-extrusion), the printhead speeds up to reduce local deposition. This continuous feedback loop ensures more uniform extrusion, minimizes void formation, and enhances filament bonding in curved regions.

**Experimental Validation and Mechanical Strength Improvement**



We implemented the force-based adaptive deposition strategy on a UR5e-based multi-axis printing platform, synchronized with a Duet 3D control board. Physical experiments include printing several test models—such as the Bracket, Bridge, Topology-Optimized block, and Bunny-Head—using both geometry-driven and force-based methods. Tensile testing and SEM imaging reveal that force-based prints consistently achieve higher failure loads and exhibit significantly reduced internal voids compared to purely geometry-based approaches. For instance, on the Topology-optimized model with 359 curved layers, our method yields up to 72% higher failure load than geometry-based curved slicing when normalized by weight. Moreover, when simulating nozzle blockages or missing material segments, force-based control effectively compensates for these imperfections in subsequent layers—demonstrating robustness against unpredictable extrusion errors.

**Repository Structure** 

**Models**: Includes all 3D geometry files (e.g., Bridge, Bracket, Topo-Opt, Bunny-Head) used for printing experiments.

**Toolpaths**: Contains two sets of path definitions for each model. One set follows pure geometry-based planning, while the other incorporates force-based adaptive deposition. Each file lists vertex coordinates, normals, and corresponding extrusion volumes (computed from local surface geometry). The format is:

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

**Conclusion**
By combining geometry-based extrusion estimates with real-time force feedback, this force-based adaptive deposition method significantly reduces porosity and boosts mechanical strength in curved 3D printing, offering a robust solution for filament-based multi-axis additive manufacturing.


