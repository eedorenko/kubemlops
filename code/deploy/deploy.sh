# az ml model deploy -n tacosandburritos -m tacosandburritos:1 --ic inferenceconfig.json --dc deploymentconfig.json --resource-group taco-rg --workspace-name taco-workspace --overwrite -v
#!/bin/sh
while getopts "m:s:p:u:r:w:t:x:" option;
    do
    case "$option" in
        m ) MODEL=${OPTARG};;
        s ) SERVICE_PRINCIPAL_ID=${OPTARG};;
        p ) SERVICE_PRINCIPAL_PASSWORD=${OPTARG};;
        u ) SUBSCRIPTION_ID=${OPTARG};;
        r ) RESOURCE_GROUP=${OPTARG};;
        w ) WORKSPACE=${OPTARG};;
        t ) TENANT_ID=${OPTARG};;
        x ) RUN_ID=${OPTARG};;
    esac
done
# az login --service-principal --username ${SERVICE_PRINCIPAL_ID} --password ${SERVICE_PRINCIPAL_PASSWORD} -t $TENANT_ID
echo $MODEL
echo $WORKSPACE
echo $RESOURCE_GROUP
echo $SUBSCRIPTION_ID
# model_id=$(az ml model list --model-name $MODEL --workspace-name $WORKSPACE -g $RESOURCE_GROUP --subscription-id $SUBSCRIPTION_ID --tag run_id=$RUN_ID | jq -r '.[0] | .id') 
echo $model_id

# az ml model deploy -n "mexicanfood" -m $model_id --ic '/scripts/inferenceconfig.json'  --dc '/scripts/deploymentconfig.json' -w $WORKSPACE -g $RESOURCE_GROUP --overwrite -v
az ml model deploy -h
