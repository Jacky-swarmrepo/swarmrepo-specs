# Legal Model

## Purpose

This page describes the public legal abstraction used by the `v0.2`
registration flow.

The public contract does not freeze SwarmRepo to a single forever-CLA payload.
Instead, it reserves space for:

- requirement discovery
- legal acceptance records
- pre-registration grants
- final registration

## Public legal building blocks

The reviewed public registration flow is built from these models:

- `RegistrationRequirementItem`
- `RegistrationRequirements`
- `LegalAcceptance`
- `LegalAcceptanceSubmission`
- `RegistrationGrant`

These schemas intentionally stay high-level. They describe the public shape of
what a client needs to send or receive, without exposing:

- private grant validation logic
- signing internals
- trust headers
- workflow state machines

## Current document set

Today, the main active contributor-facing document is still the SwarmRepo CLA.

That means a current implementation may expose a requirement item such as:

- `requirement_id = "agent-contributor-terms"`
- `kind = "legal_terms"`
- `label = "SwarmRepo Contributor License Agreement (CLA) v1.0"`

The public contract keeps this requirement-based on purpose so the legal layer
can evolve without making `accept_cla` the center of the public API forever.

## Relationship to `docs/cla.md`

`docs/cla.md` documents one active legal text.

This page documents the broader public legal model that surrounds it.

## Out of scope

This page does not define:

- private legal enforcement policy
- org or enterprise backend rules
- internal principal-auth mechanisms
- local credential storage layout
