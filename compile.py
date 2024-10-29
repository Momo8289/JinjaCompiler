from jinja2 import Environment, FileSystemLoader, select_autoescape

import os
from os.path import join

from utils import empty_dir, copy_file


def compile_dir(
    templates_dir: str, 
    pages_dir: str, 
    output_dir: str, 
    types: list[str],
    no_copy: bool=False,
    _clear_out: bool=True, 
    _base: str="", 
    _env: Environment=None, 
):
    if not _env:
        _env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape
        )

    if _clear_out: empty_dir(output_dir)

    for file in os.listdir(join(templates_dir, pages_dir)):
        full_path = join(pages_dir, file)
        real_path = join(templates_dir, pages_dir, file)

        if os.path.isdir(real_path):
            os.mkdir(join(output_dir, _base, file))
            compile_dir(
                templates_dir,
                full_path,
                output_dir,
                types,
                no_copy=no_copy,
                _clear_out=False,
                _base=join(_base, file)
            )
            continue

        if not os.path.isfile(real_path):
            # print(f"Skipping non-file '{full_path}'") 
            continue
        
        if not file.split(".")[-1] in types:
            if not no_copy:
                # print(f"Copying non-template file '{file}'")
                copy_file(real_path, join(output_dir, _base, file))
            continue
        
        out_path = join(output_dir, _base, f"{file.split(".")[0]}.html")
        with open(out_path, "w") as out:
            template = _env.get_template(full_path)
            out.write(template.render())
            # print(f"Template '{file}' rendered")