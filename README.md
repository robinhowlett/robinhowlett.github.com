# robinhowlett.com

Personal blog of Robin Howlett — built with [Jekyll](https://jekyllrb.com/) on the
"Royce" theme, published to [robinhowlett.com](https://robinhowlett.com/) via GitHub Pages.

## Local development

Requires Ruby 3.x and Bundler.

```bash
bundle install
bundle exec jekyll serve      # http://localhost:4000/
```

The site builds in `Etc/UTC` (`timezone:` in `_config.yml`) so post permalinks match
production regardless of your machine's timezone — don't remove that setting.

### macOS toolchain note

`bundle install` compiles the native `eventmachine` gem (a Jekyll dependency). On this
Mac the Command Line Tools install is missing its C++ headers, so a plain
`bundle install` fails to compile it. The proper fix is to reinstall the CLT:

```bash
sudo rm -rf /Library/Developer/CommandLineTools
xcode-select --install
```

Until then, this one-time workaround compiles it against the SDK's libc++:

```bash
CPLUS_INCLUDE_PATH="$(xcrun --show-sdk-path)/usr/include/c++/v1" \
  MAKEFLAGS='CXX=clang++' bundle install
```

(Only needed for `bundle install`; `jekyll serve`/`build` need no special flags.)

## Writing a post

Add a Markdown file to `_posts/` named `YYYY-MM-DD-title-slug.markdown` with front matter:

```yaml
---
layout: post
title: "Your Title"
tags: code java      # space-separated, no commas
---
```

The URL is `/blog/:year/:month/:day/:title/` (do not change the `permalink` in
`_config.yml` — it preserves 15 years of existing links).

If a post introduces a **new tag**, regenerate the tag pages and commit them:

```bash
python3 tag_generator.py     # rewrites tag/*.md (read by _layouts/tagpage.html)
```

## Deployment

Deploys run via GitHub Actions (`.github/workflows/pages.yml`): push to `source`
builds with Jekyll 4 and publishes to Pages.

> **One-time cutover:** the repo currently still uses the *legacy* Pages branch build.
> To switch to the Actions build, go to **Settings → Pages → Build and deployment →
> Source** and choose **GitHub Actions**. This is reversible (switch back to
> "Deploy from a branch" → `source`).

## Comments

Comments use Disqus by default. To switch to [giscus](https://giscus.app) (GitHub
Discussions): enable Discussions on the repo, install the giscus GitHub App, then fill
in the four `giscus:` IDs in `_config.yml`. Posts switch to giscus automatically once
those are set.

## Analytics

Set a GA4 Measurement ID (`G-XXXXXXXXXX`) as `ga_analytics:` in `_config.yml` to enable
Google Analytics (loads in production builds only). Left blank = no analytics.
