# GPT-Math reproducible CI acceptance criteria (2026-10-18)

This checklist distinguishes proposed checks from checks actually executed on the same Git commit.

- [ ] Every production Lean module is inventoried and compiled in GitHub Actions; any research draft excluded from compilation is explicitly marked unverified.
- [ ] The workflow records the Lean/Mathlib toolchain and dependency manifest, and reports trust assumptions (including `native_decide`).
- [ ] Python finite arithmetic is independently recomputed, with negative tests for corrupted certificates and altered witness lists.
- [ ] Workflow artifacts contain the certificate, SHA-256, machine-readable status, and the exact commit SHA.
- [ ] A deliberately failing test makes the workflow fail and leaves inspectable failure logs.
- [ ] A scheduled run on the default branch succeeds; scheduling delays are tolerated and not confused with missing checks.
- [ ] A human-readable report links to the exact successful workflow run and identifies proof scope and unverified claims.

No mathematical novelty or general Erdős–Straus theorem is asserted by this checklist.
