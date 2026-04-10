# INFRASCAN: AI-Powered Post-Flood Reconstruction Intelligence 

**INFRASCAN** is a geospatial AI platform designed for rapid post-flood damage assessment and resilient reconstruction. By integrating **LiDAR point clouds**, drone imagery, and Machine Learning, it provides a unified intelligence layer for optimizing disaster response and floodplain-aware rebuilding.

---

## System Architecture & LiDAR Pipeline

### Data Ingestion & ArcGIS Managed Storage
* **LiDAR Formats:** Native support for `.LAS`, `.LAZ` (compressed), and `.ZLAS`.
* **ArcGIS LAS Dataset:** The system utilizes the **LAS Dataset** structure in ArcGIS Pro to manage billions of points across multiple flight lines without conversion, enabling rapid spatial indexing and filtered 3D visualization.

### ArcGIS Processing Workflow
Terrain intelligence is derived through a rigorous **ArcGIS Pro 3D Analyst** pipeline:

1.  **Point Classification:** Ground points are separated from non-ground (buildings, vegetation) using the `Classify LAS Ground` tool.
2.  **Surface Extraction:**
    * **DEM (Digital Elevation Model):** Generated via `LAS Dataset to Raster`, filtered for "Ground" points to create a bare-earth surface.
    * **DSM (Digital Surface Model):** Created using "First Return" points to capture infrastructure heights and canopy.
3.  **Hydrological Change Detection:** By running the `Surface Difference` tool between pre-flood and post-flood DEMs, the system quantifies:
    * **Scouring & Erosion:** Volume of soil lost at riverbanks.
    * **Sedimentation:** Depth of silt deposited in urban sectors.
4.  **Flood Simulation:** Leverages **GPU-based Flood Simulation** in ArcGIS to run shallow water equations directly on the LiDAR-derived mesh, predicting water accumulation and flow velocity.

---

## Technical Implementation (Data Analysis and Visualization)

The core processing engine utilizes a robust Python stack to automate geospatial visualization and analysis:

* **Surface Modeling:** Uses `rasterio` and `matplotlib.colors.LightSource` to generate hillshades and digital elevation visualizations.
* **Vector Analysis:** Employs `geopandas` and `fiona` to read File Geodatabases (`.gdb`) and overlay infrastructure layers (roads, bridges) onto the LiDAR-derived DEM.
* **3D Mesh Generation:** Utilizes `pyvista.StructuredGrid` to convert grid-based elevation data into interactive 3D terrain meshes for structural inspection.
* **Point Cloud Visualization:** Uses `laspy` for direct extraction of $X, Y, Z$ coordinates from LiDAR files, rendering raw point clouds to identify debris and blockages.

---

## Features & User Roles

* **Government / Military**
  * LiDAR Situational Viewer: High-resolution 3D terrain monitoring.
  * Dynamic Routing: AI-optimized pathfinding for rescue and logistics.
  * Fiscal Dashboards: Real-time tracking of reconstruction budgets and resources.
* **NGOs / Relief Organizations**
  * Resource Request Boards: Centralized hub for food, medical, and shelter logistics.
  * Volunteer Deployment Maps: Geospatial tracking of personnel and relief camps.
* **Communities (Public)**
  * Damage Visualization: Interactive maps showing safe zones and affected areas.
  * Geo-tagged Media Uploads: Ground-truth data collection (photos/videos) for AI verification.
* **Investors / Donors (Stakeholder)**
  * Milestone-based Funding Logs: Transparency in fund allocation and project progress.
  * Transparency Dashboards: Real-time impact metrics and completion reports.
