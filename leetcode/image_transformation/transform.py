# This project contains a collection of images (under images/cats-small and images/cats-large) and a collection of pipelines (under pipelines) to be applied to them.
# Your mission, should you choose to accept it, is to apply every pipeline file to every image.
# The pipeline files are guaranteed to contain a well-formatted JSON array of individual transformation operations, for example:
# [
#   { "transform": "scale", "args": [0.75] },
#   { "transform": "grayscale", "args": [] }
# ]
# The exact set of supported transformation operations is defined by the ImageTransformation type.
# Getting started
# The code to enumerate the list of images and pipelines is already written for you. Search for TODO in main.py and you’ll find a description of what to do next.
# Which image-transformation library you use is up to you; you may research online and install any package you like.
import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Any, Tuple
import time
from statistics import mean

from PIL import Image, ImageOps, ImageFilter
# alternative: scikit image

@dataclass(frozen=True)
class TaskProfile:
    image_path: str
    pipeline_name: str
    duration_s: float

# Support transformations such as grayscale, flip horizontally, flip vertically,
# scale, blur, rotate, grayscale
@dataclass(frozen=True)
class Operation:
    op: str
    args: Any # We validate later; JSON may contain wrong shapes

@dataclass(frozen=True)
class Pipeline:
    name: str
    operations: List[Operation]


def _print_benchmark_summary(profiles: List[TaskProfile], total_time: float) -> None:
    if not profiles:
        print("No tasks executed.")
        return

    durations = [p.duration_s for p in profiles]
    slowest = max(profiles, key=lambda p: p.duration_s)

    print("\n=== Image Pipeline Benchmark ===")
    print(f"Total tasks:   {len(profiles)}")
    print(f"Total time:    {total_time:.3f} s")
    print(f"Avg per task:  {mean(durations):.4f} s")
    print(f"Throughput:    {len(profiles) / total_time:.2f} tasks/s")
    print("Slowest task:")
    print(f"  image:       {slowest.image_path}")
    print(f"  pipeline:    {slowest.pipeline_name}")
    print(f"  duration:    {slowest.duration_s:.4f} s")
    print("================================\n")

class ImageTransformer:
    def __init__(self):
        self.pipelines = []

    def _validate_operation(self, op: Operation) -> None:
        if op.op in ("grayscale", "flip_horizontally", "flip_vertically"):
            if op.args not in (None, [], ()):
                raise ValueError(f"{op.op} expects no args, got {op.args}")
        elif op.op == "scale":
            if not op.args or len(op.args) != 1:
                raise ValueError(f"scale expects exactly 1 arg, got {op.args}")
            try:
                scale = float(op.args[0])
                if scale <= 0:
                    raise ValueError(f"scale must be > 0, got {scale}")
            except ValueError:
                raise ValueError(f"scale must be a float, got {op.args[0]}")
        elif op.op == "blur":
            if not op.args or len(op.args) != 1:
                raise ValueError(f"blur expects exactly 1 arg, got {op.args}")
            try:
                radius = float(op.args[0])
                if radius < 0:
                    raise ValueError(f"blur must be >= 0, got {radius}")
            except ValueError:
                raise ValueError(f"blur must be a float, got {op.args[0]}")
        elif op.op == "rotate":
            if not op.args or len(op.args) != 1:
                raise ValueError(f"rotate expects exactly 1 arg, got {op.args}")
            try:
                float(op.args[0])
            except ValueError:
                raise ValueError(f"rotate expects exactly 1 arg, got {op.args}")
        else:
            raise TypeError(f"Invalid op: {op.op}")

    def _tranform(self, img: Image.Image, oper: Operation) -> Image.Image:
        op = oper.op
        args = oper.args
        if op == 'grayscale':
            return ImageOps.grayscale(img)
        if op == 'flip_horizontally':
            return ImageOps.mirror(img)
        if op == 'flip_vertically':
            return ImageOps.flip(img)
        if op == 'scale':
            scale = float(args[0])
            return ImageOps.scale(img, scale)
        if op == 'blur':
            radius = float(args[0])
            return img.filter(ImageFilter.GaussianBlur(radius))
        if op == 'rotate':
            angle = int(args[0])
            return img.rotate(angle)
        raise TypeError(f"Unexpected operation: {op} for image: {img.fp}")

    def _process_one(self, in_path: str, out_dir: str, pipeline: Pipeline) -> Tuple[str, TaskProfile]:
        start = time.perf_counter()

        out_filepath = self._output_filepath(in_path, out_dir, pipeline.name)
        with Image.open(in_path) as img:
            tmp_img = img
            for op in pipeline.operations:
                tmp_img = self._tranform(tmp_img, op)
            tmp_img.save(out_filepath)

        duration = time.perf_counter() - start
        profile = TaskProfile(
            image_path=in_path,
            pipeline_name=pipeline.name,
            duration_s=duration,
        )
        return out_filepath, profile

    def _output_filepath(self, image_path: str, out_dir: str, pipeline_name: str) -> str:
        base = os.path.basename(image_path)
        stem, ext = os.path.splitext(base)
        return os.path.join(out_dir, f"{stem}__{pipeline_name}{ext}")

    def load_pipelines(self, pipeline_dir: str):
        pipelines = []
        with os.scandir(pipeline_dir) as inodes:
            for ino in inodes:
                if ino.is_file() and ino.path.lower().endswith('.json'):
                    with open(ino.path) as json_f:
                        json_arr = json.load(json_f)
                        pipeline_name = os.path.splitext(ino.name)[0]
                        ops = [
                            Operation(op=item.get("transform"), args=item.get("args"))
                            for item in json_arr
                        ]
                        pipelines.append(Pipeline(name=pipeline_name, operations=ops))
        if not pipelines:
            raise ValueError(f"No pipeline JSON files found in {pipeline_dir}")
        self.pipelines = pipelines

    def _list_image_files(self, dir_paths: List[str]) -> List[str]:
        files = []
        for dir_path in dir_paths:
            for root, _, names in os.walk(dir_path): # recursively scandir
                for name in names:
                    lower = name.lower()
                    if lower.endswith((".png", ".jpg", ".jpeg")):
                        files.append(os.path.join(root, name))
        return files

    def run(self, dir_paths: List[str], out_dir: str, max_workers: int | None = None) -> None:
        if not self.pipelines:
            raise ValueError("No pipelines are loaded")
        for p in self.pipelines:
            print("pipeline: ", p.name)
            for op in p.operations:
                self._validate_operation(op)

        image_paths = self._list_image_files(dir_paths)

        tasks = []
        profiles: List[TaskProfile] = []
        t0 = time.perf_counter()
        # CPU pool
        with ProcessPoolExecutor(max_workers=max_workers) as exc:
            for img_path in image_paths:
                for pipeline in self.pipelines:
                    task = exc.submit(
                        self._process_one, img_path, out_dir, pipeline)
                    tasks.append(task)

            for fut in as_completed(tasks):
                # This is required.
                # Otherwise you fire a bunch of tasks then immediately exit
                _, profile = fut.result()
                profiles.append(profile)

        t1 = time.perf_counter()
        total_time = t1 - t0
        _print_benchmark_summary(profiles, total_time)

if __name__ == "__main__":
    transformer = ImageTransformer()
    transformer.load_pipelines("pipelines/")
    max_workers = 2
    transformer.run(["images/"], "out/", max_workers)