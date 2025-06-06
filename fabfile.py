from datetime import datetime
import json
import os
import subprocess
from shlex import quote, split

from invoke import run as local
from invoke.tasks import task

# Process .env file
if os.path.exists(".env"):
    # Note - this uses setdefault which will not replace existing values
    # Therefore, if there is more than one value for a symbol set in the .env file,
    # the first one will be used.
    with open(".env", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            var, value = line.split("=", 1)
            os.environ.setdefault(var, value)

FRONTEND = os.getenv("FRONTEND", "docker")

PROJECT_DIR = "/app"

LOCAL_MEDIA_FOLDER = "media"
LOCAL_IMAGES_FOLDER = "media/original_images"
LOCAL_DATABASE_NAME = PROJECT_NAME = "campaignresourcecentre"
LOCAL_DATABASE_USERNAME = "campaignresourcecentre"


def dexec(cmd, service="web"):
    return local(
        "docker compose exec -T {} bash -c {}".format(quote(service), quote(cmd))
    )


def sudexec(cmd, service="web"):
    return local(
        "docker compose exec --user=root -T {} bash -c {}".format(
            quote(service), quote(cmd)
        )
    )


@task
def build(c):
    """
    Build the development environment (call this first)
    """
    group = subprocess.check_output(["id", "-gn"], encoding="utf-8").strip()
    local("mkdir -p media database_dumps campaignresourcecentre/static_compiled")
    local("chmod -R 775 media database_dumps campaignresourcecentre/static_compiled")
    if FRONTEND == "local":
        local("docker compose up -d --build web")
    else:
        local("docker compose up -d --build web frontend")
        dexec("npm ci", service="frontend")
    local("docker compose stop")
    print("Project built: now run 'fab start'")


@task
def start(c):
    """
    Start the development environment
    """
    if FRONTEND == "local":
        local("docker compose up -d web")
    else:
        local("docker compose up -d web frontend")

    print("Use `fab sh` to enter the web container and run `djrun`")
    if FRONTEND != "local":
        print("Use `fab npm start` to run the front-end tooling")


@task
def stop(c):
    """
    Stop the development environment
    """
    local("docker compose stop")


@task
def restart(c):
    """
    Restart the development environment
    """
    stop(c)
    start(c)


@task
def destroy(c):
    """
    Destroy development environment containers (database will lost!)
    """
    local("docker compose down")


@task
def sh(c):
    """
    Run bash in the local web container
    """
    subprocess.run(["docker", "compose", "exec", "web", "bash"])


@task
def sh_root(c):
    """
    Run bash as root in the local web container
    """
    subprocess.run(["docker", "compose", "exec", "--user=root", "web", "bash"])


@task
def npm(c, command, daemonise=False):
    """
    Run npm in the frontend container E.G fab npm 'test'
    """
    exec_args = []
    if daemonise:
        exec_args.append("-d")
    subprocess.run(
        ["docker", "compose", "exec"] + exec_args + ["frontend", "npm"] + split(command)
    )


@task
def psql(c):
    """
    Connect to the local postgres DB using psql
    """
    subprocess.run(
        [
            "docker",
            "compose",
            "exec",
            "db",
            "psql",
            f"-d{LOCAL_DATABASE_NAME}",
            f"-U{LOCAL_DATABASE_USERNAME}",
        ]
    )


@task
def kill(c):
    """
    Kills all running docker contaners
    """
    result = local("docker ps -q", warn=True, hide=True)
    if result:
        container_id_list = [id for id in result.stdout.split("\n") if id]
        if container_id_list:
            result = local(
                "docker container kill %s" % " ".join(container_id_list),
                warn=True,
                hide=True,
            )
            if result:
                print("%d running container(s) killed" % len(container_id_list))
            else:
                print(
                    "Docker command exited with code %d: %s"
                    % (result.exited, result.stderr)
                )
        else:
            print("No running containers to kill")
    else:
        print("Docker command exited with code %d: %s" % (result.exited, result.stderr))
    # local("docker container kill $(docker ps -q)")


@task
def qstart(c):
    """
    Quick start - kill, start and SH into the container
    """

    kill(c)

    start(c)
    sh(c)


def delete_docker_database(c, local_database_name=LOCAL_DATABASE_NAME):
    print(f"Deleting existing database {LOCAL_DATABASE_NAME}...")
    dexec(
        "dropdb --if-exists --host db --username={project_name} {database_name}".format(
            project_name=PROJECT_NAME, database_name=LOCAL_DATABASE_NAME
        ),
        "db",
    )

    print(f"Recreating database {LOCAL_DATABASE_NAME}...")
    dexec(
        "createdb --host db --username={project_name} {database_name}".format(
            project_name=PROJECT_NAME, database_name=LOCAL_DATABASE_NAME
        ),
        "db",
    )


@task
def upload_file(c, local_path, remote_path, service):
    command = "docker compose cp {} {}:{}".format(
        quote(local_path), quote(service), quote(remote_path)
    )
    return local(command)


@task
def download_file(c, local_path, remote_path, service):
    command = "docker compose cp {}:{} {}".format(
        quote(service), quote(remote_path), quote(local_path)
    )
    return local(command)


@task
def import_data(c, database_filename):
    """
    Import local data file to the db container.
    """
    delete_docker_database(c)

    # Import the database file to the db container
    print("Importing the database file to the db container...")
    dexec(
        "pg_restore --clean --no-acl --if-exists --no-owner --host db \
            --username={project_name} -d {database_name} {database_filename}".format(
            project_name=PROJECT_NAME,
            database_name=LOCAL_DATABASE_NAME,
            database_filename=database_filename,
        ),
        service="db",
    )
    print(
        "Any superuser accounts you previously created locally will have been wiped and will need to be recreated."
    )


@task
def sync_db(c, env, storageKey):
    if env in ["staging", "integration", "review"]:
        try:
            print(f"Determining latest {env} dump to download...")
            blobs = local(
                f"""az storage blob list \
                    -c crc-v3-backups \
                    --prefix "{env}/" \
                    --account-name digitalcampaignsstorage \
                    --account-key "{storageKey}" \
                    --auth-mode key""",
                warn=True,
                hide=True,
            )
            if blobs:
                blobs_list = json.loads(blobs.stdout)
                if blobs_list:
                    blobs_list.sort(key=extract_datetime_from_blob, reverse=True)
                    latest_blob = blobs_list[0]
                    print(f"Downloading {latest_blob['name']}")
                    local(
                        f"""az storage blob download \
                            -f database_dumps/{env}-db.dump \
                            -c crc-v3-backups \
                            -n {latest_blob['name']} \
                            --account-name digitalcampaignsstorage \
                            --account-key "{storageKey}" \
                            --auth-mode key""",
                        warn=True,
                        hide=True,
                    )
                else:
                    print(f"No {env} dumps found")
                    return

        except Exception as e:
            print("Exception: %s" % e)
            print(
                "Please ensure that you are logged in az cli and have the az cli extension installed."
            )
        else:
            print("Restarting containers to ensure importing succeeds...")
            restart(c)
            print("Attempting to import the database...")
            import_data(c, f"/database_dumps/{env}-db.dump")
            print("All done. You might need to run migrations.")
    else:
        print(
            "Please enter a valid environment name such as 'staging', 'integration' or 'review'"
        )


def extract_datetime_from_blob(blob_properties):
    blob_name = blob_properties["name"]
    datetime_in_name = (
        blob_name.replace("db-dump-", "")
        .replace(".dump", "")
        .replace("review/", "")
        .replace("integration/", "")
        .replace("staging/", "")
    )
    return datetime.strptime(datetime_in_name, "%d-%m-%Y_%H:%M:%S")


@task
def create_dump(c):
    result = local(
        """az pipelines release create \
            --organization "https://dev.azure.com/nhsuk/" \
            --project "dct.campaign-resource-centre-v3" \
            --definition-id 2 \
            --open""",
        warn=True,
        hide=True,
    )
    if result:
        result_object = json.loads(result.stdout)
        # print (json.dumps (result_object, indent=4))
        release_id = result_object["id"]
        release_devops_url = (
            "https://dev.azure.com/nhsuk/dct.campaign-resource-centre-v3/_releaseProgress?_a=release-pipeline-progress&releaseId=%s"
            % release_id
        )
        print(
            "Database dump pipeline triggered - review progress at %s"
            % release_devops_url
        )
    else:
        print(
            "Pipeline trigger failed with error code %d: %s"
            % (result.exited, result.stderr)
        )
        print(
            "Please ensure that you are logged in az cli and have the az cli extension installed."
        )


def delete_local_renditions(c, local_database_name=LOCAL_DATABASE_NAME):
    try:
        psql(c, "DELETE FROM images_rendition;")
    except Exception:
        pass

    try:
        psql(c, "DELETE FROM wagtailimages_rendition;")
    except Exception:
        pass


#######
# Utils
#######


def make_bold(msg):
    return "\033[1m{}\033[0m".format(msg)


@task
def dellar_snapshot(c, filename):
    """Snapshot the database, files will be stored in the db container"""
    dexec(
        "pg_dump -d {database_name} -U {database_username} > {filename}.psql".format(
            database_name=LOCAL_DATABASE_NAME,
            database_username=LOCAL_DATABASE_USERNAME,
            filename=filename,
        ),
        service="db",
    ),
    print("Database snapshot created")


@task
def dellar_restore(c, filename):
    """Restore the database from a snapshot in the db container"""
    delete_docker_database(c)

    dexec(
        "psql -U {database_username} -d {database_name} < {filename}.psql".format(
            database_name=LOCAL_DATABASE_NAME,
            database_username=LOCAL_DATABASE_USERNAME,
            filename=filename,
        ),
        service="db",
    ),
    print("Database restored.")


@task
def docker_coverage(c):
    return dexec(
        "coverage erase && coverage run manage.py test \
            --settings=campaignresourcecentre.settings.test && coverage report",
        service="web",
    )


@task
def run_test(c):
    """
    Run python tests in the web container
    """
    subprocess.call(
        [
            "docker",
            "compose",
            "exec",
            "web",
            "python",
            "manage.py",
            "test",
            "--settings=campaignresourcecentre.settings.test",
        ]
    )
