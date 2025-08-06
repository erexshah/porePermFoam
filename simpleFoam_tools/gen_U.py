import os
from textwrap import dedent

def generate_velocity_field(file_path: str, boundary: str = "symmetryPlane") -> None:
    """Generate a 'U' initial condition file with specified boundary conditions."""
    if boundary.lower() == "symmetryplane":
        bc_type = "symmetryPlane"
    elif boundary.lower() == "wall":
        bc_type = "noSlip"
    else:
        raise ValueError(f"Unsupported boundary type: {boundary}")

    U_dict = dedent(rf"""
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
            class       volVectorField;
            location    "0";
            object      U;
        }}

        dimensions      [0 1 -1 0 0 0 0];

        internalField   uniform (0 0 0);

        boundaryField
        {{
            top
            {{
                type            {bc_type};
            }}
            inlet
            {{
                type            zeroGradient;
            }}
            bottom
            {{
                type            {bc_type};
            }}
            outlet
            {{
                type            zeroGradient;
            }}
            solids
            {{
                type            noSlip;
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
        f.write(U_dict)
    print(f"Generated U at: {file_path} with boundary {bc_type}")


if __name__ == "__main__":
    import os
    basedir = os.path.dirname(os.path.abspath(__file__))

    # Velocity field example
    velocity_target = os.path.normpath(os.path.join(basedir, "../0/U"))
    generate_velocity_field(velocity_target, boundary="wall")