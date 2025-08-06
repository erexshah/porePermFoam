import os
from textwrap import dedent

def generate_pressure_field(file_path: str, boundary: str = "symmetryPlane") -> None:
    """Generate a 'p' initial condition file with specified boundary conditions."""
    # Map user-friendly boundary name to OpenFOAM type
    if boundary.lower() == "symmetryplane":
        bc_type = "symmetryPlane"
    elif boundary.lower() == "wall":
        bc_type = "zeroGradient"
    else:
        raise ValueError(f"Unsupported boundary type: {boundary}")

    p_dict = dedent(rf"""
        /*--------------------------------*- C++ -*----------------------------------*\\
          =========                 |
          \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
           \\    /   O peration     | Website:  https://openfoam.org
            \\  /    A nd           | Version:  7
             \\/     M anipulation  |
        \*---------------------------------------------------------------------------*/
        FoamFile
        {{
            version     2.0;
            format      ascii;
            class       volScalarField;
            location    "0";
            object      p;
        }}

        dimensions      [0 2 -2 0 0 0 0];

        internalField   uniform 0;

        boundaryField
        {{
            top
            {{
                type            {bc_type};
            }}
            inlet
            {{
                type            fixedValue;
                value           uniform 1e-3;
            }}
            bottom
            {{
                type            {bc_type};
            }}
            outlet
            {{
                type            fixedValue;
                value           uniform 0;
            }}
            solids
            {{
                type            zeroGradient;
            }}
            front
            {{
                type            {bc_type};
            }}
            back
            {{
                type            {bc_type};
            }}
        }}
    """)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(p_dict)
    print(f"Generated p at: {file_path} with boundary {bc_type}")


if __name__ == "__main__":
    import os
    basedir = os.path.dirname(os.path.abspath(__file__))

    # Pressure field example
    pressure_target = os.path.normpath(os.path.join(basedir, "../0/p"))
    generate_pressure_field(pressure_target, boundary="wall")