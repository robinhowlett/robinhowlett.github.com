---
layout: post
title: "Supporting Multi-Step Commands with Spring Shell"
date: 2015-03-19 15:44:25 -0600
comments: true
tags: [code, spring-shell]
---

Out of the box, [Spring Shell](http://docs.spring.io/spring-shell/docs/current/reference/htmlsingle/) supports printing command results to the terminal in a fairly basic way.

Spring Shell also provides the [`ExecutionProcessor`](http://docs.spring.io/spring-shell/docs/current/api/org/springframework/shell/core/ExecutionProcessor.html) interface, allowing a "command provider to be called in a generic fashion just before, and right after, executing a command".

The interface defines three lifecycle events that can be intercepted:

* before a command has been invoked
* after an invocation has been returned
* after an exception was thrown

I was interested in hooking into the `afterReturningInvocation` to provide "step logic" - potentially allowing user or system input to execute additional logic based on the result of the initial command result (and/or each step result) e.g. paging backwards or forwards on the command line through lists of data.

I was able to achieve this and opened [a JIRA ticket](https://jira.spring.io/browse/SHL-174) and the following pull request on Spring Shell's GitHub repo: [SHL-174: Multi-Step Commands #67](https://github.com/spring-projects/spring-shell/pull/67)

<!-- more -->

When writing command execution results to the terminal, Spring Shell's `AbstractShell` examines the instance being returned by the command and logs at `INFO` level the `toString()` output of the result object. If the result object is an instance of `Iterable`, it iterates over the collection and logs the `toString()` of each entry:

``` java AbstractShell.java
	protected void handleExecutionResult(Object result) {
		if (result instanceof Iterable<?>) {
			for (Object o : (Iterable<?>) result) {
				logger.info(o.toString());
			}
		} else {
			logger.info(result.toString());
		}
	}
```

When planning out my solution, I came up with the following back-of-the-napkin outline:

* a new custom annotation would be created and would be put on the command method. The `ParseResult invocationContext` instance passed into the processor methods could then be checked to see if the method being invoked had that annotation present, denoting a multi-step command.

* an abstract implementation of `ExecutionProcessor` would override the `afterReturningInvocation` method and detect if a multi-step command had been invoked. Command classes requiring multi-step logic would extend this class.

* the step logic would be configurable in that it could:
	* determine if there were more steps to execute, 
	* configure each step in preparation of execution, 
	* execute the step, and 
	* handle each step execution's result (e.g. logging to the shell), if any.

* the solution should also ensure that the command's original/final result was handled correctly.

<p />
---
**`@CliStepIndicator`**

I created a new annotation that denotes a `@CliCommand`-annotated method supports multi-step processing:

``` java CliStepIndicator.java
@Inherited
@Documented
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface CliStepIndicator {

}
```


**`AbstractStepExecutionProcessor.java`**

I created a new abstract class implementing `ExecutionProcessor`. The `afterReturningInvocation` method is overridden with the following logic:

* checks if this invocation is on a multi-step command
* the initial result from the command is handled and this is fact is stored on the shell
* while there are more steps
	* configure the next step
	* execute the next step in the workflow
	* handle the step execution result

{% gist robinhowlett/8e84da9f72600736d4f0 AbstractStepExecutionProcessor.java %}

## Example

`StepCommand.java` is an example command class with a multi-step command (`step-test`) method annotated with `@CliStepIndicator`. 

Each step increments a `int` variable (see `configureStep`), up to 3 times (see `hasMoreSteps`). Each step execution logs that it is executing (see `executeStep`), and step results are handled by printing the current `int` variable value (see `handleStepExecutionResult`). 

{% gist robinhowlett/8e84da9f72600736d4f0 StepCommand.java %}

The following integration test executes both the `step-test` multi-step command (to increment the `int` variable 3 times) and the `step-check` comand (to confirm the incrementation took place).

{% gist robinhowlett/8e84da9f72600736d4f0 StepCommandsTest.java %}

The test passes and prints the following output:

![Test Result](https://dl.dropboxusercontent.com/s/zy1rx79g8ugpad7/Screenshot%202015-03-19%2022.22.00.png)

I'll be posting shortly about how I used this feature in a recent CLI project to navigate API pagination, run simulations, diff audit log entries etc.