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
  
Important to note is the label used for this template. This will be used in the workflow that gets triggered next.

What happens when we create our new issue? Nothing, without a workflow defined. We want this workflow to trigger when a new `Issue` has been assigned.

```yaml hl_lines="2 3 4"
name: Orchestrate Issue triggered workflows based on labels
on:
  issues:
    types: [assigned]

jobs:
  issue_assigned:
    name: Issue Assigned
    
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8]
```


Now we can use that templated information within a linux environment to take us into phase 2 of our automation flow. 
```yaml hl_lines="4 5 6"
# Ignore the non-highlighted for now
- name: Generate Blog Entry and Clean Up
    env:
        BRANCH_NAME: blog/issue${{github.event.issue.number}}
    if: ${{github.event.issue.labels[0].name == 'documentation.blog'}}
    run: |
        echo "${{github.event.issue.body}}" > src/config.yml
        cat src/config.yml
```

!!! note
    The commands for building a new blog entry only happen if the issue that triggered the GitHub workflow has a label of `documentation.blog`.

### Automating Boilerplate Code


``` python
# Perform the initial build
# build the .md file and write to blog directory
config = builder()        
config['publish_date'] = date.today()
template_file = f"{templates}/blog-post-{config['type']}.md.j2"
blog_filename = f"{config['publish_date']:%Y-%m-%d}-{slugify(config['title'])}.md"
dest_file = f"{output_dir}/{blog_filename}"
```
## Conclusion

# Cheatsheet
## [Admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#supported-types)

!!! note
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

??? note
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

!!! note ""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

!!! note "Other Title"
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

!!! note
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non 
    
    ```python
        import re
        print("Hello World!")
    ```

    consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.