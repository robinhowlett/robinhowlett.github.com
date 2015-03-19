---
layout: post
title: "Building a Custom Jackson Deserializer"
date: 2015-01-01 21:35:31 -0700
comments: true
categories: java jackson
---

A partner recently provided a useful HTTP-based API for me at short notice. 

The API returned simple JSON representations of the current state of various events they had periodically ingested from our REST APIs.

A decision they made was to use `"yes"`/`"no"` values in the response, rather than booleans e.g.

``` json
{
...
	"exists": "yes",
	"has_ended": "no"
...
}
```

I had written a [Spring Social](http://projects.spring.io/spring-social/)-based API client to interact with their API but wanted to deserialize their API response representation into a POJO that followed Java convention.

[Jackson](http://wiki.fasterxml.com/JacksonHome) is a great Java library for processing JSON data format. It's quite straightforward to use it to solve a problem like the above with a custom [`JsonDeserializer`](http://fasterxml.github.io/jackson-databind/javadoc/2.4/com/fasterxml/jackson/databind/JsonDeserializer.html).

<!-- more -->

<p>
---

Planning out the solution, there were a couple of things I wanted to incorporate:

* the deserializer should be case-insensitive
* a `null` value in the JSON document should be treated as `false` (due to autoboxing considerations around Java's primitive (`boolean`) and Object-based `Boolean` representations)
* an exception should be thrown if something other than `"yes"` or `"no"` was provided

Sketching out the JUnit test class, I needed a static inner class to represent the POJO that Jackson would deserialize to, an [`ObjectMapper`](http://fasterxml.github.io/jackson-databind/javadoc/2.4/com/fasterxml/jackson/databind/ObjectMapper.html) to deserialize a sample JSON document, and test cases for the above conditions.

For the field that will use the custom deserializer, the [`@JsonDeserialize`](http://fasterxml.github.io/jackson-databind/javadoc/2.4/com/fasterxml/jackson/databind/annotation/JsonDeserialize.html) annotation is added, with the `using` parameter pointing at our implementation class.

{% gist robinhowlett/1ef8a82584e9ea36ed04 YesNoBooleanDeserializerTest.java %}

For the implementation, we must override the [`JsonDeserializer.deserialize(JsonParser jp, DeserializationContext ctxt)`](http://fasterxml.github.io/jackson-databind/javadoc/2.4/com/fasterxml/jackson/databind/JsonDeserializer.html#deserialize(com.fasterxml.jackson.core.JsonParser, com.fasterxml.jackson.databind.DeserializationContext\)) method. 

If Jackson has identified the field value token currently being deserialized as a String, it is case-insensitively checked for either a `"yes"` or `"no"` value, throwing a [`JsonMappingException`](http://fasterxml.github.io/jackson-databind/javadoc/2.4/com/fasterxml/jackson/databind/JsonMappingException.html) with an explaination through the [`DeserializationContext.weirdStringException(String value, Class<?> instClass, String msg)`](http://fasterxml.github.io/jackson-databind/javadoc/2.4/com/fasterxml/jackson/databind/DeserializationContext.html#weirdStringException(java.lang.String, java.lang.Class, java.lang.String\)) method if an unsupported String value is received instead.

As Java supports both the primitive `boolean` and the Object `Boolean`, and can autobox between them, `null` values will be interpreted as `false`. To do this, [`JsonDeserializer.getNullValue()`](http://fasterxml.github.io/jackson-databind/javadoc/2.4/com/fasterxml/jackson/databind/JsonDeserializer.html#getNullValue(\)) is overridden and returns `Boolean.FALSE`. Then within the `deserialize` method, the current token is checked if it is a `JsonToken.VALUE_NULL` and the `getNullValue()` method is called if it is.

Finally, an exception is thrown if the token is of any other type.

{% gist robinhowlett/1ef8a82584e9ea36ed04 YesNoBooleanDeserializer.java %}

