"""
Add missing terminal hydrogens to a MOF (or any) CIF structure.

Usage (matches the original CuTA triazolate case):
    python src/run_add_hydrogens.py \
        --cif CuTA_orthorhombic.cif \
        --out CuTA_orthorhombic_with_H.cif \
        --target-element C --neighbor-elements C N \
        --bond-length 0.96 --search-cutoff 2.5

Adding to N instead of C (e.g. an imidazolate NH), and excluding a metal
node explicitly even though it's outside the search cutoff by default:
    python src/run_add_hydrogens.py \
        --cif linker.cif --out linker_with_H.cif \
        --target-element N --neighbor-elements C N --exclude-elements Zn \
        --bond-length 1.01
"""
import argparse

from pymatgen.core import Structure
from pymatgen.io.cif import CifWriter

from add_hydrogens import add_terminal_hydrogens, summarize


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cif", required=True, help="Input CIF path")
    p.add_argument("--out", required=True, help="Output CIF path (structure with H added)")
    p.add_argument("--target-element", default="C", help="Element to add H to (default: C)")
    p.add_argument("--neighbor-elements", nargs="+", default=["C", "N"],
                    help="Elements counted as ring/chain bonds when computing H direction (default: C N)")
    p.add_argument("--exclude-elements", nargs="+", default=[],
                    help="Elements to ignore entirely as neighbors, e.g. the metal node (default: none)")
    p.add_argument("--bond-length", type=float, default=0.96,
                    help="Target-H bond length in Angstrom (default: 0.96, standard aromatic C-H; use ~1.01 for N-H)")
    p.add_argument("--search-cutoff", type=float, default=2.5,
                    help="Neighbor search radius in Angstrom (default: 2.5)")
    args = p.parse_args()

    s = Structure.from_file(args.cif)
    print(f"Formula: {s.formula}")
    print(f"Space group: {s.get_space_group_info()}")
    print(f"Total sites: {len(s)}\n")

    s_with_h, n_added, warnings = add_terminal_hydrogens(
        s,
        target_element=args.target_element,
        neighbor_elements=tuple(args.neighbor_elements),
        exclude_elements=tuple(args.exclude_elements),
        bond_length=args.bond_length,
        search_cutoff=args.search_cutoff,
    )

    for w in warnings:
        print(f"WARNING: {w}")

    print(f"\nH atoms added: {n_added}")
    print(f"New formula: {s_with_h.formula}\n")
    summarize(s, s_with_h, args.target_element)

    CifWriter(s_with_h).write_file(args.out)
    print(f"\nSaved to: {args.out}")


if __name__ == "__main__":
    main()
