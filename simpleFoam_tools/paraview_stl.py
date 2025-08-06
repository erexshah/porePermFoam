#!/usr/bin/env pvpython
from paraview.simple import *
import sys

if len(sys.argv) != 3:
    print("Usage: pvpython paraview_stl.py input.vti output.stl")
    sys.exit(1)

input_vti, output_stl = sys.argv[1], sys.argv[2]

# 1) Read the VTI
reader = XMLImageDataReader(FileName=[input_vti])
reader.PointArrayStatus = ['Scalars_']
reader.UpdatePipeline()

# 2) Threshold to keep only solids (value == 0)
thresh = Threshold(Input=reader)
thresh.Scalars = ['POINTS', 'Scalars_']
thresh.ThresholdMethod = 'Between'
thresh.LowerThreshold = 0
thresh.UpperThreshold = 0
thresh.UpdatePipeline()

# 3) Extract the surface of that mask
surf = ExtractSurface(Input=thresh)
surf.UpdatePipeline()

# 4) Triangulate all polys into triangles
tri = Triangulate(Input=surf)
tri.UpdatePipeline()

# 5) Write out to ASCII STL
SaveData(output_stl,
         proxy=tri,
         FileType='Ascii')

print(f"✅ Wrote ASCII STL: {output_stl}")