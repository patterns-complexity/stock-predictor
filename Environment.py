from environs import Env
from os import path
from enum import Enum
from argparse import ArgumentParser
from tabulate import tabulate
from colorama import Fore, Style


class Environment(Enum):
    TRAIN = 'train'
    PREDICT = 'predict'


parser = ArgumentParser()

parser.add_argument(
    '-e', '--environment',
    type=str,
    default=Environment.TRAIN.value,
    help='Environment to load',
    required=False
)

arguments = parser.parse_known_args()[0]

abspath = path.abspath(path.curdir)
strpath = f'{abspath}/.env.{arguments.environment}'
path = path.normpath(strpath)

env = Env()
env.read_env(path=path)


def read_env(path):
    file_content = ''

    with open(path) as env_file:
        file_content = env_file.read()

    return file_content


def parse_env(file_content):
    sections = []

    for line in file_content.splitlines():
        if line.strip() == '':
            continue

        if line.startswith('#'):
            sections.append([f"{line.split('#')[1].strip()}", []])
            continue

        sections[-1][1].append([
            line.split('=')[0],
            line.split('=')[1].split('#')[0],
            line.split('#')[1]
            if len(line.split('#')) > 1
            else None,
        ])

    return sections


def print_env(sections, colors):
    for section in sections:
        print(colors.pop(0) + f'# {section[0]}')
        print(tabulate(
            section[1],
            headers=["Variable", "Value", "Description"]
        ))
        print("\n" + Style.RESET_ALL)


def generate_markdown_table(sections):
    markdown = ''

    for section in sections:
        markdown += '\n\n'
        markdown += f'### {section[0]}\n'
        markdown += '| Variable | Value | Description |\n'
        markdown += '| --- | --- | --- |\n'
        markdown += '\n'.join(
            [
                f'| {variable[0]} | \
                `{variable[1] if len(variable[1]) < 20 else (variable[1][0:20] + "...")}` \
                | {variable[2]} |'
                for variable in section[1]
            ]
        )

    return markdown


def replace_markdown_table_in_readme(markdown):
    readme_path = './README.MD'

    with open(readme_path, 'r') as readme_file:
        readme_content = readme_file.read()

    readme_beginning = readme_content.split(
        '\n\n<!-- ENVIRONMENT VARIABLES -->'
    )[0]
    readme_end = readme_content.split(
        '<!-- /ENVIRONMENT VARIABLES -->\n\n'
    )[1]

    readme_content = readme_beginning + \
        '\n\n<!-- ENVIRONMENT VARIABLES -->\n\n' + \
        markdown + \
        '\n\n<!-- /ENVIRONMENT VARIABLES -->\n\n' + \
        readme_end

    with open(readme_path, 'w') as readme_file:
        readme_file.write(readme_content)


def overwrite_dist(path):
    with open(f'{path}.dist', 'w') as dist_file:
        dist_file.write(read_env(path))


file_content = read_env(path)
sections = parse_env(file_content)

colors: list[str] = [
    Fore.GREEN,
    Fore.YELLOW,
    Fore.LIGHTGREEN_EX,
    Fore.MAGENTA,
    Fore.RED,
    Fore.BLUE,
    Fore.BLACK,
]

print_env(sections, colors)

markdown = generate_markdown_table(sections)

replace_markdown_table_in_readme(markdown)

overwrite_dist(path)
