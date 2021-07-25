## References https://github.com/mkdocs/mkdocs/blob/d9b957e771bd6380ba5c865b5991b402ac3e1382/mkdocs/commands/serve.py 

import logging

from slugify import slugify
from shutil import Error

from jinja2.exceptions import TemplateNotFound
import jinja2

from datetime import date
from os.path import isdir, isfile, join, abspath
from pathlib import Path

from profile_builder.config import load_config
from profile_builder import utils

log = logging.getLogger(__name__)

def blog(templates=None, config_file=None, output_dir=None, mkdocs_file=None, **kwargs):
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

    # add new blog to mkdocs config
    def update_blog(config, publish_date: date, entry):
        try:
            config["nav"][2]["Blogs"][1][publish_date.year].insert(0, entry)
        except IndexError as e:
            log.debug(f"Adding new year to mkdocs.yml")
            config["nav"][2]["Blogs"].insert(1, {publish_date.year:[entry]})
        config.write_file()

    def generate_blog(template_file, config, dest_file):
        with open(abspath(template_file), 'r', encoding='utf-8', errors='strict') as f:
            template = jinja2.Template(f.read())
            blog = template.render(config)
            if blog.strip():
                utils.write_file(blog.encode('utf-8'), dest_file)
            else:
                log.info(f"Template skipped: '{template_file}' generated empty output.")
        
    try:
        # Perform the initial build
        # build the .md file and write to blog directory
        config = builder()        
        config['publish_date'] = date.today()
        template_file = f"{templates}/blog-post-{config['type']}.md.j2"
        blog_filename = f"{config['publish_date']:%Y-%m-%d}-{slugify(config['title'])}.md"
        config['filename'] = blog_filename
        dest_file = f"{output_dir}/{blog_filename}"
        
        generate_blog(template_file, config, dest_file)

        # get the relative path from within the docs directory
        p = Path(dest_file)
        entry = Path(*p.parts[2:]) 

        # Update the mkdocs.yml file nav with the new structure
        mkdocs_config = load_config(config_file=mkdocs_file)
        update_blog(mkdocs_config, config['publish_date'], {config['title']: str(entry)})
        
    except Exception as e:
        log.warning(f"Error reading template '{template_file}': {e}")    
    except Error as e:
        print(e)
