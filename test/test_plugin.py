import os
import tempfile
from optparse import Values
from shutil import rmtree
from uuid import uuid4

import pytest
import xmltodict as xmltodict
from flake8.style_guide import Violation

from flake8_svg_badge.reporter import ReportSVGBadge


def test_exception_on_no_image_path():

    with pytest.raises(Exception):
        rp = ReportSVGBadge(Values({'output_file': None}))


def test_parse_file_no_errors():
    target_path = os.path.join(tempfile.gettempdir(), str(uuid4()))
    os.makedirs(target_path)

    cwd = os.getcwd()
    os.chdir(target_path)
    try:
        rp = ReportSVGBadge(Values({'output_file': None, 'image': '123.svg'}))

        with open('lala.py', 'w') as f:
            f.write('print(123)\n')
            f.write('print(123)\n')

        with open('lulu.py', 'w') as f:
            f.write('print(123)\n')
            f.write('print(123)\n')

        rp.beginning('lala.py')
        rp.finished('lala.py')

        rp.beginning('lulu.py')
        rp.finished('lulu.py')

        rp.stop()

        with open("123.svg") as f:
            el = xmltodict.parse(f.read())

        assert el['svg']['g'][1]['text'][3]['#text'] == '100%'
    finally:
        os.chdir(cwd)
        rmtree(target_path)


def test_parse_file_one_error():
    target_path = os.path.join(tempfile.gettempdir(), str(uuid4()))
    os.makedirs(target_path)

    cwd = os.getcwd()
    os.chdir(target_path)
    try:
        rp = ReportSVGBadge(Values({'output_file': None, 'image': '123.svg'}))

        with open('lala.py', 'w') as f:
            f.write('print(123)\n')
            f.write('print(123)\n')

        with open('lulu.py', 'w') as f:
            f.write('print(123)\n')
            f.write('print(123)\n')
            f.write('print(123)\n')
            f.write('print(123)\n')

        rp.beginning('lala.py')
        rp.finished('lala.py')

        rp.beginning('lulu.py')
        rp.handle(Violation('F101', 'lulu.py', 123, 123, 123, 123))
        rp.finished('lulu.py')

        rp.stop()

        with open("123.svg") as f:
            el = xmltodict.parse(f.read())

        assert el['svg']['g'][1]['text'][3]['#text'] == '67%'
    finally:
        os.chdir(cwd)
        rmtree(target_path)

