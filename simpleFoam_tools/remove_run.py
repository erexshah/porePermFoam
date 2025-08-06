import os
import shutil

def remove_run_files(basedir):
    """Remove all files and directories related to the 'run' directory."""
    cellLevel = os.path.join(basedir, "0/cellLevel")
    os.remove(cellLevel) if os.path.exists(cellLevel) else None
    pointLevel = os.path.join(basedir, "0/pointLevel")
    os.remove(pointLevel) if os.path.exists(pointLevel) else None
    for dir in os.listdir(basedir):
        if dir[0].isdigit() and dir != '0':
            shutil.rmtree(os.path.join(basedir, dir))
            
    msh_path = os.path.join(basedir, "constant", "polyMesh")
    if os.path.exists(msh_path):
        shutil.rmtree(msh_path)
    postProc_path = os.path.join(basedir, "postProcessing")
    if os.path.exists(postProc_path):
        shutil.rmtree(postProc_path)
        
if __name__ == "__main__":
    import os
    basedir = os.path.dirname(os.path.abspath(__file__))
    basedir = os.path.normpath(os.path.join(basedir, ".."))
    remove_run_files(basedir)
    