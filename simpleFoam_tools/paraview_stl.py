from paraview.simple import *
import sys

if len(sys.argv) != 3:
    print("Usage: pvpython paraview_stl.py input.vti output.stl")
    sys.exit(1)

input_vti, output_stl = sys.argv[1], sys.argv[2]

reader = XMLImageDataReader(FileName=[input_vti])
reader.PointArrayStatus = ['Scalars_']
reader.UpdatePipeline()

thresh = Threshold(Input=reader)
thresh.Scalars = ['POINTS', 'Scalars_']
thresh.ThresholdMethod = 'Between'
thresh.LowerThreshold = 0
thresh.UpperThreshold = 0
thresh.UpdatePipeline()

surf = ExtractSurface(Input=thresh)
surf.UpdatePipeline()

tri = Triangulate(Input=surf)
tri.UpdatePipeline()

SaveData(output_stl,
         proxy=tri,
         FileType='Ascii')

print(f"✅ Wrote ASCII STL: {output_stl}")