#!/usr/bin/env python3
import os
from textwrap import dedent

def generate_snappyHexMeshDict(location_in_mesh: tuple, stl_file: str, file_path: str, refinement: int = 0) -> None:
    """Generate snappyHexMeshDict for a given STL geometry and mesh location."""
    x, y, z = location_in_mesh

    # Use doubled braces to escape f-string literal braces
    snappy_dict = dedent(rf"""
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
            class       dictionary;
            object      snappyHexMeshDict;
        }}
        // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

        castellatedMesh true;
        snap            false;
        addLayers       false;

        geometry
        {{
            {stl_file}
            {{
                type triSurfaceMesh;
                name solids;
            }}
        }};

        castellatedMeshControls
        {{
            maxLocalCells        100000;
            maxGlobalCells       2000000;
            minRefinementCells   10;
            maxLoadUnbalance     0.10;
            nCellsBetweenLevels  3;
            features             ();   
            refinementSurfaces
            {{
                solids
                {{
                    level ({refinement} {refinement});
                }}
            }}
            resolveFeatureAngle  30;
            refinementRegions    {{}}
            locationInMesh       ({x} {y} {z});
            allowFreeStandingZoneFaces false;
        }}

        snapControls
        {{
            nSmoothPatch     3;
            tolerance        2.0;
            nSolveIter       30;
            nRelaxIter       5;
            nFeatureSnapIter 10;
            implicitFeatureSnap false;
            explicitFeatureSnap true;
            multiRegionFeatureSnap false;
        }}

        addLayersControls
        {{
            relativeSizes       true;
            layers              {{}};
            expansionRatio      1.0;
            finalLayerThickness 0.3;
            minThickness        0.1;
            nGrow               0;
            featureAngle        60;
            slipFeatureAngle    30;
            nRelaxIter          3;
            nSmoothSurfaceNormals 1;
            nSmoothNormals      3;
            nSmoothThickness    10;
            maxFaceThicknessRatio      0.5;
            maxThicknessToMedialRatio  0.3;
            minMedianAxisAngle         90;
            nBufferCellsNoExtrude      0;
            nLayerIter                 50;
        }}

        meshQualityControls
        {{
            maxNonOrtho           50;
            maxBoundarySkewness   20;
            maxInternalSkewness   4;
            maxConcave            80;
            minVol                1e-17;
            minTetQuality         1e-3;
            errorReduction        0.75;
            nSmoothScale          4;
            minFaceWeight         0.02;
            minArea               1e-14;
            minVolRatio           0.01;
            minTwist              0.02;
            minTriangleTwist      0.02;
            minDeterminant        0.001;
            maxAspectRatio        50;
            maxFaceFlatness       10;
        }}

        writeFlags
        (
            scalarLevels
            layerSets
            layerFields
        );

        mergeTolerance 1e-6;
    """)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as f:
        f.write(snappy_dict)
    print(f"Generated snappyHexMeshDict at: {file_path}")

if __name__ == "__main__":
    basedir = os.path.dirname(os.path.abspath(__file__))
    # Example usage:
    location = (25, 25, 25)
    stl = "cylinder.stl"
    target = os.path.normpath(os.path.join(basedir, "../system/snappyHexMeshDict"))
    generate_snappyHexMeshDict(location, stl, target)
