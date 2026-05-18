---
title: "PROPOSAL_TITLE"
options:
  eka:
    schema: eka.v1
    domain: product
    classification:
      C: MODERATE                          # MODERATE for L1 internal; HIGH for L2
      I: HIGH
      A: LOW
    tier: L1
    owner: OWNER_HANDLE
    status: draft
    last_reviewed: YYYY-MM-DD
    next_review: YYYY-MM-DD
    review_cadence: 180d
    codename_refs: []                      # at L2+: list entity codes referenced
    data_subjects: []
    labels: [proposal, rfc]
    related: []                            # link to L2 detailed version if this is an L1 summary
---

# PROPOSAL_TITLE

> **Status:** Draft for Tech Review
> **Owner:** OWNER
> **Last updated:** YYYY-MM-DD
> **Reviewers:** Staff Engineer, Security Lead, Domain Lead

## Summary

ONE_PARAGRAPH_SUMMARY answering: what changes, why now, who's affected, what's the cost.

## Goals

| # | Goal | Measurable outcome |
|---|------|--------------------|
| G1 | First goal | How we'll know |
| G2 | Second goal | How we'll know |

## Non-goals

- Things explicitly out of scope, called out to manage expectations

## Background / current state

Why this matters. What problem are we solving. Brief enough that a
reader unfamiliar with the area gets oriented.

## Proposed design

The high-level shape. Multiple sections as needed.

## Detailed design

Architecture, sequence diagrams, data model, API surface — as
appropriate.

> **If this section grows to contain customer-specific detail,
> threat-model specifics, named platform internals, or anything
> exceeding the repo's `max_tier` — STOP. Split the document.**
> Keep the executive summary here at L1. Promote the detailed
> design to L2 in `{org}-company-docs` and link via `related:`.

## Trade-offs and alternatives considered

Decision log: what we chose, what we considered, why.

## Rollout

Phasing, feature flags, rollback plan.

## Open questions

For tech review. Each open question gets a row with proposed
answer + alternative + recommended decision.

## What's contestable

Choices reasonable people will disagree with. Listed explicitly to
invite challenge in review.

## References

| # | Reference | Type |
|---|-----------|------|
| 1 | EXAMPLE | adr / rfc / vendor doc / paper |
