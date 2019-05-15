---
layout: post
title: "Custom Jackson Polymorphic Deserialization without Type Metadata"
date: 2015-03-19 11:28:24 -0700
comments: true
tags: [code, jackson]
---

At [SportsLabs](http://sportslabs.com) we regularly encounter proprietary, non-standard APIs and formats. Our job is to integrate with these APIs, normalize them, and distribute the data in web- and mobile-friendly web services.

One of the scenarios we often encounter is a provider supplying multiple resource JSON-based APIs that share a lot of the same data in their responses, but without any particular field dedicated to identying the type of the resource e.g.

``` json
{
...
	"common": "a common field within multiple resource responses",
	"one": "one is a field only within this response type"
...
}
```

and 

``` json
{
...
	"common": "a common field within multiple resource responses",
	"two": "two is a field only within this response type"
...
}
```

Instead of mapping 1-to-1 with these APIs, we often try to follow [DRY](http://en.wikipedia.org/wiki/Don%27t_repeat_yourself) principles and model them as implementations of a common polymorphic abstraction.

When using [Jackson for polmorphic deserialization](http://wiki.fasterxml.com/JacksonPolymorphicDeserialization) and not being in control of the API response data, the lack of any kind of `type` identifier requires a different solution.

One of the ways we've addressed this problem is to identify fields and properties that are unique to a particular resource API's response. 

We then add this field to a registry of known unique-property-to-type mappings and then, during deserialization, lookup the response's field names to see if any of them are stored within the registry.

<!-- more -->

Planning out the solution, there were a couple of things I wanted to incorporate:

* the deserializer should be initialized with the abstract class representing the shared response data
* a `register(String uniqueProperty, Class<? extends T> clazz)` method will add the field-name-to-concrete-class mapping to the registry
* the custom deserializer would be added to a Jackson `SimpleModule` which in turn would be registered with the `ObjectMapper`.

{% gist robinhowlett/ce45e575197060b8392d UniquePropertyPolymorphicDeserializer.java %}

The `deserialize` method reads each of the fields in the response and looks up the registry to see if it is present. If it finds a match, the `mapper.treeToValue` method is invoked with the response object and the mapped class returned by the registry. If no match is found an exception is thrown.

For the unit test, I created an inner static abstract class `AbstractTestObject` (containing shared data) with two concrete implementations (`TestObjectOne` and `TestObjectTwo`) that each contain a property unique to that type. 

The test also contains a inner class `TestObjectDeserializer` that extends `UniquePropertyPolymorphicDeserializer`. The test's `setUp` method:

* initializes the custom deserializer,
* registers the unique-field-name-to-type mappings, and
* adds the custom deserializer to a new `SimpleModule` which is registered with the `ObjectMapper` in turn.

{% gist robinhowlett/ce45e575197060b8392d UniquePropertyPolymorphicDeserializerTest.java %}

If others have solved this problem differently, I'd love to hear about it!