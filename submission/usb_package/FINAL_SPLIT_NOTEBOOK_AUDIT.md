# Final Split Notebook Audit

## Scope

Checked final USB-facing artifacts:

- `Summary.md`
- `README_SUBMISSION.md`
- `JUDGING_CRITERIA_ALIGNMENT.md`
- `solution/Problem 1.ipynb`
- `solution/Problem 2.ipynb`
- `solution/Problem 3.ipynb`
- `solution/figures/`
- `presentation/QuantumCylinder_presentation.pdf`
- `presentation/PRESENTATION_SLIDE_TEXT_EN.md`
- `presentation/PRESENTATION_STORYBOARD_EN.md`
- `source_code/README_FOR_JUDGES.md`
- `source_code/PROBLEM_REQUIREMENT_MAP.md`
- `source_code/results/ibm_qpu_validation/`
- root `README.md`

## Audit Answers

1. Are `Problem 1.ipynb`, `Problem 2.ipynb`, `Problem 3.ipynb` present?

Yes. They are present under `submission/usb_package/solution/` and are now
explicitly identified as the primary judge-facing split notebooks.

2. Is the English PDF/PPT presentation present?

Yes. `presentation/QuantumCylinder_presentation.pdf` is present. It has 15
pages, is not encrypted, and the first page rendered locally. The package also
includes English slide text, storyboard, checklist, and a 15-minute speaker
script. No separate PPT file is required by the current package structure.

3. Is source code present?

Yes. `source_code/` contains `src/`, `scripts/`, `tests/`, `configs/`,
`submission/`, `solution/`, `results/`, `pyproject.toml`, and
`requirements.txt`.

4. Do Summary/README files correctly point to split notebooks as primary final answer?

Yes. `Summary.md`, `README_SUBMISSION.md`, root `README.md`, and
`source_code/README_FOR_JUDGES.md` now state that the split notebooks under
`solution/` are the primary judge-facing report. `solution_1.ipynb` is described
only as a compact source-code reference.

5. Are there stale references to `solution_1.ipynb` as the main final answer?

No blocking stale references remain. Historical audit files may mention
`solution_1.ipynb` as an artifact that was previously checked, but current
guide, presentation, and requirement-map documents demote it to compact
source-code reference.

6. Are Problem 1(a) through Problem 3(c) explicitly covered in split notebooks?

Yes. Each split notebook has a top judge-facing summary cell. Problem 1 covers
1(a), 1(b), and 1(c); Problem 2 covers 2(a), 2(b), 2(c), and 2(d); Problem 3
covers 3(a), 3(b), and 3(c).

7. Is Haar reference included in Problem 1?

Yes. Problem 1 includes the Haar reference as a reference level, not a training
target. `solution/figures/fig2_random_unitary_haar_baseline.png` is included
and shows the Haar mean, one-standard-deviation band, and plateau zoom.

8. Is IBM Cloud execution included in Problem 3 and presentation?

Yes. Problem 3 now contains a Problem 3(b) IBM Cloud validation callout. The
presentation core slide text and storyboard also include the `ibm_fez`
measurement-basis sweep callout. The already-submitted PDF was inspected but
not regenerated in this pass; if the PDF is the controlling presentation file,
regenerate it from the updated slide text/storyboard before USB submission.
Detailed job IDs and tables remain available for appendix/Q&A.

9. Are Markdown/CSV files readable with proper line breaks?

Yes for the final-facing guides and generated validation reports. Markdown
headings, bullets, code fences, and tables remain valid. Long command lines are
kept inside fenced code blocks. CSV validation is documented in
`CSV_VALIDATION_REPORT.md`.

10. Are there broken math expressions such as `F(psi, phi) = ||^2`?

No blocking broken expressions were found after cleanup. Fidelity is written as
\(F(\psi,\phi)=|\langle\psi|\phi\rangle|^2\), and the Problem 3 post-selection
map is written with proper LaTeX equations.

11. Are IBM tokens/API keys/CRNs absent?

Yes. `IBM_SECRET_SCAN_REPORT.md` reports PASS. The scan covered
`submission/usb_package/`, IBM QPU docs, and IBM QPU scripts.

12. What must be fixed before USB submission?

No blocking packaging/source-code issue remains from this audit. Manual actions
left before official submission:

- Open the PDF on another machine if possible.
- Regenerate or manually update the final presentation PDF if it must contain
  the new Problem 3(b) IBM Cloud core callout. The Markdown slide text and
  storyboard are updated; the PDF itself was only inspected, not rebuilt.

## Decision

The current USB package follows the intended split-notebook hierarchy and is
ready for final source-code inspection, subject to the manual PDF sanity check
above.
