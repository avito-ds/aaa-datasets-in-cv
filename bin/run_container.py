#!/usr/bin/env python3
import os
import time
import re
import socket
import subprocess

data_docker_compose = """version: '3.8'
name: {project_name}
services:
    {project_name}:
        runtime: nvidia
        build:
          context: ./
          dockerfile: ./Dockerfile
          args:
            CONTEXT: 'dev'
        image: item2param-learning:dev-$USER
        container_name: {project_name}
        environment:
            - TZ=MSK
            - PYTHONUNBUFFERED=1
            - JUPYTER_PASSWORD=$JUPYTER_PASSWORD
            - APP_NAME=item2param-learning
            - USERNAME=$USER
            - OPENBLAS_NUM_THREADS=8
            - DS_VERTICA_USERNAME=$DS_VERTICA_USERNAME
            - DS_VERTICA_PASSWORD=$DS_VERTICA_PASSWORD
            - DS_VERTICA_PORT=$DS_VERTICA_PORT
            - APP_ENVIRONMENT=$APP_ENVIRONMENT
            - SERVICE_INFOMODEL_URL=https://prod.k.avito.ru/service-infomodel
            - SERVICE_ITEM2PARAM_URL=http://staging.k.avito.ru/service-item2param
            - SERVICE_DATASET_COLLECTOR_URL=http://prod.k.avito.ru/service-dataset-collector
            - SERVICE_DATASET_COLLECTOR_TIMEOUT=10000
        volumes:
            - ./:/app
        ports:
            - "{free_port1}:8888"
        shm_size: 16G
        command: /bin/bash -c "cd / && jupyter notebook --allow-root --ip=0.0.0.0 \
            & nohup tensorboard --logdir /data/tensorboard/ --bind_all \
            && sleep infinity"
        restart: unless-stopped
"""


def get_free_random_port():
    sock = socket.socket()
    sock.bind(('', 0))
    _, port = sock.getsockname()
    return port


def get_path_to_docker_compose():
    abs_path_to_script = os.path.abspath(__file__)
    path_to_project = os.path.dirname(os.path.dirname(abs_path_to_script))
    path_to_docker_compose = os.path.join(path_to_project, 'docker-compose.yaml')
    return path_to_docker_compose


def main():
    user = os.getenv('USER')
    project_name = 'aaa-cv-%s' % user

    free_port1 = get_free_random_port()
    free_port2 = get_free_random_port()

    data = data_docker_compose.format(
        project_name=project_name,
        free_port1=free_port1,
        free_port2=free_port2,
    )

    path_to_docker_compose = get_path_to_docker_compose()
    with open(path_to_docker_compose, 'w') as file:
        file.write(data)

    docker_compose_version = subprocess.run(['docker', 'compose', 'version'])
    if docker_compose_version.returncode:
        print('Please install docker compose plugin:')
        print('sudo apt-get update')
        print('sudo apt-get install docker-compose-plugin')
        print('OR look this page')
        print('https://docs.docker.com/compose/install/')
        return

    process_build = subprocess.run(['docker', 'compose', 'build'])
    process_build.check_returncode()

    process_up = subprocess.run(['docker', 'compose', 'up', '-d'])
    process_up.check_returncode()

    time.sleep(5)
    hostname = socket.gethostname()
    process_docker_logs = subprocess.run(
        ['docker', 'logs', project_name], capture_output=True, text=True
    )
    output = process_docker_logs.stdout + process_docker_logs.stderr

    jupyter_url_without_host = re.search(r':8888/', output)
    jupyter_url_without_host = jupyter_url_without_host.group()
    jupyter_url_without_host = jupyter_url_without_host.replace('8888', str(free_port1))
    jupyter_url = 'http://' + hostname + jupyter_url_without_host
    print('-' * 50)
    print(f'Jupyter доступен по ссылке: {jupyter_url}')
    print('-' * 50)


if __name__ == '__main__':
    main()
