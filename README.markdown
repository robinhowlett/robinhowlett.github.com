# The Boy Wonders

Robin Howlett's blog based on an (old) version of [Octopress](http://octopress.org), a [Jekyll](https://github.com/mojombo/jekyll)-based blog framework. It does the job for me.

## Blog Posts

```
rake new_post["Zombie Ninjas Attack: A survivor's retrospective"]`
# Creates source/_posts/2011-07-03-zombie-ninjas-attack-a-survivors-retrospective.markdown
```

The filename will determine your url. With the default permalink settings the url would be something like `http://site.com/blog/2011/07/03/zombie-ninjas-attack-a-survivors-retrospective/index.html`

### YAML

```
---
layout: post
title: "Zombie Ninjas Attack: A survivor's retrospective"
date: 2011-07-03 5:59
comments: true
external-url:
categories:
---
```

### Categories

```
# One category
categories: Sass
 
# Multiple categories example 1
categories: [CSS3, Sass, Media Queries]
 
# Multiple categories example 2
categories:
- CSS3
- Sass
- Media Queries
```

## Pages

```
rake new_page[super-awesome]
# creates /source/super-awesome/index.markdown
 
rake new_page[super-awesome/page.html]
# creates /source/super-awesome/page.html
```

The title is derived from the filename so you'll likely want to change that. This is very similar to the post yaml except it doesn't include categories, and you can toggle sharing and comments or remove the footer altogether. If you don't want to show a date on your page, just remove it from the yaml.

## Generate & Preview

```
rake generate   # Generates posts and pages into the public directory
rake watch      # Watches source/ and sass/ for changes and regenerates
rake preview    # Watches, and mounts a webserver at http://localhost:4000
rake deploy

git add .
git commit -m 'your message'
git push origin source
```

If you want to work on posts without publishing them, you can add a `published: false` to your post's YAML header. You can preview these posts with ``rake preview` on your local server, but they won't get published by rake generate.

## Octopress License
(The MIT License)

Copyright © 2009-2013 Brandon Mathis

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ‘Software’), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ‘AS IS’, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
