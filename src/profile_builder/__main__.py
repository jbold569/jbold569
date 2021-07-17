#!/usr/bin/env python

"""
profile_builder
"""

import logging
import sys
import os

from . import __version__
from . import utils
from . import config
from .commands import blog

import click
import textwrap
import shutil

log = logging.getLogger(__name__)

config_help = "Provide a specific Profile_Builder config"

class ColorFormatter(logging.Formatter):
    colors = {
        'CRITICAL': 'red',
        'ERROR': 'red',
        'WARNING': 'yellow',
        'DEBUG': 'blue'
    }

    text_wrapper = textwrap.TextWrapper(
        width=shutil.get_terminal_size(fallback=(0, 0)).columns,
        replace_whitespace=False,
        break_long_words=False,
        break_on_hyphens=False,
        initial_indent=' '*12,
        subsequent_indent=' '*12
    )

    def format(self, record):
        message = super().format(record)
        prefix = f'{record.levelname:<8} -  '
        if record.levelname in self.colors:
            prefix = click.style(prefix, fg=self.colors[record.levelname])
        if self.text_wrapper.width:
            # Only wrap text if a terminal width was detected
            msg = '\n'.join(
                self.text_wrapper.fill(line)
                for line in message.splitlines()
            )
            # Prepend prefix after wrapping so that color codes don't affect length
            return prefix + msg[12:]
        return prefix + message


class State:
    ''' Maintain logging level.'''

    def __init__(self, log_name='profile_builder', level=logging.INFO):
        self.logger = logging.getLogger(log_name)
        # Don't restrict level on logger; use handler
        self.logger.setLevel(1)
        self.logger.propagate = False

        self.stream = logging.StreamHandler()
        self.stream.setFormatter(ColorFormatter())
        self.stream.setLevel(level)
        self.stream.name = 'ProfileBuilderStreamHandler'
        self.logger.addHandler(self.stream)

        # Add CountHandler for strict mode
        self.counter = utils.log_counter
        self.counter.setLevel(logging.WARNING)
        self.logger.addHandler(self.counter)

pass_state = click.make_pass_decorator(State, ensure=True)

def add_options(opts):
    def inner(f):
        for i in reversed(opts):
            f = i(f)
        return f

    return inner

def verbose_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        if value:
            state.stream.setLevel(logging.DEBUG)
    return click.option('-v', '--verbose',
                        is_flag=True,
                        expose_value=False,
                        help='Enable verbose output',
                        callback=callback)(f)

common_options = add_options([verbose_option])
# Might have a use for this, might not
# common_config_options = add_options([
#     click.option('-f', '--config-file', type=click.File('rb'), help=config_help),
#     # Don't override config value if user did not specify --strict flag
#     # Conveniently, load_config drops None values
#     click.option('-s', '--strict', is_flag=True, default=None, help=strict_help),
#     click.option('-t', '--theme', type=click.Choice(theme_choices), help=theme_help),
#     # As with --strict, set the default to None so that this doesn't incorrectly
#     # override the config file
#     click.option('--use-directory-urls/--no-directory-urls', is_flag=True, default=None, help=use_directory_urls_help)
# ])

PYTHON_VERSION = sys.version[:3]

PKG_DIR = os.path.dirname(os.path.abspath(__file__))


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(
    __version__,
    '-V', '--version',
    message=f'%(prog)s, version %(version)s from { PKG_DIR } (Python { PYTHON_VERSION })'
)
#@common_options
def cli():
    """
    Profile_builder - Profile site built with Markdown.
    """

@cli.command(name="blog")
@click.option('-t', '--templates', type=click.Path(), help='template help', default='./templates')
@click.option('-c', '--config', type=click.File(), help='config help', default='./config.yml')
@click.option('-o', '--output-dir', type=click.Path(), help="output help", default='../docs/blog')
@click.option('-m', '--mkdocs-file', type=click.File(), help="mkdocs help", default='../mkdocs.yml')
@common_options
# @common_config_options
def blog_command(templates, config, output_dir, mkdocs_file, **kwargs):
    """Generate new blog according to arguments"""
    blog.blog(templates=templates, config=config, output_dir=output_dir, mkdocs_file=mkdocs_file, **kwargs)

if __name__ == '__main__':
    cli()