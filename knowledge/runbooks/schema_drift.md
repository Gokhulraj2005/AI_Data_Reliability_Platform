# Schema Drift Runbook

## Problem

Schema drift occurs when the structure of incoming data changes from the expected schema.

## Common Causes

- Column renamed
- Column removed
- New column added
- Data type changed
- Source-system update

## Detection

Compare incoming columns with the expected schema.

## Recovery

1. Identify missing expected columns.
2. Identify unexpected columns.
3. Map renamed columns when the mapping is known.
4. Validate data types.
5. Re-run the pipeline.

## Safety

Automatic schema changes should require human approval when the mapping is uncertain.