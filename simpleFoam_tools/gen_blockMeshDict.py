#!/usr/bin/env python3
import os
from textwrap import dedent

def generate_blockMeshDict(shape: tuple, mesh_resolution: tuple, file_path: str, boundary: str="symmetryPlane") -> None:
    """Generate blockMeshDict for a given geometry and cell size."""
    nx, ny, nz = shape
    dx, dy, dz = mesh_resolution
    if boundary.lower() == "symmetryplane":
        bc_type = "symmetryPlane"
    elif boundary.lower() == "wall":
        bc_type = "Wall"
    else:
        raise ValueError(f"Unsupported boundary type: {boundary}")

    blockMeshDict = dedent(rf"""
        /*--------------------------------*- C++ -*----------------------------------*\\
          =========                 |
          \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
           \\    /   O peration     | Website:  https://openfoam.org
            \\  /    A nd           | Version:  7
             \\/     M anipulation  |
        \\*---------------------------------------------------------------------------*/
        FoamFile
        {{
            version     2.0;
            format      ascii;
            class       dictionary;
            object      blockMeshDict;
        }}

        // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

        convertToMeters 1;

        lx0 0;
        ly0 0;
        lz0 0;

        lx1 {nx-1};
        ly1 {ny-1};
        lz1 {nz-1};

        nx {dx};
        ny {dy};
        nz {dz};

        vertices
        (
            ($lx0 $ly0 $lz0)   //0
            ($lx1 $ly0 $lz0)   //1
            ($lx1 $ly1 $lz0)   //2
            ($lx0 $ly1 $lz0)   //3
            ($lx0 $ly0 $lz1)   //4
            ($lx1 $ly0 $lz1)   //5
            ($lx1 $ly1 $lz1)   //6
            ($lx0 $ly1 $lz1)   //7
        );

        blocks
        (
            hex (0 1 2 3 4 5 6 7) ($nx $ny $nz) simpleGrading (1 1 1)
        );

        edges
        (
        );

        boundary
        (
            top
            {{
                type {bc_type};
                faces
                (
                    (7 6 3 2)
                );
            }}

            inlet
            {{
                type patch;
                faces
                (
                    (0 4 7 3)
                );
            }}

            bottom
            {{
                type {bc_type};
                faces
                (
                    (1 5 4 0)
                );
            }}

            outlet
            {{
                type patch;
                faces
                (
                    (1 2 6 5)
                );
            }}

            front
            {{
                type {bc_type};
                faces
                (
                    (0 3 2 1)
                );
            }}

            back
            {{
                type {bc_type};
                faces
                (
                    (4 5 6 7)
                );
            }}
        );
    """)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as f:
        f.write(blockMeshDict)
    print(f"Generated blockMeshDict at: {file_path}")


if __name__ == "__main__":
    basedir = os.path.dirname(os.path.abspath(__file__))
    shape = (100, 50, 50)  # Example shape

    # Resolve the target path inside the system directory:
    system_dir   = os.path.join(basedir, "..", "system")
    file_path    = os.path.normpath(os.path.join(system_dir, "blockMeshDict"))

    generate_blockMeshDict(shape, file_path, boundary="wall")
