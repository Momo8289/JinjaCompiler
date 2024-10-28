from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from os.path import join
from utils import empty_dir, copy_file
import time
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
import sys
import argparse
from compile import compile_dir



def run_watcher(args: argparse.Namespace):
    templates_dir = args.templates_dir
    out_dir = args.output_dir
    pages_dir = args.pages_dir
    template_types = args.types.split(",")
    class EventHandler(FileSystemEventHandler):
        def on_any_event(self, event: FileSystemEvent):
            if event.event_type in ["modified", "created", "deleted"]:
                print("Changes detected, re-compiling")
                try:
                    compile_dir(
                        templates_dir, 
                        pages_dir, 
                        out_dir, 
                        template_types,
                        no_copy=args.no_copy
                    )
                except Exception as e:
                    print(e)

    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, templates_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        return
    finally:
        observer.stop()
        observer.join()


def main(args: argparse.Namespace):
    templates_dir = args.templates_dir
    out_dir = args.output_dir
    pages_dir = args.pages_dir
    template_types = args.types.split(",")

    print(args)

    for path in [templates_dir, out_dir, join(templates_dir, pages_dir)]:
        if not os.path.exists(path):
            print(f"Directory '{path}' does not exist.")
            return
    
    compile_dir(
        templates_dir, 
        pages_dir, 
        out_dir, 
        template_types,
        no_copy=args.no_copy,
    )

    if args.watch:
        run_watcher(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="JinjaCompiler",
        description="Compile Jinja templates into static HTML files",
    )   

    parser.add_argument("templates_dir", help="Path to the directory containing the Jinja templates")
    parser.add_argument("output_dir", help="Path where the compliled files should go. Folder structure will copy that of pages_dir. Directory contents are deleted before compiling, dont put stuff in here that you want to keep.")
    parser.add_argument("-p", "--pages-dir", default="pages/", help="Relative path in templates_dir which contains the templates that will be compiled to HTML. Default: 'pages/'")
    parser.add_argument("-w", "--watch", action="store_true", help="Run in watcher mode, which will monitor templates_dir for changes and automatically recompile.")
    parser.add_argument("-t", "--types", default="jinja", help="Comma-separated list of file types that will be treated as Jinja templates. Default: .jinja")
    parser.add_argument("-n", "--no-copy", action="store_true", help="Don't copy non-template files into output directory.")

    args = parser.parse_args()

    main(args)
