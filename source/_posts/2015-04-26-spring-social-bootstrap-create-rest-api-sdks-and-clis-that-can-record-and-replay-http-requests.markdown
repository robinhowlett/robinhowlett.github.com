---
layout: post
title: "Spring Social Bootstrap: Create REST API SDKs and CLIs that can Record and Replay HTTP requests"
date: 2015-04-26 16:50:33 -0600
comments: true
categories: 
---

I joined [SportsLabs](http://sportslabs.com) (then still under the [Silver Chalice](http://www.silverchalice.com/) brand) way back [in 2011](https://www.linkedin.com/in/robinhowlett) as one of its earliest employees and the first engineer. 

We started work on envisioning and building the [Advanced Media Platform](http://sportslabs.com/platform/) - a system to ingest, process, transform, distribute, and stream sports, news, social, and media content to create market leading mobile, web, and social products for clients such as [Samsung](http://milk.samsung.com/), the [University of Notre Dame](http://watchnd.tv/#!/), the [ACC](http://www.theacc.com/), the [College Football Playoff](http://www.collegefootballplayoff.com/), [IMG College](https://play.google.com/store/apps/developer?id=SportsLabs&hl=en), the [Mountain West](http://www.themw.com/) and [Campus Insiders](http://campusinsiders.com/), among others.

Since then, SportsLabs has consumed data from dozens of sources including [STATS LLC](http://www.stats.com/), [Twitter](https://twitter.com/), and [Ooyala](http://www.ooyala.com/), but also from proprietary systems that were never foreseen as integration points. 

Data providers' APIs use combinations of JSON, XML and/or CSV. Some are spec-compliant, others are not. Some rely heavily on query parameters, while others favor HTTP headers. Some API providers use [OAuth 2.0](http://oauth.net/2/) plus API rate limits, while others have rolled their own security solutions. Some integrations were with partners willing to work with us on evolving their web services. Others were with competitors who were not motivated to make things easy.

This plethora of ways to configure, consume, learn from, and integrate with APIs led us to create [Spring Social Bootstrap](https://github.com/robinhowlett/spring-social-bootstrap), a family of projects intended to aid creating and managing API clients for many of the above scenarios.

Spring Social Bootstrap is comprised of the following:

* **[Spring Social Bootstrap SDK](https://github.com/robinhowlett/spring-social-bootstrap/tree/master/spring-social-bootstrap-sdk)**: a [Spring Social](http://projects.spring.io/spring-social)-based framework for rapidly and consistently developing API clients
* **[Bootstrap Shell](https://github.com/robinhowlett/spring-social-bootstrap/tree/master/bootstrap-shell)**: a [Spring Shell](http://docs.spring.io/spring-shell/docs/current/reference/htmlsingle/)-based framework to aid creating command-line interface (CLI) applications for API clients built on Spring Social Bootstrap SDK
* **[HAR Mar Interceptor](https://github.com/robinhowlett/spring-social-bootstrap/tree/master/har-mar-interceptor)**: allows capturing HTTP request/response exchanges, persisting them in a [HAR](http://www.softwareishard.com/blog/har-12-spec/) or [ALF](https://github.com/Mashape/api-log-format)-compatible format, and re-executing those requests at a later time.

<!-- more -->

<p>
---

<p align="center">![Spring Social Bootstrap SDK](http://i.imgur.com/asX8yGM.jpg)

**Spring Social Bootstrap SDK** is a simple [Spring Social](http://projects.spring.io/spring-social)-based framework for rapidly and consistently developing API clients.

It combines the strengths of Spring Social, such as [native support for OAuth-based service providers](http://docs.spring.io/spring-social/docs/current/reference/htmlsingle/#connectFramework) (including support for OAuth 1 and OAuth 2), with consistent and well-defined extension points for new API clients.

Spring Social, despite its name, has no requirement on integrations being only with social networks. In truth, its primarily a set of interfaces for predictable implementations of API clients - which is our goal too.

Spring Social Bootstrap SDK provides CRUD and query capabilities out-of-the-box e.g.

```java
testApi.testOperations().create(testBaseApiResource);
testApi.testOperations().get(testBaseApiResource.getId());
testApi.testOperations().update(testBaseApiResource);
testApi.testOperations().delete(testBaseApiResource.getId());
testApi.testOperations().query();
```

as well as guidelines on how to create developer-friendly features like query builders e.g.

```java
testApi.testOperations().qb().withPaging(1, 25, "name", Sort.Direction.ASC).query();
```

I've advise taking a look at the [Spring Social Bootstrap SDK README](https://github.com/robinhowlett/spring-social-bootstrap/blob/master/spring-social-bootstrap-sdk/README.md) to learn more on how to create API clients based on Spring Social Bootstrap SDK.

<p>
---

<p align="center">![Bootstrap Shell](http://i.imgur.com/PypWRjx.png)

**Bootstrap Shell** is a [Spring Shell](http://docs.spring.io/spring-shell/docs/current/reference/htmlsingle/)-based framework to aid creating command-line interface (CLI) applications for API clients built on [Spring Social Bootstrap SDK](https://github.com/robinhowlett/spring-social-bootstrap/tree/master/spring-social-bootstrap-sdk).

When developing API clients, SportsLabs learned that is worth leveraging the clients in data monitoring, QA, testing, and simulation scenarios. As such, we created a small CLI framework to allow highly interactive command-line applications as well as taking advantage of the power of command line tools, such as [pipes](http://man7.org/linux/man-pages/man2/pipe.2.html), [`xargs`](http://unixhelp.ed.ac.uk/CGI/man-cgi?xargs), [`jq`](http://stedolan.github.io/jq/), and even opening the browser to online side-by-side diff tools like [mergely](http://www.mergely.com/editor?lhs=http://mockbin.com/bin/800a818b-5fb6-40d4-a342-75a1fb8599db/view&rhs=http://mockbin.com/bin/3c149e20-bc9c-4c68-8614-048e6023a108/view).

We also liked Spring Shell's Spring-based interactive shell, but the XML-only configuration, the `toString()`-based command outputs and lack of menu-style multi-step support required a fork of the project to add the following:

* [SHL-106: Java Configuration support](https://github.com/spring-projects/spring-shell/pull/66): Permits configuring a Spring Shell application using Java `@Configuration` classes instead of XML ([JIRA](https://jira.spring.io/browse/SHL-106))
* [SHL-174: Multi-Step Commands](https://github.com/spring-projects/spring-shell/pull/67): Permits commands annotated with `@CliStepIndicator` to perform additional logic during its execution, including accepting user input e.g. pagination instructions ([JIRA](https://jira.spring.io/browse/SHL-174))
* [SHL-175: Multiple Output Formats for Commands](https://github.com/spring-projects/spring-shell/pull/68): Permits command results to be printed to the console with different formats by using Spring Type Converters, denoted by `@CliPrinter` annotations on Command parameters ([JIRA](https://jira.spring.io/browse/SHL-175))

The result was a handy framework for developers and QA engineers to quickly start using our API clients in a variety of situations.

_e.g. [Mockbin CLI](https://github.com/robinhowlett/mockbin-cli): an Bootstrap Shell-based CLI application for [Mockbin](http://mockbin.com/) powered by [Spring Social Mockbin](https://github.com/robinhowlett/spring-social-mockbin)_
![CLI Example](http://i.imgur.com/8Eca4p3.gif)

Again, check out the [Bootstrap Shell README](https://github.com/robinhowlett/spring-social-bootstrap/blob/master/bootstrap-shell/README.md) for more information.

<p>
---

<p align="center">![HAR Mar Interceptor](http://i.imgur.com/oaqfyPi.png)

**HAR Mar Interceptor** allows capturing HTTP request/response exchanges, persisting them in a [HTTP Archive (HAR)](http://www.softwareishard.com/blog/har-12-spec/) or [API Log Format (ALF)](https://github.com/Mashape/api-log-format)-compatible format, and re-executing those requests at a later time.

Often one of the challenging things about creating clients for proprietary APIs is the lack of documentation or samples available to learn from. Also, some API providers can be very strict with rate limits and test API endpoints are rarely provided.

In Sports, this issue is complicated further by the time sensitive nature of the domain - events rarely last longer than a couple of hours and every so often rare scenarios like weather-related postponements, data-entry errors and [22 inning baseball games](http://www.ncaa.com/news/baseball/article/2014-06-01/tcu-wins-22-innings-second-longest-game-ncaa-tourney-history) create challenges for how well our products work for users.

Early on in SportsLabs' life, we created our own system for storing the request history of particular API endpoints, but I discovered the [HTTP Archive (HAR)](http://www.softwareishard.com/blog/har-12-spec/) spec, created by [@JanOdvarko](https://twitter.com/janodvarko), lead of the [Firebug](http://www.getfirebug.com/) project. 

If you are familar with Firebug you'll know you can see the requests the browser is making for a particular page and the time taken for each response to be received:

![Firebug](http://core0.staticworld.net/images/idge/imported/article/itw/2013/11/22/netpanel-100521990-orig.png)

[Mashape](https://www.mashape.com/) [API Log Format (ALF)](https://github.com/Mashape/api-log-format) is based on HAR and is particularly designed for API consumer use cases.

HAR Mar Interceptor ships with a customized Spring [`ClientHttpRequestInterceptor`](http://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/http/client/ClientHttpRequestInterceptor.html) for capturing HTTP request/response exchanges and storing them in ALF to a JDBC database:

![HAR Table](http://i.imgur.com/siNRX66.png)

The persisted data can be loaded into an `AlfHar` POJO and represented in JSON using [Jackson](http://wiki.fasterxml.com/JacksonHome). This JSON can even be stored in a `.har` file and loaded into HAR-compatible tools like [Charles Web Debugging Proxy](http://www.charlesproxy.com/).

It also provides `ReplayAlfHarTemplate` to replay entries in the HAR log at either real-time, fixed or immediate intervals.

This allows us to capture what our systems are requesting and/or responding under certain conditions, replay system inputs and/or outputs for debugging, plus design and tweak scenarios based on real data.

It also aids us when integrating with new data providers lacking documentation, as we can learn from the archive log and, for those who wish to limit testing efforts against their infrastructure, use services like Mashape's [Mockbin](http://mockbin.com/) to mock their endpoints with observed data - using [Spring Social Mockbin](https://github.com/robinhowlett/spring-social-mockbin), naturally.