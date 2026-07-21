# Fix GitHub LaTeX rendering regression

**Date:** 2026-07-21

## Problem

The portfolio README introduced `\(...\)` and `\[...\]` delimiters. GitHub Markdown does not reliably render those delimiters in repository README files.

## Decision

Use GitHub-supported dollar-delimited math in Markdown:

- inline: `$...$`;
- display: `$$...$$`.

No mathematical content or scientific claim changes.
