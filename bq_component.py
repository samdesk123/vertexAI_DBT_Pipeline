# bq_component.py
import kfp.v2.dsl as dsl
from kfp.v2.dsl import component


@component(
    packages_to_install=['google-cloud-bigquery'],
    base_image="python:3.9-slim"
)
def insert_record_to_bigquery(
    project_id: str,
    dataset_id: str,
    table_id: str,
    record_data: str
):
    """Inserts a single JSON record into a BigQuery table."""
    from google.cloud import bigquery
    import json

    client = bigquery.Client()
    table_ref = client.dataset(dataset_id).table(table_id)

    # The record_data is passed as a string and needs to be loaded as a JSON object
    rows_to_insert = [json.loads(record_data)]

    errors = client.insert_rows_json(table_ref, rows_to_insert)
    if errors:
        raise RuntimeError(f"Encountered errors while inserting rows: {errors}")
    else:
        print("New rows have been added.")