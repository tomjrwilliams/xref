from __future__ import annotations

from typing import Optional

import functools
import itertools
import time
import dataclasses

import datetime

import functools

import abc
import collections.abc
import typing
import csv

import hashlib

import sys

import functools

import tempfile
import pathlib

import contextlib
import typing
import json

import dataclasses

import distutils.dir_util
import hashlib

import subprocess

import hashlib

from subprocess import Popen, PIPE, CalledProcessError


@contextlib.contextmanager
def temp_dir():
    with tempfile.TemporaryDirectory() as dp:
        yield dp


def render(
    qmd_text,
    fmt,  # eg. html
    fp_stem,
    root_dir,  # of repo
    with_output=True,
    #
):

    fp_qmd = pathlib.Path(fp_stem + ".qmd")
    fp_html = pathlib.Path(fp_stem + ".html")

    # out_files = str(fp_html).replace(".html", "_files")

    with temp_dir() as dp:

        fp = dp / fp_qmd.name
        fp.parent.mkdir(exist_ok=True, parents=True)

        with fp.open("w+") as f:
            f.write(qmd_text)

        # [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]
        # [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]

        cmd = " ".join(
            [
                "cd {} &&".format(root_dir),
                "quarto",
                "render",
                str(fp),
                "--to {} --execute-daemon-restart".format(
                    fmt
                ),
            ]
        )

        if with_output:
            res = subprocess.run(
                cmd,
                shell=True,
                stdout=sys.stdout,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True,
                # check=True,
                # capture_output=True,
            )
            # subprocess.check_call(cmd, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)
        else:
            res = subprocess.run(
                cmd,
                capture_output=True,
                shell=True,
                # check=True,
            )

        sys.stdout.flush()
        sys.stderr.flush()

        # print("Return code: ", res.returncode)

        assert res.returncode == 0, [
            res.returncode,
            cmd,
            "-----",
            #
        ] + (
            []
            if with_output
            else res.stdout.decode().split("\n")
            + res.stderr.decode().split("\n")
        )

        res_fp = str(fp).replace(".qmd", ".html")
        # res_files = str(fp).replace(".qmd", "_files")

        # assumes self_contained=True (?)

        with pathlib.Path(res_fp).open("r") as ff:
            html = ff.read()
            # print(html)

        # for ffp in pathlib.Path(fp).parent.iterdir():
        #     print(ffp)

        # distutils.dir_util.copy_tree(filesFp, outFiles)

    with fp_html.open("w+") as f:
        f.write(html)

    return fp_html
