<!-- ---
disqus: jbold569.disqus.com
--- -->

<div id="banner" class="page-image">
    <img src="../img/2021-07-17-blog-banner.drawio.svg" alt="Lisa Brewster">
    <div class="page-image-caption">
        <p>
            <a href="https://flic.kr/p/9NdAX1">Flickr Lisa Brewster</a>
        </p>
    </div>
</div>

<!-- Reposition the banner image on top -->
<script>
    var article = document.getElementsByTagName("article")[0];
    article.insertBefore(document.getElementById("banner"), article.childNodes[0]);
</script>

# Automating Docs as Code

2021 Jul 17 by [Jason Bolden](../about.md)


This may be an unpopular opinion, but software engineers are notoriously bad at maintaining documentation. I don't believe that's any fault of our own. Moving at break-neck speeds to keep up with changing technology while pausing to record the trials and tribulations of the journey takes that much more time away from your Product Owner's tight deadlines. [Docs as Code](https://www.docslikecode.com/articles/change-case-study/) as a methodology is arguably magnitudes more convenient than maintaining a Sharepoint site or Word document, but what if we could make things just a little simpler for the lazy coder?

## Objective
In this article, we're going to explore a handful of methods to make capturing documentation a little more convenient. As a working example, we'll walk through a python module that generates templated blog posts. Github is used to maintain our documentation and actions are leveraged to orchestrate all of our tedious steps.

<figure>
  <img src="../img/2021-07-17-conceptual.drawio.svg" />
  <figcaption>Figure 1 - Conceptual of our 3 phased approach to automation</figcaption>
</figure>

!!! attention
    There's a lot of moving pieced in this setup. It's important to note that this write up is focused on the art of the possible and snippets shared are enough for a presentable proof of concept. 

## Steps
Assuming you have a fresh repo ready to go, let's start at the top.

