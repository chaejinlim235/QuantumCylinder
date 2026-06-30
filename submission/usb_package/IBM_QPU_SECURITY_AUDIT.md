# IBM QPU Security Audit

## Files Scanned

The IBM QPU update path was scanned across:

- `scripts/`
- `docs/`
- `results/ibm_qpu_validation/`
- `submission/usb_package/`

Search patterns included:

- `QISKIT_IBM_TOKEN`
- `IBM_QUANTUM_TOKEN`
- `QISKIT_IBM_INSTANCE`
- `CRN`
- `API key`
- `token=`
- `instance=`
- `crn:`
- `No token/API key/CRN was printed or saved`

## Suspicious Matches

Matches were limited to:

- environment variable names used by scripts;
- placeholder examples such as `<your-token>` and `<your-instance-crn>`;
- safety warnings that tokens, API keys, and CRNs must not be committed;
- code that reads credentials from environment variables without printing or
  saving the values;
- explicit confirmation strings that no token/API key/CRN was printed or saved.

## Secret-Like Values Found

No actual token, API key, instance CRN, account credential, `.env` file,
private-key file, or local credential file was found in the scanned update
path.

## Action Taken

No redaction was required. The USB copy helper excludes `.git`, `.env`,
credential JSON files, token files, and private-key file extensions.

## Guardrail

IBM QPU validation remains appendix-only. It does not claim hardware advantage
and does not replace the state-vector benchmark.
