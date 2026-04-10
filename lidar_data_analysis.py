import os
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import rasterio
import geopandas as gpd
import fiona
from matplotlib.colors import LightSource

try:
    import pyvista as pv
    HAS_PYVISTA = True
except:
    HAS_PYVISTA = False

try:
    import laspy
    HAS_LAS = True
except:
    HAS_LAS = False


script_dir = os.path.dirname(os.path.abspath(__file__))

base_dir = os.path.join(script_dir, "79B6SE")
gdb_path = os.path.join(base_dir, "79B6SE.gdb")
dem_dir = os.path.join(base_dir, "DEM")
ortho_dir = os.path.join(base_dir, "ORTHO")

output_dir = os.path.join(script_dir, "outputs")
os.makedirs(output_dir, exist_ok=True)

print("Base directory:", base_dir)


print("\nLoading DEM...")

dem_path = None

for root, dirs, files in os.walk(dem_dir):
    for file in files:
        if file.lower().endswith(".tif"):
            dem_path = os.path.join(root, file)
            break
    if dem_path:
        break

if dem_path is None:
    raise FileNotFoundError("No DEM .tif file found inside DEM folder.")

print("DEM found at:", dem_path)

with rasterio.open(dem_path) as src:
    dem = src.read(1)
    dem_profile = src.profile
    transform = src.transform

print("DEM loaded successfully.")

plt.figure(figsize=(8,6))
plt.imshow(dem, cmap="terrain")
plt.colorbar(label="Elevation (m)")
plt.title("DEM")
plt.savefig(os.path.join(output_dir, "dem.png"))
plt.close()


print("Generating hillshade...")

ls = LightSource(azdeg=315, altdeg=45)
hillshade = ls.hillshade(dem, vert_exag=1)

plt.figure(figsize=(8,6))
plt.imshow(hillshade, cmap="gray")
plt.title("Hillshade")
plt.savefig(os.path.join(output_dir, "hillshade.png"))
plt.close()


if os.path.exists(ortho_dir):

    ortho_path = None

    for root, dirs, files in os.walk(ortho_dir):
        for file in files:
            if file.lower().endswith(".tif"):
                ortho_path = os.path.join(root, file)
                break
        if ortho_path:
            break

    if ortho_path:
        print("Loading orthophoto...")

        with rasterio.open(ortho_path) as src:
            ortho = src.read([1,2,3])
            ortho = np.transpose(ortho, (1,2,0))

        plt.figure(figsize=(8,6))
        plt.imshow(ortho)
        plt.title("Orthophoto")
        plt.savefig(os.path.join(output_dir, "orthophoto.png"))
        plt.close()


if os.path.exists(gdb_path):
    print("\nReading GDB layers...")
    layers = fiona.listlayers(gdb_path)
    print("Layers found:", layers)

    for layer in layers:
        print(f"Processing layer: {layer}")
        gdf = gpd.read_file(gdb_path, layer=layer)

        # Layer alone
        fig, ax = plt.subplots(figsize=(8,6))
        gdf.plot(ax=ax, facecolor='none', edgecolor='red')
        plt.title(layer)
        plt.savefig(os.path.join(output_dir, f"{layer}.png"))
        plt.close()

        # Overlay on DEM
        fig, ax = plt.subplots(figsize=(8,6))
        ax.imshow(dem, cmap='terrain')
        gdf.plot(ax=ax, facecolor='none', edgecolor='black')
        plt.title(f"DEM + {layer}")
        plt.savefig(os.path.join(output_dir, f"DEM_{layer}.png"))
        plt.close()

if HAS_PYVISTA:
    print("Launching 3D terrain viewer...")

    x = np.arange(dem.shape[1])
    y = np.arange(dem.shape[0])
    xx, yy = np.meshgrid(x, y)

    grid = pv.StructuredGrid(xx, yy, dem)

    plotter = pv.Plotter()
    plotter.add_mesh(grid, cmap="terrain")
    plotter.show()
else:
    print("PyVista not installed. Skipping 3D view.")


if HAS_LAS:
    las_files = []

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith((".las", ".laz")):
                las_files.append(os.path.join(root, file))

    if las_files:
        print("Loading LAS file...")
        las = laspy.read(las_files[0])

        x = las.x
        y = las.y
        z = las.z

        plt.figure(figsize=(8,6))
        plt.scatter(x, y, c=z, s=0.1)
        plt.colorbar(label="Elevation")
        plt.title("Raw LiDAR Point Cloud")
        plt.savefig(os.path.join(output_dir, "lidar_pointcloud.png"))
        plt.close()


print("\n Processing Complete.")
print(" All outputs saved in:", output_dir)

