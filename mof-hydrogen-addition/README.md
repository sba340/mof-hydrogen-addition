# mof-hydrogen-addition

Adds missing terminal hydrogen atoms to a MOF (or other) CIF structure
that was reported/solved without them — common for ligand rings
(triazolate, imidazolate, etc.) where X-ray structures often don't
resolve H positions.

## Method

For every atom of a chosen `target_element` (e.g. C) missing a bonded H:

1. Find its heavy-atom neighbors within a search radius, restricted to
   specified bonding elements (e.g. only count C/N as ring bonds, ignore
   the metal node and coordinated water).
2. Average the bond-direction vectors to those neighbors.
3. Place the new H opposite that average direction — the correct terminal
   geometry for an aromatic/heterocyclic C-H or N-H with no other open
   valence.
4. Bond length is fixed (default 0.96 Å for C-H; use ~1.01 Å for N-H).

This is a simple geometric placement, not a DFT-quality optimization —
**always relax the resulting H positions** (e.g. a short DFT or force-field
optimization) before using the structure for production calculations.

**Limitation:** only places one H per atom. Groups needing more than one
H on the same atom (CH2, CH3, NH2) require known local coordination
geometry and aren't handled by this method.

## Usage

```bash
pip install -r requirements.txt

python src/run_add_hydrogens.py \
    --cif your_structure.cif \
    --out your_structure_with_H.cif \
    --target-element C --neighbor-elements C N \
    --bond-length 0.96 --search-cutoff 2.5
```

Excluding the metal node explicitly, or adding to N instead of C (e.g. an
imidazolate N-H):

```bash
python src/run_add_hydrogens.py \
    --cif linker.cif --out linker_with_H.cif \
    --target-element N --neighbor-elements C N --exclude-elements Zn \
    --bond-length 1.01
```

Try it on a synthetic test ring first (no real MOF data needed):

```bash
python examples/make_example_structure.py
python src/run_add_hydrogens.py --cif examples/ring_no_H.cif --out /tmp/ring_with_H.cif \
    --target-element C --neighbor-elements C N
```

## Notebook

`notebooks/MOF_adding_H_CIF.ipynb` is the original notebook this was
developed in, hardcoded for one compound (CuTA, orthorhombic phase,
triazolate ligand). `src/` is the general, reusable version — same
placement logic, but works for any target element / neighbor set /
bond length via command-line flags.
