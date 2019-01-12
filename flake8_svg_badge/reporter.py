import sys
from functools import reduce
from textwrap import dedent

from flake8.formatting import base

SEVERITY_ORDER = [
    ('E9', 1),
    ('F', 1),
    ('E', 2),
    ('W', 2),
    ('C', 2),
    ('D', 3)
]
DEFAULT_SEVERITY = 3


def find_severity(code):
    for prefix, sev in SEVERITY_ORDER:
        if code.startswith(prefix):
            return sev
    return DEFAULT_SEVERITY


DEFAULT_COLOR = '#a4a61d'
COLORS = {
    'brightgreen': '#4c1',
    'green': '#97CA00',
    'yellowgreen': '#a4a61d',
    'yellow': '#dfb317',
    'orange': '#fe7d37',
    'red': '#e05d44',
    'lightgrey': '#9f9f9f',
}
COLOR_RANGES = [
    (95, 'brightgreen'),
    (90, 'green'),
    (75, 'yellowgreen'),
    (60, 'yellow'),
    (40, 'orange'),
    (0, 'red'),
]


def find_color(total):
    try:
        xtotal = int(total)
    except ValueError:
        return COLORS['lightgrey']
    for range_, color in COLOR_RANGES:
        if xtotal >= range_:
            return COLORS[color]


class ReportSVGBadge(base.BaseFormatter):

    def __init__(self, options):
        super().__init__(options)

        self.error_points = None
        self.files = {}

    def after_init(self):
        super().after_init()

        if not self.options.image:
            raise Exception('--image must be given to generate svg badge')

    def beginning(self, filename):
        super().beginning(filename)
        self.error_points = 0

    def format(self, error):
        pass

    def finished(self, filename):
        with open(filename) as f:
            lines_cnt = len(f.readlines())
            self.files[filename] = (lines_cnt, min(lines_cnt, self.error_points))

    def handle(self, error):
        self.error_points += find_severity(error.code) * 2

    def stop(self):
        total_lines, bad_lines = reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), self.files.values(), (0, 0))

        percent = '{0:.0f}'.format(round(100 - (bad_lines / total_lines) * 100))
        color = find_color(percent)

        with open(self.options.image, "w") as f:
            f.write(dedent("""<?xml version="1.0" encoding="UTF-8"?>
                <svg xmlns="http://www.w3.org/2000/svg" width="99" height="20">
                    <linearGradient id="b" x2="0" y2="100%">
                        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
                        <stop offset="1" stop-opacity=".1"/>
                    </linearGradient>
                    <mask id="a">
                        <rect width="99" height="20" rx="3" fill="#fff"/>
                    </mask>
                    <g mask="url(#a)">
                        <path fill="#555" d="M0 0h63v20H0z"/>
                        <path fill="{color}" d="M63 0h36v20H63z" />
                        <path fill="url(#b)" d="M0 0h99v20H0z"/>
                    </g>
                    <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
                        <text x="31.5" y="15" fill="#010101" fill-opacity=".3">quality</text>
                        <text x="31.5" y="14">quality</text>
                        <text x="80" y="15" fill="#010101" fill-opacity=".3">{percent}%</text>
                        <text x="80" y="14">{percent}%</text>
                    </g>
                </svg>""".format(percent=percent, color=color)))

    @classmethod
    def add_options(cls, options):
        cls.option_manager = options
        options.add_option(
            '--image',
            help="Svg path to generate",
            parse_from_config=True
        )