import sys
import os
from pathlib import Path

print(f"Haya! Using Python {sys.version}!")
python_version = sys.argv[1]
project_name = sys.argv[2]
print(f"Python version: {python_version}")
root_dir = Path.cwd()


def generate_makefile(project_name):
    file_name = "Makefile"
    image_name = f"{project_name}_img"
    makefile_content = (f"run:\n\tdocker compose up -d --remove-orphans\n\n"
                        f"docker_build:\n\tdocker build -t {image_name} .\n\n"
                        f"docker_run:\n\tdocker run -d --name {project_name} -p 8000:8000 {image_name}\n\n"
                        f"docker_restart:\n"
                        f"\tdocker container stop {project_name} && \\\n"
                        f"\tdocker container rm {project_name} && \\\n"
                        f"\tdocker run -d --name {project_name} -p 8000:8000 {image_name}"
                        )
    if Path(file_name).exists():
        pass
    else:
        Path(file_name).write_text(makefile_content)


def generate_dockerfile(python_version, project_name):
    file_name = "Dockerfile"
    dockerfile_content = (
                            f"FROM python:{python_version}\n\n"
                            "ENV PYTHONFAULTHANDLER=1 \\\n"
                            "PYTHONUNBUFFERED=1 \\\n"
                            "PYTHONHASHSEED=random \\\n"
                            "PIP_NO_CACHE_DIR=off \\\n"
                            "PIP_DISABLE_PIP_VERSION_CHECK=on \\\n"
                            "PIP_DEFAULT_TIMEOUT=100 \\\n"
                            "POETRY_NO_INTERACTION=1 \\\n"
                            "POETRY_VIRTUALENVS_CREATE=false \\\n"
                            "POETRY_CACHE_DIR='/var/cache/pypoetry' \\\n"
                            "POETRY_HOME='/usr/local' \\\n"
                            f"POETRY_VERSION=2.1.2\n\n"
                            "RUN curl -sSL https://install.python-poetry.org | python3 -\n\n"
                            f"WORKDIR /{project_name}\n\n"
                            f"COPY poetry.lock pyproject.toml /{project_name}/\n\n"
                            f"RUN poetry install --no-interaction --no-ansi --no-root\n\n"
                            f"COPY ./{project_name}/src /{project_name}\n\n"
                            f"CMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"
                          )
    if Path(file_name).exists():
        pass
    else:
        Path(file_name).write_text(dockerfile_content)


def generate_docker_compose(project_name):
    file_name = "docker-compose.yaml"
    image_name = f"{project_name}_img"
    docker_compose_content = (
                                f"services:\n"
                                f"  {project_name}:\n"
                                f"    ports:\n"
                                f"      - \"8000:8000\"\n"
                                f"    image: {image_name}\n"
                                f"    container_name: {project_name}\n"
                                f"    restart: no\n"
                                f"    volumes:\n"
                                f"      - ./{project_name}/src:/{project_name}/{project_name}\n"
                                f"    command: uvicorn {project_name}.main:app --host 0.0.0 --port 8000\n"
                                f"  db:\n"
                                f"    image: postgres:latest\n"
                                f"    container_name: {project_name}_db\n"
                                f"    restart: no\n"
                                f"    environment:\n"
                                f"      POSTGRES_USER: postgres\n"
                                f"      POSTGRES_PASSWORD: postgres\n"
                                f"      POSTGRES_DB: {project_name}\n"
                                f"    ports:\n"
                                f"      - \"5432:5432\"\n"
                                f"  adminer:\n"
                                f"    image: adminer\n"
                                f"    container_name: {project_name}_adminer\n"
                                f"    restart: no\n"
                                f"    ports:\n"
                                f"      - \"8080:8080\"\n"
                              )
    if Path(file_name).exists():
        pass
    else:
        Path(file_name).write_text(docker_compose_content)

def generate_app_file(project_name):
    file_name = f"{project_name}"
    app_file_content = (f"from fastapi import FastAPI\n"
                        f"\n"
                        f"app = FastAPI()\n"
                        f"\n"
                        f"@app.get(\"/\")\n"
                        f"async def root():\n"
                        f"    return {{\"message\": \"Hello! This is {project_name}!\"}}\n"
                        f"\n"
                        )
    if Path(file_name).exists():
        pass
    else:
        Path(file_name).write_text(app_file_content)


root_dir.joinpath(project_name, "src").mkdir(parents=True, exist_ok=True)
root_dir.joinpath(project_name, "src", "__init__.py").touch()
root_dir.joinpath(project_name, "src", "routers").mkdir(parents=True, exist_ok=True)
root_dir.joinpath(project_name, "src", "routers", "__init__.py").touch()
root_dir.joinpath(project_name, "src", "models").mkdir(parents=True, exist_ok=True)
root_dir.joinpath(project_name, "src", "models", "__init__.py").touch()
root_dir.joinpath(project_name, "src", "schemas").mkdir(parents=True, exist_ok=True)
root_dir.joinpath(project_name, "src", "schemas", "__init__.py").touch()
root_dir.joinpath(project_name, "src", "repositories").mkdir(parents=True, exist_ok=True)
root_dir.joinpath(project_name, "src", "repositories", "__init__.py").touch()
root_dir.joinpath(project_name, "tests").mkdir(parents=True, exist_ok=True)
root_dir.joinpath(project_name, "tests", "__init__.py").touch()

path_to_main = root_dir.joinpath(project_name, "src", "main.py")
generate_app_file(path_to_main)

generate_dockerfile(python_version, project_name)
generate_makefile(project_name)
generate_docker_compose(project_name)

os.system(f"poetry run alembic init {root_dir.joinpath(project_name, "src", "migrations")}")
