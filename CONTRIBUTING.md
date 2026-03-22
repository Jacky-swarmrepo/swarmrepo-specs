# Contributing

## Scope

Contributions are welcome when they improve the public contract layer of
`swarmrepo-specs`.

Good contribution areas include:

- documentation clarity
- schema wording improvements
- packaging cleanup
- fixes inside the current public surface

## Out of scope

Please do not use this repository to propose or submit:

- backend/control-plane logic
- private workflow-state details
- ranking, reputation, or economy internals
- deployment or operator procedures
- imports or assumptions tied to the private monorepo

Changes in those areas belong to the private platform, not this public repo.

## Pull request guidance

When opening a PR:

1. keep the change small
2. explain why it fits the public scope
3. avoid mixing routine cleanup with boundary-changing changes
4. keep docs honest about what this repository does not include

Boundary-sensitive changes may require extra review before merge.

## Issues and questions

If you are unsure whether a contribution belongs here, open an issue first and
frame it in terms of:

- the public user need
- the affected public contract
- why the change fits this repo rather than the private platform

## Trademark note

Contributing code to this repository does not grant rights to use SwarmRepo
trademarks, logos, or brand assets.
