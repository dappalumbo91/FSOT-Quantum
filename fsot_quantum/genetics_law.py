"""
Genetics trit law — copied here, genetics repo not edited.

Source (read-only): FSOT-Genetics
  formulas/64_codon_trinary_map.txt
  formulas/20_amino_acid_expanded_trinary.txt
  scripts/trinary_syntax.py  (F01 + aromatic/branch/hetero/detail)

Same pin family. Discrete chemistry facts as trits. No free parameters.
"""

from __future__ import annotations

from typing import Sequence

# F01 (c, p, v) — genetics authority
F01: dict[str, tuple[int, int, int]] = {
    "A": (0, -1, -1),
    "R": (1, 1, 1),
    "N": (0, 1, 0),
    "D": (-1, 1, 0),
    "C": (0, 0, -1),
    "Q": (0, 1, 1),
    "E": (-1, 1, 1),
    "G": (0, -1, -1),
    "H": (1, 1, 1),
    "I": (0, -1, 1),
    "L": (0, -1, 1),
    "K": (1, 1, 1),
    "M": (0, -1, 1),
    "F": (0, -1, 1),
    "P": (0, -1, 0),
    "S": (0, 1, -1),
    "T": (0, 1, 0),
    "W": (0, -1, 1),
    "Y": (0, 1, 1),
    "V": (0, -1, 0),
}

AA20 = "ARNDCQEGHILKMFPSTWYV"

# Standard genetic code — published biology object, not a fit.
GENETIC_CODE: dict[str, str] = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}

# Published 7-trit words from 20_amino_acid_expanded_trinary.txt
PUBLISHED_WORD: dict[str, tuple[int, int, int, int, int, int, int]] = {
    "A": (0, -1, -1, 0, 0, 0, 0),
    "R": (1, 1, 1, 0, 0, 0, 1),
    "N": (0, 1, 0, 0, 0, 0, 0),
    "D": (-1, 1, 0, 0, 0, 0, 0),
    "C": (0, 0, -1, 0, 0, 1, 0),
    "Q": (0, 1, 1, 0, 0, 0, 0),
    "E": (-1, 1, 1, 0, 0, 0, 0),
    "G": (0, -1, -1, 0, 0, -1, 0),
    "H": (1, 1, 1, 0, 0, 1, 0),
    "I": (0, -1, 1, 0, 1, 0, 1),
    "L": (0, -1, 1, 0, 1, 0, -1),
    "K": (1, 1, 1, 0, 0, 0, -1),
    "M": (0, -1, 1, 0, 0, 1, 0),
    "F": (0, -1, 1, 1, 0, 0, 1),
    "P": (0, -1, 0, 0, -1, 0, 0),
    "S": (0, 1, -1, 0, 0, -1, 0),
    "T": (0, 1, 0, 0, 1, -1, -1),
    "W": (0, -1, 1, 1, 0, 1, 0),
    "Y": (0, 1, 1, 1, 0, -1, 0),
    "V": (0, -1, 0, 0, 1, 0, 1),
}

BASES = "ACGT"


def trit(x: int) -> int:
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def trit_not(t: int) -> int:
    return trit(-int(t))


def base_primary(b: str) -> int:
    """A,G → +1; C,T → −1. Genetics codon.zig."""
    u = b.upper()
    if u in "AG":
        return 1
    if u in "CT":
        return -1
    return 0


def base_secondary(b: str) -> int:
    """A → +1; T → −1; G,C → 0. Genetics codon map."""
    u = b.upper()
    if u == "A":
        return 1
    if u == "T":
        return -1
    return 0


def codon_primary(codon: str) -> tuple[int, int, int]:
    c = codon.upper()
    return (base_primary(c[0]), base_primary(c[1]), base_primary(c[2]))


def codon_secondary(codon: str) -> tuple[int, int, int]:
    c = codon.upper()
    return (base_secondary(c[0]), base_secondary(c[1]), base_secondary(c[2]))


def aromatic_trit(aa: str) -> int:
    return 1 if aa in "FYW" else 0


def branch_trit(aa: str) -> int:
    if aa in "IVLT":
        return 1
    if aa == "P":
        return -1
    return 0


def hetero_trit(aa: str) -> int:
    if aa in "CM":
        return 1
    if aa in "STY":
        return -1
    if aa in "WH":
        return 1
    if aa == "G":
        return -1
    return 0


def detail_trit(aa: str) -> int:
    if aa == "I":
        return 1
    if aa == "L":
        return -1
    if aa == "R":
        return 1
    if aa == "K":
        return -1
    if aa == "F":
        return 1
    if aa == "V":
        return 1
    if aa == "T":
        return -1
    return 0


def aa_opcode(aa: str) -> tuple[int, int, int, int, int, int, int]:
    c, p, v = F01[aa]
    return (
        c,
        p,
        v,
        aromatic_trit(aa),
        branch_trit(aa),
        hetero_trit(aa),
        detail_trit(aa),
    )


def all_codons() -> list[str]:
    return [a + b + c for a in BASES for b in BASES for c in BASES]


def translate(codon: str) -> str:
    return GENETIC_CODE[codon.upper()]
