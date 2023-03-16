import os
from pathlib import Path
from shutil import copy, copy2, copytree, rmtree

def copy_and_overwrite(from_path, to_path):

    if os.path.exists(to_path):
        rmtree(to_path)

    copytree(from_path, to_path)


sphinx_dir = Path(os.path.dirname(__file__))
home_dir = sphinx_dir.parent
build_dir = sphinx_dir.joinpath('_build')
html_dir = build_dir.joinpath('html')
docs_dir = home_dir.joinpath('docs')


# print(sphinx_dir)
# print(home_dir)
# print(html_dir)
# print(docs_dir)

copy_and_overwrite(html_dir, docs_dir)

print()
print("--------------- Documentation Published ---------------")
print()



