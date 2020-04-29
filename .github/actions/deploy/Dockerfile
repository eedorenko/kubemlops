FROM mcr.microsoft.com/azure-cli
RUN pip install --upgrade pip && \
    az extension add -n azure-cli-ml
COPY deploymentconfig.json /scripts/deploymentconfig.json
COPY inferenceconfig.json /scripts/inferenceconfig.json
COPY deploy.sh /scripts/deploy.sh
COPY score.py /scripts/score.py
COPY environment.yml /scripts/environment.yml

