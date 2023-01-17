# Get a list of review environment resources to be deleted.
#
# We work this out by looking at kubernetes namespaces and postgres databases.
# If a k8s environment or database exists but the branch doesn't, it needs to be deleted.

PREFIX="dct-crc-v3-review-"

get_k8s_namespaces() {

    ALL_K8S_NAMESPACES=$(kubectl get ns --no-headers | grep "^$PREFIX" | awk '{print $1}')

    # For each namespace, make sure the git branch still exists. If not, delete the namespace
    for namespace in $ALL_K8S_NAMESPACES; do
        # Remove the prefix and postfix from namespace to just get the review name
        REVIEW_NAME=$(echo $namespace | sed 's/dct-crc-v3-review-\(.*\)-ns$/\1/')

        git show-ref --verify --quiet "refs/remotes/origin/review/$REVIEW_NAME"
        if [[ $? -eq 1 ]]; then
            echo "$namespace"
        fi
    done
}

# Currently, databases are shared between environments, so we don't want to delete them on review environments
#get_databases() {
#
#    ALL_DATABASES=$(az postgres db list -s campaigns-cms-psql-dev-uks -g nhsuk-dct-rg-dev-uks --query="[].name" -o tsv | grep "^$PREFIX") #here
#
#    for database in $ALL_DATABASES; do
#        REVIEW_NAME=$(echo $database | sed 's/dct-crcv3-review-\(.*\)$/\1/')
#
#        git show-ref --verify --quiet "refs/remotes/origin/review/$REVIEW_NAME"
#        if [[ $? -eq 1 ]]; then
#            echo "$database"
#        fi
#    done
#}

# Require either k8s or databases as the first argument, and run the appropriate function
if [[ $1 == "k8s" ]]; then
    get_k8s_namespaces
#elif [[ $1 == "databases" ]]; then
#    get_databases
else
    echo "A resource type must be specified. \"k8s\"" > /dev/stderr
    echo "Usage:" > /dev/stderr
    echo "get-resources-to-delete.sh [k8s]" > /dev/stderr
    exit 1
fi