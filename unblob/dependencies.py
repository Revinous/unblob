import shutil
from typing import List, Type

import attr

from .models import Handler


@attr.define
class Dependency:
    command: str
    is_installed: bool


INSTALLED = "✓"
NOT_INSTALLED = "✗"


def get_dependencies(handlers: List[Type[Handler]]) -> List[Dependency]:
    all_commands = set(handler._get_extract_command() for handler in handlers)
    rv = []
    for command in sorted(all_commands):
        is_installed = shutil.which(command) is not None
        rv.append(Dependency(command=command, is_installed=is_installed))
    return rv


def pretty_format_dependencies(dependencies: List[Dependency]) -> str:
    longest_key_length = max(len(dep.command) for dep in dependencies)
    lines = ["The following executables found installed, which are needed by unblob:"]
    for dependency in dependencies:
        mark = INSTALLED if dependency.is_installed else NOT_INSTALLED
        lines.append(f"    {dependency.command:<{longest_key_length}}    {mark}")
    return "\n".join(lines)
