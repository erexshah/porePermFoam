import kphi
import os
import sys
import subprocess
basedir = os.path.dirname(os.path.abspath(__file__))

def make_cylinder_vti(radii, shape, vti_path):
    """Create a VTI file with a cylinder geometry."""

    kphi.create_binary_vti(shape=shape,
                           geometry="cylinder",
                           radius=radii,
                           filename=vti_path,
                           axis="z_to_x")
    print(f"Created VTI file: {vti_path}")
    

def make_stl(vti_path, stl_path):
    """Convert VTI to STL using paraview_stl.py script."""
    vti_abs = os.path.abspath(vti_path)
    stl_abs = os.path.abspath(stl_path)

    command = ["pvpython",
                os.path.join(basedir, "paraview_stl.py"),
                vti_abs,
                stl_abs,
                ]
    print(f"Running command: {' '.join(command)}")
    try:
        process = subprocess.Popen(
            command,
            cwd=basedir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Merge stderr into stdout
            text=True,
            bufsize=1,  # Line-buffered
        )

        # Print output line by line
        for line in process.stdout:
            print(line, end='')  # Already includes newline

        process.wait()

        if process.returncode != 0:
            sys.exit(process.returncode)

    except Exception as e:
        print("Error running vti2stl:", e)
        sys.exit(1)
    
    
if __name__ == "__main__":
    vti_path = os.path.join(basedir, "constant", "triSurface", "cylinder.vti")
    stl_path = os.path.join(basedir, "constant", "triSurface", "cylinder.stl")
    radii = 10
    x, y, z = 100, 50, 50
    shape = (z, y, x)

    make_cylinder_vti(radii, shape, vti_path)
    make_stl(vti_path, stl_path)