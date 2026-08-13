#!/usr/bin/env python3

"""
tag_generator.py

Regenerates the tag/<name>.md stub pages from the tags declared in _posts/.
Each stub renders through _layouts/tagpage.html at /tag/<name>/.

Originally by Long Qian (2017); hardened to tolerate comma-separated tags so
front matter like `tags: code, security` no longer produces a bogus `code,`
tag. Run this after adding/removing posts or changing their tags, then commit
the tag/ changes:

    python3 tag_generator.py

Note: keep post front matter comma-free (`tags: code security`) so Jekyll's own
site.tags keys match the files this script writes.
"""

import glob
import os
import re

POST_DIR = "_posts/"
TAG_DIR = "tag/"


def tags_in(filename):
    """Return the tag tokens from a post's YAML front matter."""
    with open(filename, encoding="utf8") as f:
        in_front_matter = False
        for line in f:
            stripped = line.strip()
            if stripped == "---":
                if in_front_matter:
                    break
                in_front_matter = True
                continue
            if in_front_matter and stripped.startswith("tags:"):
                raw = stripped[len("tags:"):]
                # Split on whitespace and/or commas, drop empties.
                return [t for t in re.split(r"[,\s]+", raw) if t]
    return []


def main():
    all_tags = set()
    for filename in glob.glob(POST_DIR + "*.markdown"):
        all_tags.update(tags_in(filename))

    os.makedirs(TAG_DIR, exist_ok=True)
    for old in glob.glob(TAG_DIR + "*.md"):
        os.remove(old)

    for tag in sorted(all_tags):
        with open(os.path.join(TAG_DIR, tag + ".md"), "w", encoding="utf8") as f:
            f.write(
                "---\n"
                "layout: tagpage\n"
                f'title: "Tag: {tag}"\n'
                f"tag: {tag}\n"
                "robots: noindex\n"
                "---\n"
            )
    print(f"Tags generated, count {len(all_tags)}")


if __name__ == "__main__":
    main()
