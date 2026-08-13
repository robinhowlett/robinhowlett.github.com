source "https://rubygems.org"

# Standalone Jekyll (no github-pages gem) so we can run a current Jekyll and
# build via GitHub Actions rather than the legacy Pages builder.
gem "jekyll", "~> 4.3"

# Local dev server (Ruby 3+ no longer bundles webrick).
gem "webrick", "~> 1.8"

group :jekyll_plugins do
  gem "jekyll-paginate"  # keeps /page:num/ pagination URLs identical to prod
  gem "jekyll-seo-tag"   # <head> SEO/canonical/OpenGraph tags
  gem "jekyll-gist"      # {% gist %} embeds used in a couple of posts
  gem "jekyll-sitemap"   # /sitemap.xml (additive; not present on the old site)
end

# Link/image checker used locally and in CI (see .github/workflows).
gem "html-proofer", "~> 5.0"

# Windows/JRuby lack the system tzinfo database; we pin the build TZ to UTC.
gem "tzinfo-data", platforms: [:windows, :jruby]

# Faster file watching on Windows during `jekyll serve`.
gem "wdm", "~> 0.1", platforms: [:windows]
