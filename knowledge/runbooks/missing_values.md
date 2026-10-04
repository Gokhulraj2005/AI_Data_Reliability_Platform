# Missing Values Runbook

## Problem

Required fields contain null or missing values.

## Common Causes

- Incomplete source records
- API failures
- Incorrect data transformation
- Missing source-system fields

## Detection

Calculate missing-value counts for every column.

## Recovery

1. Identify affected columns.
2. Determine whether the field is required.
3. Use an appropriate strategy:
   - Remove invalid records
   - Fill with a valid default
   - Forward fill when appropriate
   - Use statistical imputation
4. Validate the repaired dataset.
5. Re-run the pipeline.

## Safety

Do not automatically fill critical business fields without validation.