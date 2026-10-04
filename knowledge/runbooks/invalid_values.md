# Invalid Values Runbook

## Problem

Data contains values that violate predefined business rules.

## Examples

- Negative quantity
- Discount greater than 100
- Negative price
- Invalid dates

## Detection

Apply business validation rules to incoming records.

## Recovery

1. Identify invalid records.
2. Determine the cause.
3. Correct the value when a trusted source exists.
4. Otherwise quarantine the record.
5. Re-run validation.

## Safety

Never automatically replace an invalid business value with a guessed value.