---
layout: post
title: "Solved: When the Maven Deploy Plugin silently fails to deploy"
tags: [code, maven, snaplogic]
---

At SnapLogic, we recently noticed that a particular build job that was responsible for deploying build artifacts to a Nexus repository via Maven had suddenly stopped, well, deploying. What was odd was that no error of any kind was being communicated, even in DEBUG mode. 

Examining the history of the repository, what had changed was the addition of a new module ("slbugs") to the existing multi-module Maven build. This module's reposibility was to run some code health checks using Google's [error-prone](https://github.com/google/error-prone) static analysis tool to catch some programming mistakes that our developers occassionally made that had a negative effect at runtime.

What was different about this module versus the others was that it did not use the root POM as a parent (as it was sufficiently different from the other more product-focused modules). The other modules were also configured to use the [`deployAtEnd`](https://maven.apache.org/plugins/maven-deploy-plugin/deploy-mojo.html#deployAtEnd) parameter of the parent's [`maven-deploy-plugin`](https://maven.apache.org/plugins/maven-deploy-plugin) plugin configuration.

The problem was that each of the product modules would log that they would be deployed at the end of the build, but after the last module ran its `deploy` phase, nothing would happen - no uploading of artifacts would be attempted, no warnings or debug messages logged to explain the inaction, and the build would just end with a SUCCESS status.

The solution turned out to be related to the wonderful world of Maven classloaders.

<!-- more -->

When the problem was reported and some obvious things had been tried (changing plugin versions etc.), I started to look into it. The first thing I did was create a standalone test that mirrored the basic structure of the multi-module project and chose what I deemed to be the pertinent configurations from the production POMs.

It looked like this:

![multi-module project layout](/assets/images/posts/2019/multi-module-layout.png)

Quite standard as you can see. `pom-root` defines the modules (`module-one` and `module-two`), where `module-one` does not use `pom-root` as its parent but `module-two` does. All dependency and plugin versions are identical, but `pom-root` (and therefore `module-two` by inheritence) uses the `deployAtEnd` configuration for the `maven-deploy-plugin`. For running the `deploy` phase, I setup a local empty temporary repository via the `distributionManagement` definition.

So, I ran `mvn clean deploy` and expected to see the problem reproduced:

```
> mvn clean deploy
[MVNVM] Using maven: 3.5.2
[INFO] Scanning for projects...
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Build Order:
[INFO] 
[INFO] module-one
[INFO] pom-root
[INFO] module-two
[INFO] 
[INFO] ------------------------------------------------------------------------
[INFO] Building module-one 1.0-SNAPSHOT
[INFO] ------------------------------------------------------------------------
[INFO] 
[INFO] --- maven-clean-plugin:2.5:clean (default-clean) @ module-one ---
[INFO] Deleting /Users/rhowlett/dev/tmp/pom-root/module-one/target
[INFO] 
[INFO] --- maven-resources-plugin:2.6:resources (default-resources) @ module-one ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] skip non existing resourceDirectory /Users/rhowlett/dev/tmp/pom-root/module-one/src/main/resources
[INFO] 
[INFO] --- maven-compiler-plugin:3.1:compile (default-compile) @ module-one ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 1 source file to /Users/rhowlett/dev/tmp/pom-root/module-one/target/classes
[INFO] 
[INFO] --- maven-resources-plugin:2.6:testResources (default-testResources) @ module-one ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] skip non existing resourceDirectory /Users/rhowlett/dev/tmp/pom-root/module-one/src/test/resources
[INFO] 
[INFO] --- maven-compiler-plugin:3.1:testCompile (default-testCompile) @ module-one ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 1 source file to /Users/rhowlett/dev/tmp/pom-root/module-one/target/test-classes
[INFO] 
[INFO] --- maven-surefire-plugin:2.12.4:test (default-test) @ module-one ---
[INFO] Surefire report directory: /Users/rhowlett/dev/tmp/pom-root/module-one/target/surefire-reports

-------------------------------------------------------
 T E S T S
-------------------------------------------------------
Running com.snaplogic.AppTest
Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.048 sec

Results :

Tests run: 1, Failures: 0, Errors: 0, Skipped: 0

[INFO] 
[INFO] --- maven-jar-plugin:2.4:jar (default-jar) @ module-one ---
[INFO] Building jar: /Users/rhowlett/dev/tmp/pom-root/module-one/target/module-one-1.0-SNAPSHOT.jar
[INFO] 
[INFO] --- maven-install-plugin:2.4:install (default-install) @ module-one ---
[INFO] Installing /Users/rhowlett/dev/tmp/pom-root/module-one/target/module-one-1.0-SNAPSHOT.jar to /Users/rhowlett/.m2/repository/com/snaplogic/module-one/1.0-SNAPSHOT/module-one-1.0-SNAPSHOT.jar
[INFO] Installing /Users/rhowlett/dev/tmp/pom-root/module-one/pom.xml to /Users/rhowlett/.m2/repository/com/snaplogic/module-one/1.0-SNAPSHOT/module-one-1.0-SNAPSHOT.pom
[INFO] 
[INFO] --- maven-deploy-plugin:2.8.2:deploy (default-deploy) @ module-one ---
Downloading from dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-one/1.0-SNAPSHOT/maven-metadata.xml
Uploading to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-one/1.0-SNAPSHOT/module-one-1.0-20190515.171609-1.jar
Uploaded to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-one/1.0-SNAPSHOT/module-one-1.0-20190515.171609-1.jar (2.4 kB at 237 kB/s)
Uploading to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-one/1.0-SNAPSHOT/module-one-1.0-20190515.171609-1.pom
Uploaded to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-one/1.0-SNAPSHOT/module-one-1.0-20190515.171609-1.pom (1.4 kB at 702 kB/s)
Downloading from dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-one/maven-metadata.xml
Uploading to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-one/1.0-SNAPSHOT/maven-metadata.xml
Uploaded to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-one/1.0-SNAPSHOT/maven-metadata.xml (767 B at 192 kB/s)
Uploading to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-one/maven-metadata.xml
Uploaded to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-one/maven-metadata.xml (281 B at 94 kB/s)
[INFO] 
[INFO] ------------------------------------------------------------------------
[INFO] Building pom-root 1.0-SNAPSHOT
[INFO] ------------------------------------------------------------------------
[INFO] 
[INFO] --- maven-clean-plugin:2.5:clean (default-clean) @ pom-root ---
[INFO] 
[INFO] --- maven-install-plugin:2.4:install (default-install) @ pom-root ---
[INFO] Installing /Users/rhowlett/dev/tmp/pom-root/pom.xml to /Users/rhowlett/.m2/repository/com/snaplogic/pom-root/1.0-SNAPSHOT/pom-root-1.0-SNAPSHOT.pom
[INFO] 
[INFO] --- maven-deploy-plugin:2.8.2:deploy (default-deploy) @ pom-root ---
[INFO] Deploying com.snaplogic:pom-root:1.0-SNAPSHOT at end
[INFO] 
[INFO] ------------------------------------------------------------------------
[INFO] Building module-two 1.0-SNAPSHOT
[INFO] ------------------------------------------------------------------------
[INFO] 
[INFO] --- maven-clean-plugin:2.5:clean (default-clean) @ module-two ---
[INFO] Deleting /Users/rhowlett/dev/tmp/pom-root/module-two/target
[INFO] 
[INFO] --- maven-resources-plugin:2.6:resources (default-resources) @ module-two ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] skip non existing resourceDirectory /Users/rhowlett/dev/tmp/pom-root/module-two/src/main/resources
[INFO] 
[INFO] --- maven-compiler-plugin:3.1:compile (default-compile) @ module-two ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 1 source file to /Users/rhowlett/dev/tmp/pom-root/module-two/target/classes
[INFO] 
[INFO] --- maven-resources-plugin:2.6:testResources (default-testResources) @ module-two ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] skip non existing resourceDirectory /Users/rhowlett/dev/tmp/pom-root/module-two/src/test/resources
[INFO] 
[INFO] --- maven-compiler-plugin:3.1:testCompile (default-testCompile) @ module-two ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 1 source file to /Users/rhowlett/dev/tmp/pom-root/module-two/target/test-classes
[INFO] 
[INFO] --- maven-surefire-plugin:2.12.4:test (default-test) @ module-two ---
[INFO] Surefire report directory: /Users/rhowlett/dev/tmp/pom-root/module-two/target/surefire-reports

-------------------------------------------------------
 T E S T S
-------------------------------------------------------
Running com.snaplogic.AppTest
Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.043 sec

Results :

Tests run: 1, Failures: 0, Errors: 0, Skipped: 0

[INFO] 
[INFO] --- maven-jar-plugin:2.4:jar (default-jar) @ module-two ---
[INFO] Building jar: /Users/rhowlett/dev/tmp/pom-root/module-two/target/module-two-1.0-SNAPSHOT.jar
[INFO] 
[INFO] --- maven-install-plugin:2.4:install (default-install) @ module-two ---
[INFO] Installing /Users/rhowlett/dev/tmp/pom-root/module-two/target/module-two-1.0-SNAPSHOT.jar to /Users/rhowlett/.m2/repository/com/snaplogic/module-two/1.0-SNAPSHOT/module-two-1.0-SNAPSHOT.jar
[INFO] Installing /Users/rhowlett/dev/tmp/pom-root/module-two/pom.xml to /Users/rhowlett/.m2/repository/com/snaplogic/module-two/1.0-SNAPSHOT/module-two-1.0-SNAPSHOT.pom
[INFO] 
[INFO] --- maven-deploy-plugin:2.8.2:deploy (default-deploy) @ module-two ---
Downloading from dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/pom-root/1.0-SNAPSHOT/maven-metadata.xml
Uploading to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/pom-root/1.0-SNAPSHOT/pom-root-1.0-20190515.171609-1.pom
Uploaded to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/pom-root/1.0-SNAPSHOT/pom-root-1.0-20190515.171609-1.pom (1.8 kB at 602 kB/s)
Downloading from dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/pom-root/maven-metadata.xml
Uploading to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/pom-root/1.0-SNAPSHOT/maven-metadata.xml
Uploaded to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/pom-root/1.0-SNAPSHOT/maven-metadata.xml (594 B at 119 kB/s)
Uploading to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/pom-root/maven-metadata.xml
Uploaded to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/pom-root/maven-metadata.xml (279 B at 70 kB/s)
Downloading from dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-two/1.0-SNAPSHOT/maven-metadata.xml
Uploading to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-two/1.0-SNAPSHOT/module-two-1.0-20190515.171610-1.jar
Uploaded to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-two/1.0-SNAPSHOT/module-two-1.0-20190515.171610-1.jar (2.1 kB at 710 kB/s)
Uploading to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-two/1.0-SNAPSHOT/module-two-1.0-20190515.171610-1.pom
Uploaded to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-two/1.0-SNAPSHOT/module-two-1.0-20190515.171610-1.pom (533 B at 178 kB/s)
Downloading from dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-two/maven-metadata.xml
Uploading to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-two/1.0-SNAPSHOT/maven-metadata.xml
Uploaded to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-two/1.0-SNAPSHOT/maven-metadata.xml (767 B at 256 kB/s)
Uploading to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-two/maven-metadata.xml
Uploaded to dev: file:///Users/rhowlett/.m2/temp-repository/com/snaplogic/module-two/maven-metadata.xml (281 B at 94 kB/s)
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO] 
[INFO] module-one ......................................... SUCCESS [  2.970 s]
[INFO] pom-root ........................................... SUCCESS [  0.131 s]
[INFO] module-two ......................................... SUCCESS [  0.652 s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 3.905 s
[INFO] Finished at: 2019-05-15T11:16:10-06:00
[INFO] Final Memory: 19M/309M
[INFO] ------------------------------------------------------------------------
```

Odd. The deployment happened perfectly. Then why wasn't it happening with the production build?

I decided to debug. I added [the source for version 2.8.2](https://github.com/apache/maven-deploy-plugin/releases/tag/maven-deploy-plugin-2.8.2) of the `maven-deploy-plugin` to my IDE and ran the same command except this time with `mvnDebug` and [a Remote Debug configuration setup](https://stackoverflow.com/a/14853683/277133). I put a breakpoint [in the `execute()` method of the `DeployMojo` class](https://github.com/apache/maven-deploy-plugin/blob/maven-deploy-plugin-2.8.2/src/main/java/org/apache/maven/plugin/deploy/DeployMojo.java#L152) and hoped to see what was causing the deployment not to be executed:

```java
/**
 * When building with multiple threads, reaching the last project doesn't have to mean that all projects are ready
 * to be deployed
 */
private static final AtomicInteger readyProjectsCounter = new AtomicInteger();
    
...

public void execute()
        throws MojoExecutionException, MojoFailureException {
    boolean addedDeployRequest = false;
    if (skip) {
        getLog().info("Skipping artifact deployment");
    } else {
        failIfOffline();

        DeployRequest currentExecutionDeployRequest =
                new DeployRequest().setProject(project).setUpdateReleaseInfo(isUpdateReleaseInfo()).setRetryFailedDeploymentCount(getRetryFailedDeploymentCount()).setAltReleaseDeploymentRepository(altReleaseDeploymentRepository).setAltSnapshotDeploymentRepository(altSnapshotDeploymentRepository).setAltDeploymentRepository(altDeploymentRepository);

        if (!deployAtEnd) {
            deployProject(currentExecutionDeployRequest);
        } else {
            deployRequests.add(currentExecutionDeployRequest);
            addedDeployRequest = true;
        }
    }

    boolean projectsReady = readyProjectsCounter.incrementAndGet() == reactorProjects.size();
    if (projectsReady) {
        synchronized (deployRequests) {
            while (!deployRequests.isEmpty()) {
                deployProject(deployRequests.remove(0));
            }
        }
    } else if (addedDeployRequest) {
        getLog().info("Deploying " + project.getGroupId() + ":" + project.getArtifactId() + ":"
                + project.getVersion() + " at end");
    }
}
```

It looked clear that the `projectsReady` boolean would be key. Its value was determined by the equality of a static `AtomicInteger` called `readyProjectsCounter` and the size of the `reactorProjects` collection. The only way for the build to log that it was going to deploy at the end and then not deploy the final module, would be if the `readyProjectsCounter` and `reactorProjects` size had some kind of off-by-X error. Indeed, the debugger showed that, for the production build, `readyProjectsCounter` was one less than the collection size. But what would cause that?

I dived into the debug logs of the production build to try to see if I could identify anything of note. After trying quite a few different things, something caught my eye.

When "slbugs" was running its `deploy` phase with the `maven-deploy-plugin`, it logged:

```
[DEBUG] Created new class realm plugin>org.apache.maven.plugins:maven-deploy-plugin:2.8.2
[DEBUG] Importing foreign packages into class realm plugin>org.apache.maven.plugins:maven-deploy-plugin:2.8.2
[DEBUG]   Imported:  < maven.api
[DEBUG] Populating class realm plugin>org.apache.maven.plugins:maven-deploy-plugin:2.8.2
[DEBUG]   Included: org.apache.maven.plugins:maven-deploy-plugin:jar:2.8.2
[DEBUG]   Included: backport-util-concurrent:backport-util-concurrent:jar:3.1
[DEBUG]   Included: org.codehaus.plexus:plexus-interpolation:jar:1.11
[DEBUG]   Included: junit:junit:jar:3.8.1
[DEBUG]   Included: org.codehaus.plexus:plexus-utils:jar:3.0.15
[DEBUG] Configuring mojo org.apache.maven.plugins:maven-deploy-plugin:2.8.2:deploy from plugin realm ClassRealm[plugin>org.apache.maven.plugins:maven-deploy-plugin:2.8.2, parent: sun.misc.Launcher$AppClassLoader@3d4eac69]
```

When the parent POM was running, this was logged:

```
[DEBUG] Created new class realm plugin>org.apache.maven.plugins:maven-deploy-plugin:2.8.2-932771130
[DEBUG] Importing foreign packages into class realm plugin>org.apache.maven.plugins:maven-deploy-plugin:2.8.2-932771130
[DEBUG]   Imported:  < maven.api
[DEBUG] Populating class realm plugin>org.apache.maven.plugins:maven-deploy-plugin:2.8.2-932771130
[DEBUG]   Included: org.apache.maven.plugins:maven-deploy-plugin:jar:2.8.2
[DEBUG]   Included: backport-util-concurrent:backport-util-concurrent:jar:3.1
[DEBUG]   Included: org.codehaus.plexus:plexus-interpolation:jar:1.11
[DEBUG]   Included: junit:junit:jar:3.8.1
[DEBUG]   Included: org.codehaus.plexus:plexus-utils:jar:3.0.15
[DEBUG] Configuring mojo org.apache.maven.plugins:maven-deploy-plugin:2.8.2:deploy from plugin realm ClassRealm[plugin>org.apache.maven.plugins:maven-deploy-plugin:2.8.2-932771130, parent: sun.misc.Launcher$AppClassLoader@3d4eac69]
```

This `-932771130` suffix was strange. When I turned on debug logging for `pom-root` by running `mvn -X clean deploy`, I saw no such recreation of a "class realm". In fact, every plugin was "initialized" once.

But in the production build, many plugins (`maven-install-plugin`, `maven-resources-plugin` etc.), all seem to have been "recreated" when the build moved on to the root pom (after the initial "slbugs" module had been deployed). What was triggering that? I started to consume some articles from the web, including:

* [The official "Guide to Maven Classloading"](https://maven.apache.org/guides/mini/guide-maven-classloading.html)
* [Semsur IT's "Java class loader and Maven plugin"](http://blog.semsur-it.com/2011/11/java-class-loader-and-maven-plugin.html)
* [takari's "Maven classloading"](http://takari.io/book/91-maven-classloading.html)
* [chalda's "Maven plugin and fight with classloading"](http://blog.chalda.cz/2018/02/17/Maven-plugin-and-fight-with-classloading.html#_class_loading_troubles)

I'll admit that I was a bit puzzled. Neither build had any custom extensions defined, but I started focusing on whether there was anything non-standard defined in the production build POM, looking at things like `<properties>`, `<build>`, or anything around `<plugins>`.

Sure enough, I noticed the following:

```
<pluginRepositories>
    <pluginRepository>
        <id>apache.snapshots</id>
        <name>Apache Snapshots</name>
        <url>http://repository.apache.org/content/groups/snapshots-group/</url>
        <releases>
            <enabled>true</enabled>
        </releases>
        <snapshots>
            <enabled>true</enabled>
        </snapshots>
    </pluginRepository>
</pluginRepositories>
```

This was added many years ago to the build, probably to avail of some SNAPSHOT-versioned plugin. So I decided to replicate this in the standalone test's `pom-root`'s pom.xml by adding the following:

```xml
<pluginRepositories>
    <pluginRepository>
        <id>temp.repo</id>
        <name>Temp Repo</name>
        <url>file://${user.home}/.m2/temp-repository</url>
    </pluginRepository>
</pluginRepositories>
```

I re-ran the build and I finally I had reproduced the problem (the non-deployment of `pom-root` and `module-two`):

```
...
[INFO] --- maven-deploy-plugin:2.8.2:deploy (default-deploy) @ module-two ---
[INFO] Deploying com.snaplogic:module-two:1.0-SNAPSHOT at end
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO] 
[INFO] module-one ......................................... SUCCESS [  3.477 s]
[INFO] pom-root ........................................... SUCCESS [  0.228 s]
[INFO] module-two ......................................... SUCCESS [  1.446 s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 5.308 s
[INFO] Finished at: 2019-05-15T12:10:55-06:00
[INFO] Final Memory: 24M/437M
[INFO] ------------------------------------------------------------------------
```

Similarly, the debug log shows the two initializations of the `maven-deploy-plugin`:

```
[DEBUG] Created new class realm plugin>org.apache.maven.plugins:maven-deploy-plugin:2.8.2
...
[DEBUG] Created new class realm plugin>org.apache.maven.plugins:maven-deploy-plugin:2.8.2-1119294797
```

So, the addition of the new module ("slbugs") in our production build (that didn't define a `<pluginRespositories>` and didn't use the root POM as its parent), created a new context that resulted in new classloaders being used when the root POM (and its child modules) executed. This caused the `maven-deploy-plugin`'s `readyProjectsCounter` static `AtomicInteger` to start once again from `0` (instead of `1` as it should have been incremented when the first module was deployed), resulting in the off-by-one error when compared to the count of the reactor module (which wasn't static), meaning the parent and child modules never meeting the condition that would trigger the deployment.

As for resolving this, I found that if both `pom-root` and `module-one` "matched" when it came to defining the `<pluginRepositories>`, then the deployment would work; meaning:

* if neither defined it, the deployment worked
* if both defined it, the deployment worked (however the `pluginRepository`'s `id` and `url`s must be the same)

The standalone project I created to demonstrate this is available on GitHub here: https://github.com/robinhowlett/maven-deploy-plugin-gotcha

[The `master` branch](https://github.com/robinhowlett/maven-deploy-plugin-gotcha/tree/master) represents the non-working deployment, and [the `fix` branch](https://github.com/robinhowlett/maven-deploy-plugin-gotcha/tree/fix) represents the working example (with the `<pluginRepositories>` [removed from the root POM](https://github.com/robinhowlett/maven-deploy-plugin-gotcha/compare/fix?expand=1#diff-600376dffeb79835ede4a0b285078036)).