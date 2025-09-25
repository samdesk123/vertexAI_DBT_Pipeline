# run_pipeline.py
import kfp.v2.compiler as compiler
from google.cloud import aiplatform

# Import the pipeline definition from main_pipeline.py
from main_pipeline import dbt_and_bq_pipeline

# ---- Configuration ----
PROJECT_ID = 'gcp-wow-rwds-ai-mmm-dev'
REGION = 'us-central1'
GCS_BUCKET = 'wx-d9688460-674a-444a-95b2-64672838518d'
PIPELINE_ROOT = f'gs://{GCS_BUCKET}/pipeline_root'
DATASET_ID = 'shubham'
TABLE_ID = 'test_vertexai'
# The data to insert, as a JSON string
RECORD_DATA = '{"name": "shubham", "surname": "singh", "role": "CA"}'

# ---- Pipeline Execution ----
if __name__ == '__main__':
    # 1. Compile the pipeline
    compiler.Compiler().compile(
        pipeline_func=dbt_and_bq_pipeline,
        package_path='dbt_and_bq_pipeline.json'
    )

    # 2. Initialize the Vertex AI SDK
    aiplatform.init(
        project=PROJECT_ID,
        location=REGION
    )

    # 3. Create and run the pipeline job
    job = aiplatform.PipelineJob(
        display_name='dbt-and-bq-job',
        template_path='dbt_and_bq_pipeline.json',
        pipeline_root=PIPELINE_ROOT,
        parameter_values={
            'project_id': PROJECT_ID,
            'dataset_id': DATASET_ID,
            'table_id': TABLE_ID,
            'record_data': RECORD_DATA
        }
    )

    job.run()