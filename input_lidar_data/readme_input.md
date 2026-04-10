# For Input LIDAR Data

The raw data files exceed standard repository limits. Data of Patna, Bihar was used in this project.

---

## Data Overview: Patna, Bihar
Patna’s unique geography—situated at the confluence of the Ganges, Gandak, and Son rivers—makes high-resolution terrain data critical for disaster mitigation.

### 1. Dataset Components
* **LiDAR Point Clouds (`.LAS` / `.LAZ`):** Raw 3D point data captured via aerial surveys over the Patna metropolitan area and surrounding floodplains.
* **DEM (Digital Elevation Model):** A 1-meter resolution bare-earth raster derived from LiDAR ground returns, used to identify low-lying, flood-prone zones.
* **Orthophotos (`.TIF`):** High-resolution, georectified aerial imagery used for structural damage assessment and land-use mapping.
* **Vector Layers (`.GDB`):** Esri File Geodatabase containing Patna's ward boundaries, drainage networks, and critical infrastructure (hospitals, schools).

---

## How LiDAR Works
LiDAR (Light Detection and Ranging) is a remote sensing method that uses light in the form of a pulsed laser to measure ranges (variable distances) to the Earth.

1.  **Pulse Emission:** A laser scanner mounted on an aircraft sends thousands of light pulses per second toward the ground.
2.  **Return Signal:** The pulses bounce off objects (trees, buildings, or the ground) and return to the sensor.
3.  **XYZ Calculation:** By measuring the time it takes for each pulse to return, the system calculates the exact **3D coordinates ($X, Y, Z$)** of every reflection point.
4.  **Point Cloud:** The result is a dense "cloud" of points that perfectly mimics the physical environment.

---

## Data Processing Workflow

### 1. ArcGIS Pro Integration
The initial heavy-lifting and data management are performed using the **ArcGIS Pro 3D Analyst** extension:
* **LAS Datasets:** We use LAS Datasets to visualize Patna's terrain without converting the raw data, allowing for immediate filtering of noise (e.g., birds, atmospheric interference).
* **Ground Classification:** Automated algorithms separate "Ground" points from "Non-Ground" (Patna's dense urban canopy) to create the bare-earth DEM.
* **Hydrological Analysis:** Using the `Fill` and `Flow Accumulation` tools to predict where water will collect in the city during a monsoon surge.

### 2. Python Processing Engine
Once the terrain models are generated, a custom Python pipeline (as seen in `main.py`) automates the visualization and intelligence extraction:

* **Surface Modeling:** Uses `rasterio` and `matplotlib` to generate **Hillshades**, which provide a 3D-like visual of Patna's topography to identify embankment breaches.
* **3D Mesh Rendering:** The `PyVista` library converts the DEM into a structured grid, allowing users to rotate and inspect the 3D landscape of affected wards.
* **Infrastructure Overlay:** `GeoPandas` reads the `.gdb` layers to overlay the city's road network directly onto the elevation data, identifying which evacuation routes will be submerged first.
