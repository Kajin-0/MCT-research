# Research programs

Each subdirectory contains the scientific state of one research program. Program state files are peers; none is the global repository authority.

Repository-wide navigation is in `research/portfolio_state.md`.

## Required program-state sections

Every program `state.md` should identify:

- objective;
- current state;
- controlling issues and decision records;
- completed foundations;
- unresolved scientific questions;
- manuscript status;
- authorized next gates;
- prohibited or unsupported claims;
- shared dependencies;
- termination or pause criteria.

## Scope semantics

A program statement such as `unauthorized`, `frozen`, or `retired` applies only to that program unless explicitly marked repository-wide.

Programs may share:

- source modules;
- datasets;
- literature records;
- tests;
- analytical derivations;
- first-principles adapters.

Shared use does not merge the programs or their manuscript claims.

## Parallel-agent protocol

An agent working in this repository should:

1. name the program in the issue and PR;
2. state whether shared foundations change;
3. avoid editing unrelated program-state files;
4. record cross-program implications explicitly;
5. use a dedicated branch;
6. preserve superseded records rather than silently rewriting history;
7. update `research/contribution_registry.md` only when contribution or manuscript status changes.

## Adding a new program

Create `research/programs/<program_id>/state.md`, add it to `research/portfolio_state.md`, and assign a distinct contribution ID if it represents a potential completed work.