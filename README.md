# **porePermFoam**  
*A lightweight tool for computing permeability of porous media using OpenFOAM.*  

> **From micro-CT to permeability in minutes — `porePermFoam` automates voxel-to-OpenFOAM workflows, making pore-scale CFD simulations fast, reproducible, and accessible.**

![Permeability Simulation](resources/img1.png)  

---

## **Overview**  
**porePermFoam** provides a streamlined workflow to estimate the permeability of porous media using **OpenFOAM** for CFD simulations and **ParaView** for post-processing.  
It is designed for researchers and engineers who need a quick, reproducible, and automated way to run permeability simulations from image-based geometries.

---

## **Features**  
- 🔹 Easy-to-run workflow with automated preprocessing and simulation setup  
- 🔹 Uses **OpenFOAM** for accurate permeability calculations  
- 🔹 Works with 3D image-based porous structures (VTI → STL → mesh)  
- 🔹 Fully open-source and extensible  
- 🔹 Minimal manual intervention required — suitable for batch processing and reproducible research

---

## **Installation**  

### **Prerequisites**  
- **OpenFOAM** (tested with OpenFOAM v7+ and v2412)  
- **ParaView** (for mesh visualisation and STL generation)  
- **Python 3.8+**  

### **Setup Steps**  
```bash
# 1. Install OpenFOAM and ParaView
#    (Refer to your OS-specific installation instructions)

# 2. Clone the repository
git clone https://github.com/erexshah/porePermFoam.git
cd porePermFoam

# 3. Create and activate a Python virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# 4. Install required Python packages
pip install -r requirements.txt
```

---

## **Usage**

### Quick start (recommended)
1. **Prepare geometry**  
   Put your porous-media `.vti` file(s)` (grain voxels = `0`, pore voxels = `1` or `255`) into `constant/geometry/`.

2. **Open the repository**  
   Open this repository in **JupyterLab** / **Jupyter Notebook** (optional) or follow the HTML tutorial at the end of this README (`resources/tutorial.html`).

3. **Run the automated workflow**  
   The workflow will convert `.vti` → `.stl`, automatically generate OpenFOAM dictionaries (`system/` & `0/`), run meshing and the solver, and write CSV post-processing files (e.g., `q_in.csv`).

4. **Post-process**  
   Use the Python utilities in `simpleFoam-tools/` to compute porosity and permeability from outputs, or inspect results with ParaView.

> **Note:** Following the HTML tutorial (`resources/tutorial.ipynb`) for the canonical, step-by-step instructions.

---

### Example workflow summary
- Convert VTI to STL: vti_to_stl(vti_path, stl_path)
- Generate meshes and dictionaries: generate_blockMeshDict, generate_snappyHexMeshDict, generate_controlDict, generate_pressure_field, generate_velocity_field
- Run OpenFOAM case from Python: run_simplefoam(".", scale=scale)
- Post-process and compute:
   - Porosity: vti_phi(vti_path)
   - Permeability via Darcy's law from q_in.csv

---

## **Repository structure**

```text
porePermFoam/
│
├── 0/                        # OpenFOAM initial-condition directory (field files)
├── constant/                 # Geometry, mesh and material/property files for OpenFOAM
├── system/                   # OpenFOAM system files (controlDict, fvSchemes, fvSolution)
├── simpleFoam-tools/         # Python utilities to automate simulation setup & runs
├── run_porePermFoam.ipynb    # Main Jupyter workflow for preprocessing, running and postprocessing
├── requirements.txt          # Python dependencies
├── resources/                # Images, logos and example inputs
└── README.md                 # Project documentation
```

---

## **Contact**  
**Developer:** Arash Pourakaberian  
**Principal Investigator:** Prof. Dr Vahid Niasar  
**Institution:** The University of Manchester  

📧 Email: **arash.pourakaberian@postgrad.manchester.ac.uk**  

| University of Manchester | IMPRES |
|:--:|:--:|
| <img src="resources/UoM_logo.jpg" alt="UoM Logo" height="80" style="vertical-align:middle;" /> | <img src="resources/IMPRES_logo.jpeg" alt="IMPRES Logo" height="80" style="vertical-align:middle;" /> |

---

## **License**  
This project is released under the **MIT License**.  
You are free to use, modify, and distribute this software with attribution.

---

## 📖 Tutorial  

<a href="resources/tutorial.ipynb">Click here to view the tutorial.</a>

---