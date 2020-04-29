"""Main pipeline file"""
from kubernetes import client as k8s_client
import kfp.dsl as dsl
import kfp.compiler as compiler
from kfp.azure import use_azure_secret
import json
import os


@dsl.pipeline(
    name='Tacos vs. Burritos',
    description='Simple TF CNN'
)

def get_callback_payload(event_type):
    payload = {}
    payload['event_type'] = event_type
    payload['sha'] = os.getenv('GITHUB_SHA')
    payload['pr_num'] = os.getenv('PR_NUM')
    payload['run_id'] = dsl.RUN_ID_PLACEHOLDER
    payload['status'] = '{{workflow.status}}'
    return json.dumps(payload)

def tacosandburritos_train(
    resource_group,
    workspace
):
    """Pipeline steps"""

    persistent_volume_path = '/mnt/azure'
    data_download = 'https://aiadvocate.blob.core.windows.net/public/tacodata.zip'  # noqa: E501
    epochs = 2
    batch = 32
    learning_rate = 0.0001
    model_name = 'tacosandburritos'
    operations = {}
    image_size = 160
    training_folder = 'train'
    training_dataset = 'train.txt'
    model_folder = 'model'
    image_repo_name = "kubeflowyoacr.azurecr.io/mexicanfood"
    callback_url = 'kubemlopsbot-svc.kubeflow.svc.cluster.local:8080'
    train_start_event = 'Training Started'
    train_finish_event = 'Training Finished'

    exit_op = dsl.ContainerOp(
        name='Exit Handler',
        image="curlimages/curl",
        command=['curl'],
        arguments=[
            '-d', get_callback_payload(train_finish_event),
            callback_url 
        ]
    )

            
    with dsl.ExitHandler(exit_op):
        # preprocess data
        start_callback = 
            dsl.InitContainer('callback',
                              'curlimages/curl',
                              command='curl -d ' + get_callback_payload(train_start_event))
        operations['preprocess'] = dsl.ContainerOp(
            name='preprocess',
            init_containers=[start_callback]
            image=image_repo_name + '/preprocess:latest',
            command=['python'],
            arguments=[
                '/scripts/data.py',
                '--base_path', persistent_volume_path,
                '--data', training_folder,
                '--target', training_dataset,
                '--img_size', image_size,
                '--zipfile', data_download
            ]
        )

        # train
        operations['training'] = dsl.ContainerOp(
            name='training',
            image=image_repo_name + '/training:latest',
            command=['python'],
            arguments=[
                '/scripts/train.py',
                '--base_path', persistent_volume_path,
                '--data', training_folder,
                '--epochs', epochs,
                '--batch', batch,
                '--image_size', image_size,
                '--lr', learning_rate,
                '--outputs', model_folder,
                '--dataset', training_dataset
            ]
        )
        operations['training'].after(operations['preprocess'])

        # register model
        operations['register'] = dsl.ContainerOp(
            name='register',
            image=image_repo_name + '/register:latest',
            command=['python'],
            arguments=[
                '/scripts/register.py',
                '--base_path', persistent_volume_path,
                '--model', 'latest.h5',
                '--model_name', model_name,
                '--tenant_id', "$(AZ_TENANT_ID)",
                '--service_principal_id', "$(AZ_CLIENT_ID)",
                '--service_principal_password', "$(AZ_CLIENT_SECRET)",
                '--subscription_id', "$(AZ_SUBSCRIPTION_ID)",
                '--resource_group', resource_group,
                '--workspace', workspace,
                '--run_id', dsl.RUN_ID_PLACEHOLDER
            ]
        ).apply(use_azure_secret())
        operations['register'].after(operations['training'])
    
        operations['finalize'] = dsl.ContainerOp(
            name='Finalize',
            image="curlimages/curl",
            command=['curl'],
            arguments=[
                '-d', get_callback_payload("Model is registered"),
                callback_url
            ]
        )
        operations['finalize'].after(operations['register'])


    # operations['deploy'] = dsl.ContainerOp(
    #     name='deploy',
    #     image=image_repo_name + '/deploy:latest',
    #     command=['sh'],
    #     arguments=[
    #         '/scripts/deploy.sh',
    #         '-n', model_name,
    #         '-m', model_name,
    #         '-t', "$(AZ_TENANT_ID)",
    #         '-r', resource_group,
    #         '-w', workspace,
    #         '-s', "$(AZ_CLIENT_ID)",
    #         '-p', "$(AZ_CLIENT_SECRET)",
    #         '-u', "$(AZ_SUBSCRIPTION_ID)",
    #         '-b', persistent_volume_path,
    #         '-x', dsl.RUN_ID_PLACEHOLDER
    #     ]
    # ).apply(use_azure_secret())
    # operations['deploy'].after(operations['register'])

    for _, op_1 in operations.items():
        op_1.container.set_image_pull_policy("Always")
        op_1.add_volume(
            k8s_client.V1Volume(
              name='azure',
              persistent_volume_claim=k8s_client.V1PersistentVolumeClaimVolumeSource(  # noqa: E501
                claim_name='azure-managed-disk')
            )
        ).add_volume_mount(k8s_client.V1VolumeMount(
            mount_path='/mnt/azure', name='azure'))


if __name__ == '__main__':
    compiler.Compiler().compile(tacosandburritos_train, __file__ + '.tar.gz')
