# Final Single-Deck Split-Notebook Audit

## Scope

Checked the final USB-facing package for the final submission stage.

Primary judge-facing report:

- `solution/Problem 1.ipynb`
- `solution/Problem 2.ipynb`
- `solution/Problem 3.ipynb`

Single submitted presentation route:

- `presentation/QuantumCylinder_presentation.pdf`
- `presentation/PRESENTATION_SLIDE_TEXT_EN.md`
- `presentation/PRESENTATION_STORYBOARD_EN.md`
- `presentation/MANUAL_PRESENTATION_EXPORT_GUIDE.md`
- `presentation/PDF_EXPORT_CHECKLIST.md`

Source-code inspection:

- `source_code/README_FOR_JUDGES.md`
- `source_code/PROBLEM_REQUIREMENT_MAP.md`
- `source_code/solution/solution_1.ipynb` as compact reference only

## Audit Answers

1. Are `Problem 1.ipynb`, `Problem 2.ipynb`, and `Problem 3.ipynb` present?

   Yes. All three split notebooks are present under `solution/`.

2. Is source code present under `submission/usb_package/source_code/`?

   Yes. The source package includes `src/`, `scripts/`, `tests/`, `configs/`,
   `submission/`, `solution/`, selected `results/`, and judge-facing guides.

3. Does the current material clearly say the split notebooks are the primary
   judge-facing answer?

   Yes. `Summary.md`, `README_SUBMISSION.md`, root `README.md`, and
   `source_code/README_FOR_JUDGES.md` identify the split notebooks as the
   primary judge-facing report.

4. Are stale references to `solution_1.ipynb` as the primary final answer
   present?

   No blocking stale references were found. `source_code/solution/solution_1.ipynb`
   remains only as a compact source-code inspection reference.

5. Does the presentation material clearly state that one same
   15-minute-capable deck is used for both main and final rounds?

   Yes. `Summary.md`, `README_SUBMISSION.md`,
   `PRESENTATION_SLIDE_TEXT_EN.md`, `PRESENTATION_STORYBOARD_EN.md`, and
   `SLIDE_CHECKLIST.md` state the single-deck route.

6. Is the 5-minute core path clearly marked?

   Yes. The 5-minute core path is marked in `Summary.md` and
   `PRESENTATION_STORYBOARD_EN.md`.

7. Is the 15-minute expanded path clearly marked?

   Yes. The 15-minute expanded path is marked in
   `PRESENTATION_STORYBOARD_EN.md`.

8. Is IBM Cloud validation visible in the 5-minute core path, not only
   appendix?

   Yes. The Problem 3(b) step of the 5-minute core path includes the IBM Cloud
   validation callout. Appendix A9 keeps detailed job IDs and beta-table
   values.

9. Is Haar reference visible in Problem 1 and core presentation?

   Yes. Problem 1 includes the Haar figure and explains that Haar is a
   reference level, not a training target. The core slide text reports
   `D_MMD = 0.869583 +/- 0.024043` and
   `W_1-F = 0.724439 +/- 0.021491`.

10. Are Problem 1(a) through Problem 3(c) mapped to the split notebooks?

    Yes. `source_code/PROBLEM_REQUIREMENT_MAP.md` maps Problem 1 subparts to
    `../solution/Problem 1.ipynb`, Problem 2 subparts to
    `../solution/Problem 2.ipynb`, and Problem 3 subparts to
    `../solution/Problem 3.ipynb`.

11. Are any broken formulas present, such as `F(psi, phi) = ||^2`,
    `<b_m|`, `tensor _M`, or `|phi_i_m(t,b)>`?

    No. The broken-notation scan found no final-facing hits.

12. Are Markdown files readable with proper line breaks?

    Yes. Final-facing Markdown files have headings, bullets, fenced code
    blocks, and readable line breaks.

13. Are final CSVs valid multi-line CSV files?

    Yes. `python scripts/validate_final_csvs_no_pandas.py` passed using the
    Python standard-library CSV parser.

14. Are IBM tokens/API keys/CRNs absent?

    Yes. `python scripts/scan_for_ibm_secrets.py` passed and updated
    `IBM_SECRET_SCAN_REPORT.md`.

15. Does the existing PDF need manual regeneration because slide text changed?

    Yes. The existing PDF is present and opens, but text extraction still shows
    older wording such as "Final notebook" and does not show the latest IBM
    Cloud core callout. The team should manually regenerate or update the
    PDF/PPT from the latest slide text.

16. What are the remaining blocking issues?

    The only blocking manual action is regenerating or updating the submitted
    PDF/PPT so it reflects the latest single-deck route, split-notebook wording,
    IBM Cloud Problem 3(b) core callout, and export checklist.

## Claim Guardrails

- No quantum advantage claim.
- No hardware advantage claim.
- No full trainable QuDDPM claim.
- No IBM QPU superiority claim.
- IBM validation is hardware-execution validation only.
- The main benchmark remains state-vector based.
