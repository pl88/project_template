import sys
from pathlib import Path

print(f"Haya! Using Python {sys.version}!")
python_version = sys.argv[1]
project_name = sys.argv[2]
print(f"Python version: {python_version}")
root_dir = Path.cwd()


def generate_makefile(project_name):
    file_name = "Makefile"
    makefile_content = (f"run:\n\tuvicorn {project_name}.src.main:{project_name} --host 0.0.0.0 --port 8000\n\n"
                        f"docker_image:\n\tdocker build -t {project_name} ."
                        )
    if Path(file_name).exists():
        pass
    else:
        Path(file_name).write_text(makefile_content)


def generate_dockerfile(python_version, project_name):
    file_name = "Dockerfile"
    dockerfile_content = (f"FROM python:{python_version}\n\n"
                          "RUN curl -sSL https://install.python-poetry.org | python3 -\n\n"
                          f"WORKDIR /{project_name}\n\n"
                          f"COPY poetry.lock pyproject.toml /{project_name}/\n\n"
                          f"RUN poetry install $(test \"$YOUR_ENV\" == production && echo \"--only=main\") --no-interaction --no-ansi\n\n"
                          "COPY . /code"
                          )
    if Path(file_name).exists():
        pass
    else:
        Path(file_name).write_text(dockerfile_content)


def generate_docker_composefile():
    file_name = "docker-compose.yaml"
    docker_compose_version = "3.9"
    docker_compose_content = (f"version: '{docker_compose_version}'\n\n"
                              f"services:\n"
                              f"  {project_name}:\n"
                              f"    build:\n"
                              f"      context: .\n"
                              f"      dockerfile: Dockerfile\n"
                              f"    volumes:\n"
                              f"      - .:/code\n"
                              )
    if Path(file_name).exists():
        pass
    else:
        Path(file_name).write_text(docker_compose_content)

def generate_app_file(project_name):
    file_name = f"{project_name}.py"
    app_file_content = (f"import os\n"
                        f"import sys\n"
                        f"from pathlib import Path\n\n"
                        f"print(f\"Hello! This is {project_name}!\")\n"
                        )
    if Path(file_name).exists():
        pass
    else:
        Path(file_name).write_text(app_file_content)


root_dir.joinpath(project_name, "src").mkdir(parents=True, exist_ok=True)
root_dir.joinpath(project_name, "src", "__init__.py").touch()
root_dir.joinpath(project_name, "tests").mkdir(parents=True, exist_ok=True)

path_to_main = root_dir.joinpath(project_name, "src", "main.py")
generate_app_file(path_to_main)

generate_dockerfile(python_version, project_name)
generate_makefile(project_name)
