"""
Add terminal (undetected) hydrogen atoms to a CIF structure that was solved
or reported without them -- common for MOF ligands (e.g. triazolate,
imidazolate rings) where X-ray structures often don't resolve H positions.

Method
------
For every atom of `target_element` (e.g. C) that is missing a bonded H:

  1. Find its heavy-atom neighbors within `search_cutoff` (excluding
     elements in `exclude_elements`, e.g. the metal node and any oxygens
     from coordinated solvent/water that shouldn't count as ring bonds).
  2. Average the bond-direction vectors to those neighbors.
  3. Place the new H along the direction opposite that average -- i.e.
     pointing away from the ring/chain, which is the correct terminal
     geometry for an aromatic/heterocyclic C-H (or N-H) with no other
     open valence.
  4. Bond length is fixed at `bond_length` (default 0.96 A, the standard
     aromatic C-H length; use ~1.01 A for N-H if adding to N instead).

This is a simple geometric placement, not a DFT-quality optimization --
always relax the resulting structure (e.g. a short DFT/force-field
optimization of just the H positions) before using it for production
calculations.
"""
from collections import Counter

import numpy as np
from pymatgen.core import Structure


def add_terminal_hydrogens(
    structure: Structure,
    target_element: str = "C",
    neighbor_elements=("C", "N"),
    exclude_elements=(),
    bond_length: float = 0.96,
    search_cutoff: float = 2.5,
    h_per_atom: int = 1,
):
    """Return (new_structure, n_added, warnings) with one H placed per
    `target_element` atom that has heavy-atom neighbors in
    `neighbor_elements` (and none in `exclude_elements`).

    h_per_atom > 1 is not handled by this simple geometric method (adding
    multiple H to the same atom requires knowing the local coordination
    geometry, e.g. sp3 CH2/CH3) -- raises if requested.
    """
    if h_per_atom != 1:
        raise NotImplementedError(
            "This geometric method only places 1 H per atom (works for "
            "aromatic/heterocyclic C-H or N-H). Multi-H groups (CH2, CH3, "
            "NH2) need a different placement strategy."
        )

    s_with_h = structure.copy()
    target_indices = [i for i, site in enumerate(s_with_h) if str(site.specie) == target_element]

    h_fracs = []
    warnings = []
    for i in target_indices:
        site = s_with_h[i]
        cart_pos = site.coords

        neighbors = s_with_h.get_neighbors(site, search_cutoff)
        neighbors = [n for n in neighbors if str(n.specie) not in exclude_elements]
        bond_neighbors = [n for n in neighbors if str(n.specie) in neighbor_elements]

        if not bond_neighbors:
            warnings.append(f"{target_element} site {i}: no {neighbor_elements} neighbors found, skipped")
            continue

        bond_vectors = [cart_pos - n.coords for n in bond_neighbors]
        avg_vector = np.mean(bond_vectors, axis=0)
        norm = np.linalg.norm(avg_vector)

        if norm < 1e-6:
            warnings.append(f"{target_element} site {i}: bonds cancel out (symmetric), skipped")
            continue

        h_direction = avg_vector / norm
        h_cart = cart_pos + bond_length * h_direction
        h_frac = s_with_h.lattice.get_fractional_coords(h_cart) % 1.0
        h_fracs.append(h_frac)

    for h_frac in h_fracs:
        s_with_h.append("H", h_frac, validate_proximity=False)

    return s_with_h, len(h_fracs), warnings


def summarize(original: Structure, new: Structure, target_element: str):
    """Print a before/after element-count table and a target:H ratio check."""
    orig_counts = Counter(str(site.specie) for site in original)
    new_counts = Counter(str(site.specie) for site in new)

    print(f"{'Element':<10} {'Original':>10} {'With H':>10}")
    print("-" * 32)
    for el in sorted(set(orig_counts) | set(new_counts)):
        print(f"{el:<10} {orig_counts.get(el, 0):>10} {new_counts.get(el, 0):>10}")

    t_count = new_counts.get(target_element, 0)
    h_count = new_counts.get("H", 0)
    print(f"\n{target_element}:H ratio = {t_count}:{h_count}")
    if t_count == h_count:
        print(f"{target_element}:H ratio is 1:1 (every {target_element} got an H).")
    else:
        print(f"Mismatch -- {t_count - h_count} {target_element} atom(s) did not get an H. "
              f"Check the warnings above and your neighbor/exclude element settings.")
