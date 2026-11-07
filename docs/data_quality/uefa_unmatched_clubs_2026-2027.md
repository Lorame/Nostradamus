# UEFA data coverage issue — 2026/2027

## Context

During the construction of the 2026/2027 Champions League qualification
pool, two clubs could not be matched with the UEFA club coefficients source:

- Como — club_id: 79946 — Italy
- N.E.C. — club_id: 52330 — Netherlands

## Findings

Both clubs are present in the qualification pool, with their club IDs,
countries and qualification statuses.

However, neither club was found in:
`data/raw/uefa_club_coefficients_full.csv`

Consequently, their UEFA enrichment fields are missing in the processed
qualification pool.

## Temporary resolution

For the 2026/2027 edition, missing club metadata will be supplemented
manually when verifiable.

Unknown UEFA coefficients and rankings must remain missing rather than
being estimated or invented.

## Follow-up

Improve the UEFA data collection and matching pipeline to reduce
unmatched clubs in future editions.
