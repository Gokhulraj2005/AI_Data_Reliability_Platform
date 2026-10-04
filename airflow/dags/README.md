# Airflow Integration

This folder is reserved for deployment-specific Airflow DAGs. Airflow is intentionally not part of the base requirements because it has a large, environment-sensitive dependency set. Add a DAG here after installing and configuring Airflow for the target environment; invoke the pipeline through its supported API or Python entry point.
