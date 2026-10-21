# Source Mapping

Traceability from each Python benchmark to primary mathematical / code sources.

> **2026-10-19 update:** the supplied executable MATLAB repositories are the
> implementation ground truth where they differ from publication tables.
> All 35 objectives and all 33 safely executable PS/PF references now match
> licensed MATLAB. Use `validation/equivalence_matrix.md` for the full matrix.

Legend for **Status**:
- **PASS** — objectives and safely executable PS/PF outputs match licensed MATLAB
- **PARTIAL** — currently only MPMOP4/9, whose MATLAB `true_PS.m` mesh is unsafe to execute
- **NEEDS_MANUAL_VERIFICATION** — ambiguous in the source materials (none remaining)

---

## Global sources

| ID | Artifact |
|---|---|
| OptMPNDS | `sources/OptMPNDS` — https://github.com/lwjie595/OptMPNDS |
| She2023 code | `sources/mpdmp_2023/2022SheOptMPNDS3` — https://github.com/MiLabHITSZ/2022SheOptMPNDS3 |
| She2023 paper | arXiv:2207.13390 (`sources/mpdmp_2023/elsarticle-template-1-num.tex`) |
| ZM26 paper | arXiv:2601.22497 (`sources/zm26_2026/main.tex`) |
| ZM26 appendix | `sources/zm26_2026/Appendix.pdf` (TeX for appendix **not** shipped; text via `pdftotext`) |

Audit update (2026-10-19): licensed MATLAB compared all 35 objectives and
all 33 safely executable PS/PF references. Octave remains optional for
MPMOP1–11 only. See `validation/audit_final.md`.

---

## MPDMP13

- **Source paper:** ZM26 Appendix S-X / Table S-V
- **Source TeX:** not available (PDF only) — verified via `pdftotext`
- **Python:** `src/fairmoo_benchmarks/mpdmp/mpdmp13.py`
- **Equations:** \(x\in[0,100]^2\), \(f_{m,i}(x)=\|x-p_{m,i}\|_2\)
- **Reference points:** DM1 (30,40),(70,40); DM2 (30,60),(70,60)
- **Validated against:** Appendix Table S-V
- **Status:** PASS

## MPDMP14–MPDMP18

Same family as MPDMP13. Points verified against Table S-V (including MPDMP17 three-DM and MPDMP18 three-triangle layouts).
- **Python:** `mpdmp14.py` … `mpdmp18.py`
- **Status:** PASS

## MPDMP1

- **Source MATLAB:** `Problems/MPDMP/square.m` + `MPDMP1.m`
- **Points / order:** A(30,70), C(70,30) → DM1; B(70,70), D(30,30) → DM2 (`distance=[fA,fC,fB,fD]`, `DM={1:2,3:4}`)
- **Common PS:** (50,50)
- **Bounds:** [0,100]^2 (`MPDMP.m`)
- **Python:** `she2023.MPDMP1`
- **Status:** PASS

## MPDMP2

- **Source MATLAB:** `trapezoid1.m`
- **Points:** A(30,70), C(70,30), B(50,70), D(30,30); common PS (130/3, 170/3)
- **Status:** PASS

## MPDMP3

- **Source MATLAB:** `LinearMap.m` + `nsidedpoly(3,'Center',[50,40],'Radius',20)`
- **Status:** PASS — Radius mode follows MathWorks nsidedpoly (first vertex right, CCW); see geometry tests / audit

## MPDMP4

- **Source MATLAB:** explicit `polyshape` vertices in `MPDMP4.m`
- **Common PS:** (50,40)
- **Status:** PASS

## MPDMP5 / MPDMP7 / MPDMP8 / MPDMP11 / MPDMP12

- **Source MATLAB:** `nsidedpoly` constructions in corresponding `.m` files
- **Status:** PASS — MATLAB `nsidedpoly` / `polyshape.Vertices` order and common-PS grids match licensed exports

## MPDMP6

- **Source MATLAB:** `MPDMP6.m` (axis-aligned SideLength squares; hardcoded PS `x=50`, `y∈[40,60]`)
- **Status:** PASS (PS geometry matches axis-aligned interpretation)

## MPDMP9 / MPDMP10

- **Source MATLAB:** `square1.m`, `Map10.m`
- **Status:** PASS — reference points, DM ownership, and square vertex order match MATLAB

## MPMOP1–MPMOP11

- **Source paper:** Liu et al., IEEE CEC 2020
- **Source MATLAB:** `MPMOP1.m`–`MPMOP11.m`, `MPMOP_Value.m`, `true_PS.m`
- **Python:** `src/fairmoo_benchmarks/mpmop/liu2020.py`
- **Equations:** direct port of `MPMOP_Value` cases MPMOP1–6 with party times from each classdef
- **Bounds:** confirmed per class (not all [0,1]^D)
- **Status:** PASS for MPMOP1–3, 5–8, 10–11 (objectives + `true_PS.m` sampling). MPMOP4/9 objectives PASS; PS/PF PARTIAL because MATLAB `meshgrid(linspace(0,1,20000))` is unsafe to execute.

### Per-problem quick map

| Problem | value_id | times | M | DM | x1 bounds (others) |
|---|---|---|---|---|---|
| MPMOP1 | MPMOP1 | 1,2 | 4 | 2 | [1,4] / [0,1] |
| MPMOP2 | MPMOP2 | 0,3 | 4 | 2 | [0,1] / [-1,1] |
| MPMOP3 | MPMOP3 | 0,π/2 | 4 | 2 | same as MPMOP2 |
| MPMOP4 | MPMOP4 | 0,1 | 6 | 2 | x1,x2≥0; else [-1,1] |
| MPMOP5 | MPMOP5 | 0,1.5 | 6 | 2 | [0,1] |
| MPMOP6 | MPMOP6 | 0,1 | 6 | 2 | as MPMOP4 |
| MPMOP7 | MPMOP1 | 0,1,2 | 6 | 3 | as MPMOP1 |
| MPMOP8 | MPMOP2 | 0,1,3 | 6 | 3 | as MPMOP2 |
| MPMOP9 | MPMOP4 | 0,0.5,1 | 9 | 3 | as MPMOP4 |
| MPMOP10 | MPMOP5 | 0,1,1.5 | 9 | 3 | [0,1] |
| MPMOP11 | MPMOP6 | 0,1,1.5 | 9 | 3 | as MPMOP4 |

## MPMOP12–MPMOP17

- **Source:** executable MATLAB classes in `2026ZhaoNash-main/MPMOP` (not Appendix Table S-VI where they conflict)
- **Python:** `mpmop12.py`–`mpmop17.py`
- **Dimension:** MATLAB `if isempty(obj.Global.D); obj.Global.D = 10; end`
- **Bounds:** unit hypercube `[0,1]^D`
- **Notes:** MATLAB MPMOP15 calls the MPMOP17 kernel (duplicate). MPMOP16 is `M=4`, `DM=2`. MPMOP17/15 are `M=6`, `DM=3`.
- **Status:** PASS (objectives, D/M/DM, bounds, party PS, and PF vs licensed MATLAB)
