import vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy

def phi_vti(vti_file_path, invert=False):
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