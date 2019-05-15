---
layout: post
title: "Adding Java Config support to Spring Shell"
date: 2015-03-19 13:58:12 -0600
comments: true
tags: [code, java, spring, spring-shell]
---

Be it [DVCS workflows](https://github.com/nvie/gitflow), [JSON transformations](http://stedolan.github.io/jq/), or [blogging frameworks](http://octopress.org/), I always favor tools that allow me to use the terminal.

I've recently started using [Spring Shell](http://docs.spring.io/spring-shell/docs/current/reference/htmlsingle/) for rapidly experimenting with consuming data from a series of APIs I had created.

I have become allergic to XML configuration for Spring applications in recent times, so I was disappointed to see a lack of support for Java configuration within Spring Shell.

However, I did find a [JIRA issue tracking the feature request](https://jira.spring.io/browse/SHL-106). The ticket creator had even submitted a pull request with a potential solution. However, Spring Shell lead [Mark Pollack](https://twitter.com/markpollack) responded that the feature could be provided in a simpler manner and even provided guidance to the solution.

Implementing this solution seemed quite straightforward, so I gave it a go and it turned out well. 

I've submitted the following pull request to the Spring Shell GitHub repository: [SHL-106: Java Configuration support #66](https://github.com/spring-projects/spring-shell/pull/66)

<!-- more -->

The pull request detailed:

- Updated [Bootstrap.java](https://github.com/robinhowlett/spring-shell/commit/38562bebf3d7621d4ee9fff1e0f477664299f282#diff-aefe86f2ee6f28928f53e91587a79910) to accept basePackages String varargs and to include them in `ClassPathBeanDefinitionScanner` scan
- Updated [sample HelloWorld project](https://github.com/robinhowlett/spring-shell/commit/38562bebf3d7621d4ee9fff1e0f477664299f282#diff-c2b9b8f993e1d2ca3677a070dd126078) to demonstrate mixing XML and Java Configuration
- Updated docbook-reference-plugin dependency group ID and version (needed to get my gradle build working)

This was my first pull request submission for a Spring project (albeit still awaiting approval). I was very happy to "give a little back" finally!