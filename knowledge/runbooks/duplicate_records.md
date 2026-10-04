# Duplicate Records Runbook

## Problem

The dataset contains repeated records.

## Common Causes

- Pipeline retry
- Duplicate source events
- Multiple ingestion jobs
- Incorrect merge operation

## Detection

Check duplicate records using the appropriate business key.

## Recovery

1. Identify duplicate records.
2. Determine the correct business key.
3. Keep the valid record.
4. Remove duplicates.
5. Validate record counts.
6. Re-run downstream validation.

## Safety

Do not remove records automatically when the correct business key is uncertain.