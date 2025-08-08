import vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy

def vti_phi(vti_file_path, invert=False):
    """
    Reads a binary .vti file and calculates porosity (fraction of pore voxels).

    Parameters:
        vti_file_path (str): Path to the binary VTI file (e.g., 0 = grain, 1 or 255 = pore).
        invert (bool): If True, inverts binary mask (e.g., if pores are stored as 0).

    Returns:
        float: Porosity (0-1)
    """
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(vti_file_path)
    reader.Update()
    image_data = reader.GetOutput()

    array = image_data.GetPointData().GetArray(0)
    voxel_values = vtk_to_numpy(array)

    binary = (voxel_values > 0).astype(int)

    porosity = np.sum(binary) / len(binary)
    
    if invert:
        porosity = 1 - porosity

    return porosity

def vti_shape(vti_file_path):
    """
    Reads a .vti file and returns its shape as a set.

    Parameters:
        vti_file_path (str): Path to the .vti file.

    Returns:
        set: Shape of the domain {nx, ny, nz}.
    """
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(vti_file_path)
    reader.Update()
    image_data = reader.GetOutput()
    
    dims = image_data.GetDimensions()  # (nx, ny, nz)
    return tuple(dims)

def find_pore_location(vti_path):
    """
    Reads a binary .vti file and returns the coordinates of a voxel
    located inside the pore space (value > 0).

    Returns:
        tuple: (x, y, z) voxel indices for pore location.
    """
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(vti_path)
    reader.Update()
    image_data = reader.GetOutput()

    dims = image_data.GetDimensions()  # (nx, ny, nz)

    # Extract voxel values as a NumPy array
    array = image_data.GetPointData().GetArray(0)
    voxel_values = vtk_to_numpy(array).reshape(dims[::-1])  # VTK uses z, y, x order

    # Find pore voxels (value > 0)
    pore_indices = np.argwhere(voxel_values > 0)

    if len(pore_indices) == 0:
        raise ValueError("No pore voxels found in the given VTI file.")

    # Pick the pore voxel closest to the center
    center = np.array(dims[::-1]) / 2
    distances = np.linalg.norm(pore_indices - center, axis=1)
    closest_idx = pore_indices[np.argmin(distances)]

    # Convert from (z, y, x) to (x, y, z)
    return (int(closest_idx[2]), int(closest_idx[1]), int(closest_idx[0]))