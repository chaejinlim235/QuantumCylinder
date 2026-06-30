# No-Pandas IBM Result Update

The IBM QPU Problem 3-b result extraction and summarization path does not
require pandas.

Scripts checked:

- `scripts/ibm_qpu_extract_p3b_counts.py`
- `scripts/summarize_ibm_qpu_p3b_results.py`
- `scripts/copy_ibm_qpu_results_to_usb.py`

These scripts use Python standard-library modules such as `csv`, `json`,
`pathlib`, `statistics`, `math`, `collections`, and `datetime`, plus
`qiskit_ibm_runtime` only for IBM Runtime job retrieval.

No `import pandas` or `pd.` usage is required for the IBM result update.
