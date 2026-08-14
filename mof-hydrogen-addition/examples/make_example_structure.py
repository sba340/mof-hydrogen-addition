"""
Build a small synthetic structure with a triazolate-like ring motif (C
atoms bonded only to N, missing their H) so the H-addition script has
something to run on without needing real, unpublished MOF CIFs.

This is NOT a real MOF -- just enough geometry (a 5-membered C-N ring in
a large box) to exercise the neighbor-search-and-place logic.

Usage:
    python examples/make_example_structure.py
"""
import numpy as np
from pymatgen.core import Lattice, Structure

if __name__ == "__main__":
    # Planar 5-membered ring: 2 C, 3 N (like a 1,2,4-triazolate), radius ~1.3 A
    n_atoms = 5
    species = ["C", "N", "C", "N", "N"]
    radius = 1.3
    angles = np.linspace(0, 2 * np.pi, n_atoms, endpoint=False)
    coords = [(radius * np.cos(a) + 10, radius * np.sin(a) + 10, 10) for a in angles]

    lattice = Lattice.cubic(20.0)
    s = Structure(lattice, species, coords, coords_are_cartesian=True)

    s.to(filename="examples/ring_no_H.cif")
    print("Wrote examples/ring_no_H.cif (synthetic, not real MOF data)")
    print(f"Formula: {s.formula}")
