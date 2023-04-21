import os
from pathlib import Path
from shutil import copytree, rmtree
import subprocess
from time import sleep


def copy_and_overwrite(from_path, to_path):

    if os.path.exists(to_path):
        rmtree(to_path)

    copytree(from_path, to_path)


sphinx_dir = Path(os.path.dirname(__file__))
home_dir = sphinx_dir.parent
build_dir = sphinx_dir.joinpath('_build')
html_dir = build_dir.joinpath('html')
docs_dir = home_dir.joinpath('docs')
jekyll = docs_dir.joinpath('.nojekyll')

# print(sphinx_dir)
# print(home_dir)
# print(html_dir)
# print(docs_dir)

print()
print("---------------- Process Started ----------------")
print()

process = subprocess.Popen(['make', 'clean'], shell=True)
process.wait()
sleep(0.5)

print()
print("---------------- Documentation Cleaned ----------------")
print()

process = subprocess.Popen(['make', 'html'], shell=True)
process.wait()
sleep(0.5)


print()
print("----------------- Documentation Made -----------------")
print()

print('Publishing Documentation')

copy_and_overwrite(html_dir, docs_dir)

with open(jekyll, 'w', encoding='utf-8') as f:
    f.write('')

print()
print("--------------- Documentation Published ---------------")
print()


print('Ready to Push to Git')


# -------------------------------------------------
