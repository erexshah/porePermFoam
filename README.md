# **porePermFoam**  
*A lightweight tool for computing permeability of porous media using OpenFOAM.*  

![Permeability Simulation](resources/img1.png)  

---

## **Overview**  
**porePermFoam** provides a streamlined workflow to estimate the permeability of porous media using **OpenFOAM** for CFD simulations and **ParaView** for post-processing.  
It is designed for researchers and engineers who need a quick, reproducible, and automated way to run permeability simulations from image-based geometries or generated meshes.

---

## **Features**  
- 🔹 Easy-to-run Jupyter notebook interface  
- 🔹 Uses **OpenFOAM** for accurate permeability calculations  
- 🔹 Automated preprocessing and simulation setup  
- 🔹 Works with 3D image-based porous structures  
- 🔹 Open-source and extensible  

---

## **Installation**  

### **Prerequisites**  
- **OpenFOAM** (tested with OpenFOAM v7+ and v2412)  
- **ParaView** (for mesh visualization and STL generation)  
- **Python 3.8+**  

### **Setup Steps**  
~~~bash
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
~~~

---

## **Usage**  
1. Open the **`run_porePermFoam.ipynb`** notebook in Jupyter Lab or Jupyter Notebook.  
2. Follow the step-by-step instructions inside to:  
   - Import your porous media geometry  
   - Configure simulation parameters  
   - Run OpenFOAM simulations  
   - Post-process results  
3. View and analyze simulation outputs in ParaView or directly from the notebook.  

---

## **Repository Structure**  
~~~text
porePermFoam/
│
├── run_porePermFoam.ipynb    # Main simulation workflow
├── requirements.txt          # Python dependencies
├── resources/                # Images & logos
└── README.md                 # Project documentation
~~~

---

## **Contact**  
**Developer:** Arash Pourakaberian  
**Principal Investigator:** Prof. Dr. Vahid Niasar  
**Institution:** The University of Manchester  

📧 Email: **arash.pourakaberian@postgrad.manchester.ac.uk**  

| University of Manchester | IMPRES |
|:--:|:--:|
| <img src="resources/UoM_logo.jpg" alt="UoM Logo" height="80" style="vertical-align:middle;" /> | <img src="resources/IMPRES_logo.jpeg" alt="IMPRES Logo" height="80" style="vertical-align:middle;" /> |

---

## **License**  
This project is released under the **MIT License**.  
You are free to use, modify, and distribute this software with attribution.
