kubectl create secret generic azcreds --from-literal=AZ_SUBSCRIPTION_ID='0fe1cc35-0cfa-4152-97d7-5dfb45a8d4ba' \
                                      --from-literal=AZ_TENANT_ID='72f988bf-86f1-41af-91ab-2d7cd011db47' \
                                      --from-literal=AZ_CLIENT_ID='6e85e789-3b22-4edb-89d0-2ab7fc09d488' \
                                      --from-literal=AZ_CLIENT_SECRET='73c9a58f-6080-4ff1-9619-e0e3c0a35d7f' \
                                      -n kubeflow
