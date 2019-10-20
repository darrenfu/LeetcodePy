import glob
import re
import os

parent_dir = '/Users/dofu/workspace/LcPy/jupyter-notebook/'
fns = glob.glob(f'{parent_dir}*.*.ipynb')
for fn in fns:
	name = fn[len(parent_dir):]
	prefix = re.sub(r"(\d{1,4})\..*\.ipynb", r"\1", name)
	suffix = re.sub(r"\d{1,4}(\..*\.ipynb)", r"\1", name)
	if 1 <= len(prefix) < 4:
		nm = f"{parent_dir}{prefix.zfill(4)}{suffix}"
		os.rename(fn, nm)
