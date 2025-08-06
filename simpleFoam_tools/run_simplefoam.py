#!/usr/bin/env python3
import subprocess
import re
import csv
import sys

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
    # Find all times
    times = re.findall(r"^Time\s*=\s*([\dEe+\.-]+)", text, re.MULTILINE)
    # Find all sum(...) of phi lines
    pattern = rf"sum\({re.escape(patch_name)}\) of phi\s*=\s*([\dEe+\.-]+)"
    rates = re.findall(pattern, text)
    if len(times) != len(rates):
        print(f"Warning: {len(times)} times vs {len(rates)} rates for '{patch_name}'")
    n = min(len(times), len(rates))
    return [(float(times[i]), float(rates[i])) for i in range(n)]

def _write_csv(filename, data):
    """Write list of (time, rate) to CSV file."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'flowRate_phi'])
        for t, q in data:
            writer.writerow([t, q])
    print(f"Wrote {len(data)} records to {filename}")

def run_simplefoam(basedir, scale: float = 1e-6):
    # 1. Mesh generation
    _run("blockMesh", cwd=basedir)
    _run("snappyHexMesh -overwrite", cwd=basedir)
    _run(f'transformPoints -scale "({scale} {scale} {scale})"', cwd=basedir)

    # 2. Solver
    _run("simpleFoam", cwd=basedir)

    # 3. postProcess (all times, not only latest)
    out_in = _run("postProcess -func 'flowRatePatch(name=inlet)'", cwd=basedir)
    out_out = _run("postProcess -func 'flowRatePatch(name=outlet)'", cwd=basedir)

    # 4. Extract data
    inlet_data = _extract_flow_rates(out_in,  'inlet')
    outlet_data = _extract_flow_rates(out_out, 'outlet')

    # 5. Save CSVs
    _write_csv("q_in.csv",  inlet_data)
    _write_csv("q_out.csv", outlet_data)

    # 6. Summary
    print("\n--- inlet fluxes ---")
    for t, q in inlet_data:
        print(f"t={t:<10g}, q_in={q:.5e}")
    print("\n--- outlet fluxes ---")
    for t, q in outlet_data:
        print(f"t={t:<10g}, q_out={q:.5e}")

if __name__ == '__main__':
    import os
    basedir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(basedir, "..")
    run_simplefoam(basedir=path, scale=1e-6)
