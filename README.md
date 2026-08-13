# robinhowlett.com

Personal blog of Robin Howlett — built with [Jekyll](https://jekyllrb.com/) 4 on the
"Royce" theme, published to [robinhowlett.com](https://robinhowlett.com/) via GitHub
Pages (GitHub Actions build).

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

1. Create `_posts/YYYY-MM-DD-title-slug.markdown` with front matter:

   ```yaml
   ---
   layout: post
   title: "Your Title"
   tags: code java      # space-separated, NO commas
   ---
   ```

   The URL becomes `/blog/:year/:month/:day/:title/`. Don't change `permalink` in
   `_config.yml` — it preserves 15 years of existing links. (If you set an explicit
   `date:` with a time + offset, remember the build is UTC, so an evening time can roll
   the date — and the URL — to the next day.)

2. Write the body in Markdown. Put `<!-- more -->` where the home-page excerpt should
   stop. Store post images under `assets/images/posts/<year>/` and reference them
   root-absolute, e.g. `![alt](/assets/images/posts/2026/foo.png)`.

3. Preview locally: `bundle exec jekyll serve` → http://localhost:4000/

4. If the post introduces a **new tag**, regenerate the tag pages and commit them:

   ```bash
   python3 tag_generator.py     # rewrites tag/*.md (rendered by _layouts/tagpage.html)
   ```

5. Commit and push to `source`. GitHub Actions builds and deploys automatically
   (~1–2 min). Comments and analytics are already wired — nothing else to do.

## Deployment

Every push to `source` triggers `.github/workflows/pages.yml`, which builds with
Jekyll 4, runs an `html-proofer` link/image check, and publishes to GitHub Pages.
Watch runs under the repo's **Actions** tab.

**Rollback:** Settings → Pages → Build and deployment → Source → "Deploy from a branch"
→ `source` reverts to the old legacy build.

## Comments

Comments use [giscus](https://giscus.app), backed by this repo's GitHub Discussions
(configured under `giscus:` in `_config.yml`). A thread is created the first time
someone comments on a post. To fall back to Disqus, blank out the `giscus:` IDs
(the `disqus:` shortname is still in config).

## Analytics

Google Analytics 4 is configured via `ga_analytics:` in `_config.yml` and loads on
**production builds only** (local/dev builds send nothing). Blank it out to disable.
