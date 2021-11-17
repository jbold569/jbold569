---
title: Introducing, DocHive!
description: After reusing the  code, powering this blog, across multiple projects, a definite pattern has come to light. At its core, this python module takes a list of key/value pairs as input, populates a documents template, and updates a mkdocs configuration. This can be leveraged across a multitude of projects to drive many use cases. It only makes sense to rip out this code and turn it into a proper piece of software. This is the start of the document archiver, [DocHive](https://github.com/boldware/dochive).
publish_date: 2021-11-17
filename: 2021-11-17-introducing-dochive
---

--8<-- "includes/abbreviations.md"

<div id="banner" class="page-image">
    <img src="../img/2021-11-17-blog-banner.drawio.svg" alt="">
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

# Introducing, DocHive!

*Posted by [Jason Bolden](../about.md) on Nov 17, 2021*

After reusing the  code, powering this blog, across multiple projects, a definite pattern has come to light. At its core, this python module takes a list of key/value pairs as input, populates a documents template, and updates a mkdocs configuration. This can be leveraged across a multitude of projects to drive many use cases. It only makes sense to rip out this code and turn it into a proper piece of software. This is the start of the document archiver, [DocHive](https://github.com/boldware/dochive).

<h2>Comments</h2>
Continue the discussion [here](https://github.com/jbold569/profile/discussions/45)!

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