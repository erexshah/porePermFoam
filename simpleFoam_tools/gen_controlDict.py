#!/usr/bin/env python3
import os
from textwrap import dedent

def generate_controlDict(file_path: str, end_time: int = 500, write_interval: int = 100) -> None:
    """Generate controlDict for a given simulation."""
    controlDict = dedent(rf"""
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
            object      controlDict;
        }}

        // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

        application     simpleFoam;

        startFrom       latestTime;

        stopAt          endTime;

        endTime         {end_time};

        deltaT         1;

        writeControl    timeStep;

        writeInterval   {write_interval};

        purgeWrite      0;

        writeFormat     ascii;

        writePrecision  6;

        writeCompression uncompressed;

        timeFormat      general;

        timePrecision   6;

        runTimeModifiable true;
    """)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as f:
        f.write(controlDict)
    print(f"Generated controlDict at: {file_path}")


if __name__ == "__main__":
    basedir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.normpath(os.path.join(basedir, "../system/controlDict"))

    generate_controlDict(file_path, end_time=300, write_interval=50)