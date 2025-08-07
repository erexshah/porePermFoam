import os
import sys
import subprocess
basedir = os.path.dirname(os.path.abspath(__file__))

def vti_to_stl(vti_path, stl_path):
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
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        for line in process.stdout:
            print(line, end='')

        process.wait()

        if process.returncode != 0:
            sys.exit(process.returncode)

    except Exception as e:
        print("Error running vti2stl:", e)
        sys.exit(1)