### Automating Inception
We're going to use GitHub's functionality as our starting point when creating a new blog, specifically [Issues](https://guides.github.com/features/issues/). Just as an issue would typically be the starting point of a new feature for application development, we're going to treat this as the place where we capture the inspiration for our next blog entry.

Since we're trying to cut out as much manual work as possible, let's take advantage of the template functionality GitHub supports for issues.

```md
---
name: Blog Post template
about: Automation entry point for creation of new blog posts.
title: "[BLOG]"
labels: documentation.blog
assignees: ''

---

title: <TITLE>
type: <tech, insight, idea>
summary: <brief summary of post>

```

Pushing this `.md` file to your repo under the `.github/ISSUE_TEMPLATE` directory will result in a pre-filled issue template that presents information we'll need to provide every time we'd like to make a new blog entry. The body is formatted using `yaml` syntax and the fields will be used as follows:

- `title` - The title of the blog entry.
- `type` - This will be more apparent later, but depending on the type of blog entry, a different template will be used.
- `summary` - This will appear as the first paragraph in the new entry. 

<figure>
  <img src="../img/2021-07-17-issue-template.drawio.svg" />
  <figcaption>Figure 2 - Result of our new issue template</figcaption>
</figure>

Important to note is the label used for this template. This will be used in the workflow that gets triggered next.

What happens when we create our new issue? Nothing, without a workflow defined. We want this workflow to trigger when a new `Issue` has been assigned.

```yaml hl_lines="2-4 8"
name: Orchestrate Issue triggered workflows based on labels
on:
  issues:
    types: [assigned]

jobs:
  blog_issue_assigned:
    if: ${{github.event.issue.labels[0].name == 'documentation.blog'}}
    name: Blog Issue Assigned
    
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8]
```


Now we can use that templated information within a linux environment to take us into phase 2 of our automation flow. 
```yaml hl_lines="2-3"
- name: Generate Blog Entry and Clean Up
  run: |
    echo "${{github.event.issue.body}}" > src/config.yml
    cat src/config.yml
```

!!! note
    The commands for building a new blog entry only happen if the issue that triggered the GitHub workflow has a label of `documentation.blog`.

### Automating Boilerplate Code
For a moment assume we had to manually create this new blog entry. For our blog, we're using [mkdoc](https://www.mkdocs.org/). We would need to add the following to our directory structure every time:

- New `.md` file under the blog directory
- Type the file name with the correct naming convention
- Add the new file to the `mkdocs.yml` file's `nav` definition

```bash hl_lines="7"
.
├── docs
.   .
.   .
.   .
│   ├── blog
│   │   ├── 2021-07-17-automating-docs-as-code.md
│   │   └── readme.md
│   └── index.md
└── mkdocs.yml
```

```yaml hl_lines="6 7"
nav:
  - Home: index.md
  - About: about.md
  - Blogs:
    - Content: blog/readme.md
    - 2021:
      - Automating Docs as Code: blog/2021-07-17-automating-docs-as-code.md
```

These steps may be small and low effort, but over time these added steps become the annoyances that cause one to avoid capturing documentation. We're going to address this by using some python code.

!!! Attention
    The code referenced in this post are snippets of the [profile_builder](https://github.com/jbold569/profile/tree/main/src/profile_builder) module used to create it. The entire module is outside of the scope of this discussion, but feel free to explore how the profile_builder works under the hood as an exercise.  

The logic of the `profile_builder` is straightforward:

- Load our config file as a dictionary, `#!python builder()`
- Load the appropriate template file (based on the blog type), `#!python generate_blog(...)`
- Create the filenames and output directories based on date and config parameters, lines 5-8

``` python
# Perform the initial build
# Build the .md file and write to blog directory
# templates - directory location of ".j2" files
config = builder()        
config['publish_date'] = date.today()
template_file = f"{templates}/blog-post-{config['type']}.md.j2"
blog_filename = f"{config['publish_date']:%Y-%m-%d}-{slugify(config['title'])}.md"
dest_file = f"{output_dir}/{blog_filename}"
generate_blog(template_file, config, dest_file)
```
!!! note
    Notice that we've parameterized the template filename using the type variable from the issue config.
    ```python
    template_file = f"{templates}/blog-post-{config['type']}.md.j2"
    ```

[Jinja](https://jinja.palletsprojects.com/en/3.0.x/templates/) is a great template engine for programmatically creating documents. Because blogs are pretty much rinse and repeat of the same formatting, why should we spend the time typing it out every time (or even copy pasting every time)? Jinja allows us to use the dict elements in our `config` variable to populate the `{{...}}` expression fields of our template. Once generated, our new entry is written to the `dest_file` directory.

```jinja
<div id="banner" class="page-image">
    <img src="../img/{{ publish_date.strftime('%Y-%m-%d') }}-blog-banner.drawio.svg" alt="">
    <div class="page-image-caption">
        <p>
            <a href="">AUTHOR</a>
        </p>
    </div>
</div>

<!-- Reposition the banner image on top -->
<script>
    var article = document.getElementsByTagName("article")[0];
    article.insertBefore(document.getElementById("banner"), article.childNodes[0]);
</script>

# {{ title }}

{{ publish_date.strftime('%Y %b %d') }} by [Jason Bolden](../about.md)


{{ summary }}

## Objective
## Steps
## Conclusion
## References
```

Lastly, we need to update `mkdocs.yml` file to include our new `2021-07-17-automating-docs-as-code.md` file.

```python
# get the relative path from within the docs directory
p = Path(dest_file)
entry = Path(*p.parts[2:]) 

# Update the mkdocs.yml file nav with the new structure
mkdocs_config = load_config(config_file=mkdocs_file)
update_blog(mkdocs_config, config['publish_date'], {config['title']: str(entry)})
```

### Automating Dev Prep
We're almost done. The only thing remaining is to stitch our `profile_builder` into our `issues_automation` workflow and create our development branch. Again, we could create a new branch manually and run the `profile_builder` module from the command line on a our local, but where's the fun in that?

```yaml
- name: Create new Blog Branch
  run: |
    git checkout -b ${{BRANCH_NAME}}
```

```yaml hl_lines="8-16"
- name: Generate Blog Entry and Clean Up
  run: |
    echo "${{github.event.issue.body}}" > src/config.yml
    cat src/config.yml
    cd src
    python -m profile_builder blog -t ./templates -o ../docs/blog -c ./config.yml -v
    rm config.yml
    cd ..
    git config user.name github-actions
    git config user.email github-actions@github.com
    git add .
    git commit -m "generated ${{BRANCH_NAME}}"
    git push --set-upstream origin ${{BRANCH_NAME}}
```
This code snippet builds on our GitHub Workflow step from [phase 1](#automating-inception). All we're doing is scripting out the actions previously described. To kick the whole thing off, simply create a new `Blog` issue, fill in the details, assign it to yourself, and switch to the newly created blog branch.

<figure>
  <img src="../img/2021-07-17-action-output.drawio.svg" />
  <figcaption>Figure 3 - Completed Action workflow following issue assignment</figcaption>
</figure>

## Conclusion
At first glance, this may seem like overkill for a simple blog. A Wordpress or Squarespace site would be much easier to put together. So instead, let's think about a repo that holds engineering artifacts for the application your team supports. Or how about a knowledge base of training material for your team of developers. Incident response playbooks for your Security Operations Center, IT Help Desk procedures, etc.

This workflow allows for someone to create suggest an addition to the team's documentation, and automate a lot of the repetitive actions that demotivates the individual from creating the documentation in the first place. In addition to the bonus of treating the docs as managed source code, the GitHub repo facilitates a collaborative environment so documentation is less likely to be created in a vacuum without peer review.

## References
- [Jinja](https://jinja.palletsprojects.com/en/3.0.x/)
- [MkDocs](https://www.mkdocs.org/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [GitHub Issues](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)