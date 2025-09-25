FROM python:3.9-slim

# Add the --trusted-host flag to your pip install command
RUN pip install --no-cache-dir --upgrade --force-reinstall dbt-bigquery --trusted-host pypi.org --trusted-host files.pythonhosted.org

RUN mkdir  /dbt

COPY . /dbt

WORKDIR /dbt/vertexAI

RUN ls -a

ENTRYPOINT [ "dbt" ]