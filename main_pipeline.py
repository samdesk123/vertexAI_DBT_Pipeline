# main_pipeline.py
import kfp.v2 as kfp
from kfp.v2 import compiler
from google.cloud import aiplatform

# Load components from files
dbt_run_op = kfp.components.load_component_from_file('dbt_component.yaml')
from bq_component import insert_record_to_bigquery

@kfp.dsl.pipeline(
    name='dbt-and-bq-pipeline',
    pipeline_root='gs://your-gcs-bucket/pipeline-artifacts'
)
def dbt_and_bq_pipeline(
    project_id: str,
    dataset_id: str,
    table_id: str,
    record_data: str
):
    # Step 1: Run the dbt transformation
    dbt_task = dbt_run_op()

    # Step 2: Insert a record into BigQuery after the dbt task completes
    insert_task = insert_record_to_bigquery(
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
        record_data=record_data
    )

    # Chain the tasks to create a dependency
    insert_task.after(dbt_task)