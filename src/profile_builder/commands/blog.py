## References https://github.com/mkdocs/mkdocs/blob/d9b957e771bd6380ba5c865b5991b402ac3e1382/mkdocs/commands/serve.py 

import logging

from slugify import slugify
from shutil import Error

from jinja2.exceptions import TemplateNotFound
import jinja2

from datetime import date
from os.path import isdir, isfile, join, abspath

from profile_builder.config import load_config
from profile_builder import utils

log = logging.getLogger(__name__)

def blog(templates=None, config_file=None, output_dir=None, **kwargs):
    """
    Create the directory structure and templates for a new blog entry
    
    Accepts a yaml config to populate a Jinja template and stores the resulting
    .md file in a directory according to the date parameter
    """

    def builder():
        log.info("Building blog...")
        config = load_config(
            config_file=config_file,
        )
        return config

    try:
        # Perform the initial build
        config = builder()
        publish_date = config["publish_date"] if isinstance(config["publish_date"], date) else date.today()
        template_file = f"{templates}/blog-post-{config['type']}.md.j2"
        dest_file = f"{output_dir}/{publish_date:%Y/%m/%d}/{slugify(config['title'])}.md"
        with open(abspath(template_file), 'r', encoding='utf-8', errors='strict') as f:
            template = jinja2.Template(f.read())
            blog = template.render(config)
            if blog.strip():
                utils.write_file(blog.encode('utf-8'), dest_file)
            else:
                log.info(f"Template skipped: '{template_file}' generated empty output.")
    except Exception as e:
        log.warning(f"Error reading template '{template_file}': {e}")    
    except Error as e:
        print(e)
