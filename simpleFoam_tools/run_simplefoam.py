#!/usr/bin/env python3
import subprocess
import re
import csv
import sys
import os

def _run(cmd, cwd=None):
    """Run a shell command, streaming its output to stdout/stderr and return combined output."""
    print(f"\n>>> {cmd}\n")
    p = subprocess.Popen(cmd, shell=True,
                         cwd=cwd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         text=True,)
    output = []
    for line in p.stdout:
        print(line, end='')
        output.append(line)
    p.wait()
    if p.returncode != 0:
        sys.exit(f"Command failed (code {p.returncode}): {cmd}")
    return ''.join(output)

def _extract_flow_rates(text, patch_name):
    """
    Parse postProcess output for flowRatePatch(name=patch_name),
    returning list of (time, flowRate) across all time steps.
    """
    times = re.findall(r"^Time\s*=\s*([\dEe+\.-]+)", text, re.MULTILINE)
    pattern = rf"sum\({re.escape(patch_name)}\) of phi\s*=\s*([\dEe+\.-]+)"
    rates  = re.findall(pattern, text)
    if len(times) != len(rates):
        print(f"Warning: {len(times)} times vs {len(rates)} rates for '{patch_name}'")
    n = min(len(times), len(rates))
    return [(float(times[i]), float(rates[i])) for i in range(n)]

def _extract_patch_area_from_flow(text, patch_name):
    """
    Parse the flowRatePatch output block for this patch, grabbing
    the first 'total area    = <value>' line (at T=0).
    """
    pattern = rf"surfaceFieldValue\s+flowRatePatch\(name={re.escape(patch_name)}\)[\s\S]*?total area\s*=\s*([\dEe+\.-]+)"
    m = re.search(pattern, text)
    if not m:
        sys.exit(f"Could not parse 'total area' for patch '{patch_name}'")
    return float(m.group(1))

def _write_csv(filename, data, area):
    """Write list of (time, rate) to CSV file with an area column."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'flowRate_phi', 'area'])
        for t, q in data:
            writer.writerow([t, q, area])
    print(f"Wrote {len(data)} records with area={area:g} to {filename}")

def run_simplefoam(basedir, scale: float = 1e-6):
    # 1. Mesh generation
    _run("blockMesh", cwd=basedir)
    _run("snappyHexMesh -overwrite", cwd=basedir)
    _run(f'transformPoints -scale "({scale} {scale} {scale})"', cwd=basedir)

    # 2. Solver
    _run("simpleFoam", cwd=basedir)

    # 3. postProcess (all times)
    out_in  = _run("postProcess -func 'flowRatePatch(name=inlet)'",  cwd=basedir)
    out_out = _run("postProcess -func 'flowRatePatch(name=outlet)'", cwd=basedir)

    # 4. Extract data and area
    inlet_data   = _extract_flow_rates(out_in,  'inlet')
    outlet_data  = _extract_flow_rates(out_out, 'outlet')
    area_inlet   = _extract_patch_area_from_flow(out_in,  'inlet')
    area_outlet  = _extract_patch_area_from_flow(out_out, 'outlet')

    # 5. Save CSVs with area
    _write_csv("q_in.csv",  inlet_data,  area_inlet)
    _write_csv("q_out.csv", outlet_data, area_outlet)

    # 6. Summary
    print("\n--- inlet fluxes ---")
    for t, q in inlet_data:
        print(f"t={t:<10g}, q_in={q:.5e}, A_in={area_inlet:g}")
    print("\n--- outlet fluxes ---")
    for t, q in outlet_data:
        print(f"t={t:<10g}, q_out={q:.5e}, A_out={area_outlet:g}")

if __name__ == '__main__':
    basedir = os.path.dirname(os.path.abspath(__file__))
    run_simplefoam(basedir=os.path.join(basedir, ".."), scale=1e-6)
