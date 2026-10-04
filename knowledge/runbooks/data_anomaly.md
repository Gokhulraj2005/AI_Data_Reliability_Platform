# Data Anomaly Recovery Runbook

## Problem
Unexpected values or statistical anomalies are detected in the dataset.

## Investigation
1. Check numerical columns for unusual values.
2. Compare values against historical ranges.
3. Use IQR or statistical thresholds to identify anomalies.
4. Verify whether the anomaly is caused by a valid business event.

## Recovery
Do not automatically modify anomalous values unless the correction rule is known.

## Safety
Anomaly correction may require human approval because unusual values may represent legitimate business events.