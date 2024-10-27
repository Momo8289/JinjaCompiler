from jinja2 import Environment, PackageLoader, select_autoescape
import os
from os.path import join
from utils import empty_dir, copy_file
import time
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer



pages_dir = "templates/pages"
templates_dir = "templates/"
out_dir = "out/"
template_type = ".jinja"

for path in [templates_dir, out_dir, pages_dir]:
        if not os.path.exists(path):
            os.mkdir(path)

env = Environment(
    loader=PackageLoader("jinja_compiler"),
    autoescape=select_autoescape
)



def compile_dir(path, clear_out=True, base="./"):
    if clear_out: empty_dir(out_dir)

    for file in os.listdir(join(templates_dir, path)):
        full_path = join(path, file)
        real_path = join(templates_dir, path, file)

        if os.path.isdir(real_path):
            os.mkdir(join(out_dir, base, file))
            compile_dir(full_path, base=join(base, file), clear_out=False)
            continue

        if not os.path.isfile(real_path):
            # print(f"Skipping non-file '{full_path}'") 
            continue

        if not file.endswith(template_type):
            # print(f"Copying non-template file '{file}'")
            copy_file(real_path, join(out_dir, base, file))
            continue
        
        out_path = join(out_dir, base, file.replace(template_type, ".html"))
        with open(out_path, "w") as out:
            template = env.get_template(full_path)
            out.write(template.render())
            # print(f"Template '{file}' rendered")


class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent):
        if event.event_type in ["modified", "created", "deleted"]:
            print("Changes detected, re-compiling")
            compile_dir("pages/")


if __name__ == "__main__":
    compile_dir("pages/")
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, "./templates/", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()