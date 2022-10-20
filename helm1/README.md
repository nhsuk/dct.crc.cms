# Helm chart for the dct-application-shared application

You will need the dct-application-shared image locally. The best way to create it is to run:
```
docker build . -t dct-application-shared
```

## Wagtail

Runs the HTTP server on port 8000 using uwsgi in front of wagtail.


## Initializer

A one-off job which runs startup tasks such as migrating the database.

## Redis

Redis cache, exposed with a service.

## Databases

There are two main types of database connection, `mssql` and `sqlite`
mssql is used in production so should be used where possible, sqlite is available
for working locally when a mssql container would be too slow.

When using sqlite, a PersistentVolume resource is required to share the database file between pods

To create a persistent volume, create the following yaml file:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: dct-application-shared-volume-db
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 100Mi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  hostPath:
    path: "/tmp/dct-application-shared-db"
```

Then run `kubectl apply -f your-file-name.yaml`

Run `kubectl get pv` to see your volumes.

## Asset Storage

Assets such as images and documents can be uploaded via the Wagtail CMS. In production, these assets are stored in
azure blob storage via the django-storages package.

In local development, you can run a blob storage emulator by setting a helm value of azureStorage.emulated=true.
An azure storage emulator will run on localhost on port 10000.

You will need another PersistentVolume resource, similar to the PV required by the sqlite database.

To create a persistent volume, create the following yaml file:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: dct-application-shared-volume-assets
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 100Mi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  hostPath:
    path: "/tmp/dct-application-shared-assets"
```

Then run `kubectl apply -f your-file-name.yaml`

Run `kubectl get pv` to see your volumes.

## Changes in version 2.0.0
- The paths opened to application is array eg. .Values.webPaths.
- Updated services.yaml to open ports depending on charts that get deployed.
- Deploy the charts depending on configuration in values file. eg. .Values.webDeployment and .Values.appPort.

## Changes in version 2.1.0
- Use separate paths for hostUrl and intHostUrl to separate frontend paths and cms paths.

## Changes in version 2.1.1
- Add auto scale option to all deployed containers on a namespace.

## Changes in version 2.1.2
- Add following below variables to scale up containers separately.
  - webReplicaCount
  - celeryReplicaCount
  - clockworkReplicaCount
  - delayedJobReplicaCount
  - redisReplicaCount
  - sidekiqReplicaCount
  - webMinReplicas
  - celeryMinReplicas
  - clockworkMinReplicas
  - delayedJobMinReplicas
  - redisMinReplicas
  - sidekiqMinReplicas

## Changes in version 2.1.3
1. Add hostUrlCertSecretName to ingress to add phe service url behind akamai.
