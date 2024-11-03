# JinjaCompiler
This program takes a directory containing Jinja templates, renders them, and outputs them for use in a static website.

```
usage: JinjaCompiler [-h] [-p PAGES_DIR] [-w] [-t TYPES] [-n] templates_dir output_dir

Compile Jinja templates into static HTML files

positional arguments:
  templates_dir         Path to the directory containing the Jinja templates
  output_dir            Path where the compliled files should go. Folder structure will copy that of pages_dir. Directory contents
                        are deleted before compiling, dont put stuff in here that you want to keep.

options:
  -h, --help            show this help message and exit
  -p PAGES_DIR, --pages-dir PAGES_DIR
                        Relative path in templates_dir which contains the templates that will be compiled to HTML. Default: 'pages/'
  -w, --watch           Run in watcher mode, which will monitor templates_dir for changes and automatically recompile.
  -t TYPES, --types TYPES
                        Comma-separated list of file types that will be treated as Jinja templates. Default: .jinja
  -n, --no-copy         Don't copy non-template files into output directory.
```

## Compiling as a standalone executable
```bash
python -m venv venv

# If on Linux
source venv/bin/activate

# If on Windows
venv\Scripts\activate

pip install -r requirements.txt
pip install pyinstaller

pyinstaller -F jinja_compiler.py

# Executable will be located in the newly created dist directory
```

## Attribution
The SSE code for auto-reloading with the debug webserver is from the article [Server-sent events in Flask without extra dependencies](https://maxhalford.github.io/blog/flask-sse-no-deps/).
The license for this code (MIT) can be found in `SSE_LICENSE`.