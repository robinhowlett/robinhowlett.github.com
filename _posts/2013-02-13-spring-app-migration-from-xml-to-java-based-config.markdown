---
layout: post
title: "Spring app migration: from XML to Java-based config"
date: 2013-02-13 10:46
comments: true
tags: [code, java, spring]
---
Our team recently built a Spring MVC 3.1 application for a web service API. We had used the traditional XML-based configuration but I wanted to see how easy would it be to migrate a Spring application from an XML-based to a Java annotation-based configuration.	

I referenced three great resources for this migration:

* [@baeldung](http://www.twitter.com/baeldung)'s excellent [Bootstrapping a web application with Spring 3.1 and Java based Configuration](http://www.baeldung.com/2011/10/20/bootstraping-a-web-application-with-spring-3-1-and-java-based-configuration-part-1/) series
* [@doughaber](http://www.twitter.com/doughaber)'s post, [Pagination with Spring MVC, Spring Data and Java Config](http://blog.fawnanddoug.com/2012/05/pagination-with-spring-mvc-spring-data.html), included some great "gotchas", especially around web tier configuration
* [@cbeam](http://www.twitter.com/cbeam) and [@rstoya05](http://www.twitter.com/rstoya05)'s presentation, [Configuration Enhancements in Spring 3.1](http://cbeams.github.com/spring-3.1-config), laid out in terrific detail how Spring configuration has evolved and how most XML configurations could be achieved through Java annotations

<!-- more -->

The `web.xml` defined the context configuration and dispatch servlet locations:

``` xml web.xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<web-app version="2.5" xmlns="http://java.sun.com/xml/ns/javaee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd">
	<context-param>
		<param-name>contextConfigLocation</param-name>
		<param-value>classpath:META-INF/spring/root-context.xml</param-value>
	</context-param>
	...
	<servlet>
		<servlet-name>spring-mvc-dispatcher</servlet-name>
		<servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
		<init-param>
			<param-name>contextConfigLocation</param-name>
			<param-value>classpath:META-INF/spring/servlet-context.xml</param-value>
		</init-param>
		<load-on-startup>1</load-on-startup>
	</servlet>
	<servlet-mapping>
		<servlet-name>spring-mvc-dispatcher</servlet-name>
		<url-pattern>/</url-pattern>
	</servlet-mapping>
</web-app>
```

`root-context.xml` was intended to define shared resources visible to all other web components, servlets etc and for cross-cutting concerns like security - for the moment though it was just an empty `<beans>` XML file.

`servlet-context.xml` was the `DispatcherServlet` and a wrapper around three other contexts; `persistence-context.xml` for Spring Data/JPA configuration, `bizniz-context.xml` for business/service configuration and `web-context.xml` for web service configuration:

``` xml servlet-context.xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.1.xsd">
	
	<import resource="classpath:META-INF/spring/persistence-context.xml" />
	<import resource="classpath:META-INF/spring/bizniz-context.xml" />
	<import resource="classpath:META-INF/spring/web-context.xml" />
</beans>
```

`web-context.xml` contained an `<mvc:annotation-driven>` declaration to enable Spring MVC's annotation based model. This was the first place to start.

**From `<mvc:annotation-driven>` to `@EnableWebMVC`**

`<mvc:annotation-driven>` enables the Spring MVC `@Controller` programming model and adds support for `@RequestMapping` annotations etc.

We had added to the web service a `PageableArgumentResolver` for Spring Data paging query parameter support and an instance of `MappingJackson2HttpMessageConverter` with a custom Jackson `ObjectMapper`. The custom `JacksonObjectMapper` just extended `ObjectMapper` and added a serialization inclusion configuration set to `NON_NULL`, so empty JSON properties would not be outputted.

``` xml web-context.xml
<beans …>
	
	…
	
	<mvc:annotation-driven>
		<mvc:argument-resolvers>
			<bean class="org.springframework.data.web.PageableArgumentResolver" />
		</mvc:argument-resolvers>
		<mvc:message-converters>
			<bean class="org.springframework.http.converter.json.MappingJackson2HttpMessageConverter">
				<property name="objectMapper" ref="jacksonObjectMapper" />
			</bean>
		</mvc:message-converters>
	</mvc:annotation-driven>
	
	<bean id="jacksonObjectMapper" class="com.silverchalice.contracts.json.mappers.JacksonObjectMapper" />
	
	…
	
</beans>
```

The first thing that needed to be done was to create a new configuration class, `WebConfig`, annotated with `@Configuration` and `@EnableWebMVC`. The new class was added to a new package, `com.silverchalice.api.config`.

It is common in many Spring MVC application configurations to just use the default self-closing `<mvc:annotation-driven />` tag; therefore the new configuration class could be just an empty class annotated with `@EnableWebMVC`.

However, since we had added an argument resolver and message conveter customizations, the config class would need to be able to configure these too. This was acheived by extending `WebMvcConfigurerAdapter`. The needed customizations could then be added by simply overriding the appropriate method:

``` java WebConfig.java
package com.silverchalice.api.config;

...

/**
 * Spring MVC Configuration.
 * 
 * Extends {@link WebMvcConfigurerAdapter}, which provides convenient callbacks that allow us to customize aspects of the Spring Web MVC framework.
 * These callbacks allow us to register custom interceptors, message converters, argument resovlers, a validator, resource handling, and other things.
 * 
 * @author robin
 * @see WebMvcConfigurerAdapter
 */
@Configuration
@EnableWebMvc
public class WebConfig extends WebMvcConfigurerAdapter {

	@Override
	public void addArgumentResolvers(List<HandlerMethodArgumentResolver> argumentResolvers) {
		// equivalent to <mvc:argument-resolvers>
	}
	
	@Override
	public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
		// equivalent to <mvc:message-converters>
	}
}
```

To implement the above methods, we needed references to the beans that they used; `PageableArgumentResolver`, `MappingJackson2HttpMessageConverter` and `JacksonObjectMapper`.

This was a simple as adding `@Bean` annotated methods that returned instances of each type that Spring would then manage. The overridden configuation methods could then just add those instances to their respective collections:

``` java WebConfig.java
package com.silverchalice.api.config;

...

@Configuration
@EnableWebMvc
public class WebConfig extends WebMvcConfigurerAdapter {

	@Override
	public void addArgumentResolvers(List<HandlerMethodArgumentResolver> argumentResolvers) {
        argumentResolvers.add(resolver());
	}
	
	@Override
	public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
		converters.add(converter());
	}
	
	@Bean
	public ServletWebArgumentResolverAdapter resolver() {
		return new ServletWebArgumentResolverAdapter(pageable());
	}
	
	@Bean 
	public PageableArgumentResolver pageable() {
		return new PageableArgumentResolver();
	}
	
	@Bean
	public MappingJackson2HttpMessageConverter converter() {
		MappingJackson2HttpMessageConverter converter = new MappingJackson2HttpMessageConverter();
		converter.setObjectMapper(mapper());
		return converter;
	}
	
	/**
	 * Provides the Jackson ObjectMapper with custom configuration for our JSON serialization.
	 * @return The Jackson object mapper with non-null serialization configured
	 */
	@Bean
	public JacksonObjectMapper mapper() {
		return new JacksonObjectMapper();
	}
}
```

You may have noticed that the `PageableArgumentResolver` was wrapped in a `ServletWebArgumentResolverAdapter` before being added to the `argumentResolvers` list. 

This is because Spring Data's `PageableArgumentResolver` interface uses the old `ArgumentResolver` interface instead of the new (Spring 3.1) `HandlerMethodArgumentResolver` interface. The XML config handles this behind the scenes but with a Java config it must be done manually. Thanks to [@doughaber](http://www.twitter.com/doughaber) for this [gotcha](http://blog.fawnanddoug.com/2012/05/pagination-with-spring-mvc-spring-data.html).

As the Spring MVC Java annotation-based configuration was complete, the references to the `<mvc:annotation-driven>` and `jacksonObjectMapper` beans in `web-context.xml` were removed.

We now had an annotated configuration class that configured the container - but only the Spring MVC configuration. The dispatcher servlet configuration (`servlet-config.xml`) was still being referenced as the `contextConfigLocation` under `<servlet>` and we hadn't actually replaced the application context (`root-context.xml`) with an annotated equivalent.

So, a basic `@Configuration` annotated class `AppConfig` was created to replace `root-context.xml`:

``` java AppConfig.java
package com.silverchalice.api.config;

import org.springframework.context.annotation.Configuration;

/**
 * Configuation defining shared resources visible to all other web components, 
 * servlets etc and for cross-cutting concerns like security
 * 
 * @author robin
 */
@Configuration
public class AppConfig {

}
```

`root-context.xml` was then deleted.

Similarly, `ServletConfig` was created to replace `servlet-context.xml`. However, we had only partially migrated the configuration. We needed to include the new `WebConfig` but also the existing `persistence-context.xml`, `bizniz-context.xml`, and `web-context.xml` XML-based configurations.

This was done using the `@Import` and `@ImportResource` annotations respectively:

``` java ServletConfig.java
package com.silverchalice.api.config;

…
	
/**
 * Configuation intended to aggregate the context for 
 * each architectural layer of the application
 * 
 * @author robin
 */
@Configuration
@Import(WebConfig.class)
@ImportResource({
	"classpath:META-INF/spring/persistence-context.xml",
	"classpath:META-INF/spring/bizniz-context.xml",
	"classpath:META-INF/spring/web-context.xml"
})
public class ServletConfig {

}
```

The `WebConfig` configuration class was explicity imported using `@Import`. Since we didn't need `servlet-context.xml` anymore, we used `@ImportResource` to import in the existing XML-based context configurations and deleted `servlet-context.xml`.

Next, we needed to modify our `web.xml` so that the context knows about these Java annotation-based configurations. 

The only thing needed here was to add `contextClass` params for both the application and dispatch servlet contexts referencing `AnnotationConfigWebApplicationContext`, and modifying the `contextConfigLocation` params to use the appropriate configuration class:

``` xml web.xml
<web-app version="2.5" xmlns="http://java.sun.com/xml/ns/javaee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd">

	…
	
	<context-param>
		<param-name>contextClass</param-name>
		<param-value>
		   org.springframework.web.context.support.AnnotationConfigWebApplicationContext
		</param-value>
	</context-param>
	<context-param>
		<param-name>contextConfigLocation</param-name>
		<param-value>com.silverchalice.api.config.AppConfig</param-value>
	</context-param>
	
	…
	
	<servlet>
		<servlet-name>spring-mvc-dispatcher</servlet-name>
		<servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
		<init-param>
			<param-name>contextClass</param-name>
			<param-value>
				org.springframework.web.context.support.AnnotationConfigWebApplicationContext
			</param-value>
		</init-param>
		<init-param>
			<param-name>contextConfigLocation</param-name>
			<param-value>com.silverchalice.api.config.ServletConfig</param-value>
		</init-param>
		<load-on-startup>1</load-on-startup>
	</servlet>
	<servlet-mapping>
		<servlet-name>spring-mvc-dispatcher</servlet-name>
		<url-pattern>/</url-pattern>
	</servlet-mapping>
	
</web-app>
```
	
The Spring MVC configuration was now completely Java annotation-based and the rest of the configuration, while still XML-based, was set up for incremental migration to our new way.

After deploying to Tomcat 7, the logs show that the `AnnotationConfigWebApplicationContext` has worked for both the application and dispatcher servlet configurations (which, in turn, loads the web configuration), while still picking up the renaming XML configurations:

``` logtalk
INFO : org.springframework.web.context.ContextLoader - Root WebApplicationContext: initialization started
INFO : org.springframework.web.context.support.AnnotationConfigWebApplicationContext - Refreshing Root WebApplicationContext: startup date [Thu Dec 27 23:34:24 MST 2012]; root of context hierarchy
INFO : org.springframework.web.context.support.AnnotationConfigWebApplicationContext - Successfully resolved class for [com.silverchalice.api.config.AppConfig]

…

INFO : org.springframework.web.servlet.DispatcherServlet - FrameworkServlet 'spring-mvc-dispatcher': initialization started
INFO : org.springframework.web.context.support.AnnotationConfigWebApplicationContext - Refreshing WebApplicationContext for namespace 'spring-mvc-dispatcher-servlet': startup date [Thu Dec 27 23:34:24 MST 2012]; parent: Root WebApplicationContext
INFO : org.springframework.web.context.support.AnnotationConfigWebApplicationContext - Successfully resolved class for [com.silverchalice.api.config.ServletConfig]
INFO : org.springframework.beans.factory.xml.XmlBeanDefinitionReader - Loading XML bean definitions from class path resource [META-INF/spring/persistence-context.xml]
INFO : org.springframework.beans.factory.xml.XmlBeanDefinitionReader - Loading XML bean definitions from class path resource [META-INF/spring/bizniz-context.xml]
INFO : org.springframework.beans.factory.xml.XmlBeanDefinitionReader - Loading XML bean definitions from class path resource [META-INF/spring/web-context.xml]
``` 

  
<p />
---
**From `<context:component-scan>` to `@ComponentScan`**

Next was to convert how packages are scanned to register beans within the application context.

`web-context.xml` contained the following line:

`<context:component-scan base-package="com.silverchalice.api.controller" />`

	
The `com.silverchalice.api.controller` package contains our Spring MVC components for the presentation layer (the web service interface we are exposing) e.g.

``` java SportsController.java
@Controller
@RequestMapping("/sports")
public class SportsController {
	...
}
```

To replace this component scanning directive with its Java equivalent, the `@ComponentScan` annotation is added to the web configuration class:

``` java WebConfig.java
@ComponentScan(basePackageClasses = { SportsController.class })
@Configuration
@EnableWebMvc
public class WebConfig extends WebMvcConfigurerAdapter {
	...
}
```
	
It would have been possible to just add `@ComponentScan("com.silverchalice.api.controller")` but by using the `basePackageClasses` specifier with a class reference(s), the packages of each class noted will be scanned, which is both type-safe and adds IDE support for future refactoring.

> Indeed, Spring documentation suggests to "consider creating a special no-op marker class or interface in each package that serves no purpose other than being referenced by this attribute".

`<context:component-scan … />` was removed from `web-context.xml`.



<p />
---
**From `<beans profile="…">` to `@Profile`**

With Spring 3.1 also came the ability to conditionally include beans under certain environment bean definition profiles.

[Swagger](http://swagger.wordnik.com/) is a JSON-based specification for "describing, producing, consuming, and visualizing RESTful web services". We forked [@marty_pitt](https://twitter.com/marty_pitt)'s [Swagger Spring MVC](https://github.com/SilverChaliceNewMedia/swagger-springmvc) implementation to provide deployment-tailored Swagger documentation for our web service. 

We used this functionality in `web-context.xml` to declare a `DocumentationController` bean for each deployment environment:

``` xml web-context.xml
…

<!-- Swagger integration -->
<beans profile="dev">
	<bean id="documentationController" class="com.mangofactory.swagger.springmvc.controller.DocumentationController"
			p:apiVersion="1.0"
			p:swaggerVersion="1.0"
			p:basePath="http://localhost:8080/webservice" />
</beans>
<beans profile="prod">
        <bean id="documentationController" class="com.mangofactory.swagger.springmvc.controller.DocumentationController"
           p:apiVersion="1.0"
           p:swaggerVersion="1.0"
           p:basePath="http://webservice.silverchalice.com" />
</beans>

…
```

Depending on which profile is active at application context start, a `documentationController` bean will be available for the specified environment.

[@cbeam](http://www.twitter.com/cbeam)'s blog post, [Spring 3.1 M1: Introducting @Profile](http://blog.springsource.org/2011/02/14/spring-3-1-m1-introducing-profile/), recommended *object-oriented configuration* by declaring configuration interfaces and then using `@Autowired` to inject the profile-dependent configuration themselves. I liked that, so we first created an interface for the application environment configuration:

``` java AppEnvConfig.java
/**
 * Environment configuration interface for application
 * 
 * @author robin
 */
public interface AppEnvConfig {

}
```
	
Before creating an environment configuration interface for the web layer, I created an interface for the Swagger configuration that would support profiles:

``` java SwaggerConfig.java
import com.mangofactory.swagger.springmvc.controller.DocumentationController;

/**
 * Configuration for Swagger Spring MVC API Documentation support
 * 
 * @author robin
 */
public interface SwaggerConfig {

	DocumentationController apiDocs();
	
}
```

The web environment configuration interface then extended both `AppEnvConfig` and `SwaggerConfig`:

``` java WebEnvConfig.java
/**
 * Environment configuration interface for web layer
 * 
 * @author robin
 */
public interface WebEnvConfig extends AppEnvConfig, SwaggerConfig {

}
```
	
Each web environment configuration that implemented this interface was then annotated with `@Profile` whose value specified they profile name:

``` java WebEnvDevConfig.java
/**
 * Environment configuration for the web layer (development profile)
 * 
 * @author robin
 */
@Configuration
@Profile("dev")
public class WebEnvDevConfig implements WebEnvConfig {

	@Override
	public DocumentationController apiDocs() {
		DocumentationController docs = new DocumentationController();
		
		docs.setApiVersion("1.0");
		docs.setSwaggerVersion("1.0");
		docs.setBasePath("http://localhost:8080/webservice");
		
		return docs;
	}

}
```
	
The `apiDocs` method is then overridden per profile and the `DocumentationController` instance is configured for that environment. Similarly, the production environment configuration (`WebEnvProdConfig`) class would instantiate an instance customized for production URLs.

<p />
---
**From `<context:property-placeholder location="…" />` to `@PropertySource`**

However, the various implementations of `WebEnvConfig` with slightly modified `DocumentationController` instances felt like a ["code smell"](http://www.codinghorror.com/blog/2006/05/code-smells.html).

Instead I preferred to use `.properties` files to detail environment-specific settings, for example, `web-dev.properties`:

``` properties web-dev.properties
apiVersion="1.0"
swaggerVersion="1.0"
basePath="http://localhost:8080/webservice"
```

To use properties previously with XML-based configuration, a property placeholder definition would be used:

	<context:property-placeholder location="web-dev.properties" />

With Spring 3.1, the `Environment` abstraction allows [searching for properties across a hierarchy of property sources](http://blog.springsource.com/2011/02/15/spring-3-1-m1-unified-property-management/).

The `@PropertySource` annotation will specifiy a location of properties that will be added to the environment. This makes it very easy to both add to and retrieve properties from the `Environment`.

First, the `WebEnvConfig` abstract class (that now contains the `apiDocs` method) was altered to use the `@Autowired Environment` instance to retrieve the appropriate property value:

``` java WebEnvConfig
public abstract class WebEnvConfig implements AppEnvConfig, SwaggerConfig {

	@Autowired Environment env;

	@Override
	public DocumentationController apiDocs() {
		DocumentationController docs = new DocumentationController();
		
		docs.setApiVersion(env.getProperty("apiVersion"));
		docs.setSwaggerVersion(env.getProperty("swaggerVersion"));
		docs.setBasePath(env.getProperty("basePath"));
		
		return docs;
	}
	
}
```

The, for each `@Profile` annotated concrete web configuration class, the `@PropertySource` annotation's value denotes the location of the `.properties` file to be used:

``` java WebEnvDevConfig
@Configuration
@Profile("dev")
@PropertySource("classpath:web-dev.properties")
public class WebEnvDevConfig extends WebEnvConfig {

}
```

Therefore, for whatever the active profile was (for instance, if the JVM parameter `-Dspring.profiles.active=dev` was used), the `.properties` file for that profile was loaded.

This meant that we could inject in a `WebEnvConfig` instance into our `WebConfig` class and expose our Swagger Spring MVC functionality that would be customized for the environment profile it was launched under.

To do this, we needed to import the profile annotated configuration classes, autowire a configuration instance and them expose a single bean with the desired functionality:

``` java WebConfig.java
@ComponentScan(basePackageClasses = { SportsController.class })
@Configuration
@EnableWebMvc
@Import({WebEnvDevConfig.class, WebEnvProdConfig.class})
public class WebConfig extends WebMvcConfigurerAdapter {

	// the web @Configuration class injected for this @Profile
	@Autowired WebEnvConfig webEnvConfig;
	
	…
	
	/**
	 * Swagger Spring MVC API Documentation support
	 * 
	 * @return swagger documentation controller
	 */
	@Bean
	public DocumentationController documentationController() {
		return webEnvConfig.apiDocs();
	}
	
}
```

Naturally, this approach could be extended across all application layers.

<p />
---
**From `web.xml` to `WebApplicationInitializer`**

The last piece of the puzzle of converting our Spring MVC app's web layer to a fully Java annoatation-based configuration was the conversion of the deployment descriptor itself.

At this moment, our web service was set up as a Servlet 2.5 application, but, since we were using Apache Tomcat 7 as our servlet container, we could use [Servlet 3.0 and its annotation support](http://explodingjava.blogspot.in/2010/05/servlet-30-annotations.html) instead. This also opened up the opportunity to replace most, if not all, of `web.xml` with a programmatic equivalent written in Java.

In order to configure the `ServletContext` programmatically, we needed to create a class that implemented `WebApplicationInitializer`. Implementations of this interface would be detected automatically and bootstrapped by the Servlet 3.0 container.

``` java WebInit.java
package com.silverchalice.api.config;

import javax.servlet.ServletContext;
import javax.servlet.ServletException;

import org.springframework.web.WebApplicationInitializer;

public class WebInit implements WebApplicationInitializer {

	@Override
	public void onStartup(ServletContext container) throws ServletException {
		// TODO Auto-generated method stub
	}

}
```
	
This is simply a matter of replicating our changes to `web.xml` within the `WebInit` class. 

As we are using `@Profile` now, we need to tell the container context what profile to use if no active profile has been configured (either as a JVM argument, an environment variable etc.). This was done in `web.xml` by setting a context init-param:

``` xml
<!- If no active profile is set via -Dspring.profiles.active or 
some other mechanism then this will be used. -->
<context-param>
        <param-name>spring.profiles.default</param-name>
        <param-value>dev</param-value>
</context-param>
```
	
In our new `WebInit` class, this is very easy:

``` java WebInit.java
public class WebInit implements WebApplicationInitializer {

	@Override
	public void onStartup(ServletContext container) throws ServletException {
		/*
		 * If no active profile is set via -Dspring.profiles.active or 
		 * some other mechanism then this will be used.
		 */
		container.setInitParameter("spring.profiles.default", "dev");
		
		…
		
	}
	
}
```
	
Next we created the root application context itself, set its display name, registered the root application configuration and added a context loader listener to bootstrap the container - all very standard stuff. We had set this all up earlier in `web.xml`:

``` xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<web-app version="2.5" xmlns="http://java.sun.com/xml/ns/javaee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd">
...
	<display-name>Silver Chalice Web API</display-name>
	<context-param>
	        <param-name>contextClass</param-name>
	        <param-value>
				org.springframework.web.context.support.AnnotationConfigWebApplicationContext
	        </param-value>
	</context-param>
	<context-param>
	        <param-name>contextConfigLocation</param-name>
	        <param-value>com.silverchalice.api.config.AppConfig</param-value>
	</context-param>
	<!-- Creates the Spring Container shared by all Servlets and Filters -->
	<listener>
	        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
	</listener>
...
</web-app>
```

but it was very straightforward to do this through Java:

``` java
// Creates the root application context
AnnotationConfigWebApplicationContext appContext = 
		new AnnotationConfigWebApplicationContext();

appContext.setDisplayName("Silver Chalice Web API");

// Registers the application configuration with the root context
appContext.register(AppConfig.class);

// Creates the Spring Container shared by all Servlets and Filters
container.addListener(new ContextLoaderListener(appContext));
```
	
Filters were straightforward to convert also:

``` xml
<filter>
        <filter-name>PerfLoggingFilter</filter-name>
        <filter-class>com.silverchalice.api.filter.PerfLoggingFilter</filter-class>
</filter>
<filter-mapping>
        <filter-name>PerfLoggingFilter</filter-name>
        <url-pattern>/*</url-pattern>
</filter-mapping>
```
	
became:

``` java
container.addFilter("PerfLoggingFilter", PerfLoggingFilter.class)
			.addMappingForUrlPatterns(null, false, "/*");
```
				
Finally the `DispatchServlet` itself was migrated from:

``` xml
<servlet>
	<servlet-name>spring-mvc-dispatcher</servlet-name>
	<servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
	<init-param>
		<param-name>contextClass</param-name>
		<param-value>
			org.springframework.web.context.support.AnnotationConfigWebApplicationContext
		</param-value>
	</init-param>
	<init-param>
		<param-name>contextConfigLocation</param-name>
		<param-value>com.silverchalice.api.config.ServletConfig</param-value>
	</init-param>
	<load-on-startup>1</load-on-startup>
</servlet>
<servlet-mapping>
        <servlet-name>spring-mvc-dispatcher</servlet-name>
        <url-pattern>/</url-pattern>
</servlet-mapping>
```
	
to:

``` java
// Creates the dispatcher servlet context
AnnotationConfigWebApplicationContext servletContext = 
		new AnnotationConfigWebApplicationContext();

// Registers the servlet configuraton with the dispatcher servlet context
servletContext.register(ServletConfig.class);

// Further configures the servlet context
ServletRegistration.Dynamic dispatcher = 
		container.addServlet("spring-mvc-dispatcher", 
				new DispatcherServlet(servletContext));
dispatcher.setLoadOnStartup(1);
dispatcher.addMapping("/");
```
	
`web.xml` can be deleted now and the application starts just fine:

``` logtalk
INFO : org.springframework.web.context.ContextLoader - Root WebApplicationContext: initialization started
INFO : org.springframework.web.context.support.AnnotationConfigWebApplicationContext - Refreshing Silver Chalice Web API: startup date [Tue Jan 01 19:21:33 MST 2013]; root of context hierarchy
INFO : org.springframework.web.context.support.AnnotationConfigWebApplicationContext - Registering annotated classes: [class com.silverchalice.api.config.AppConfig]
…
INFO : org.springframework.web.context.ContextLoader - Root WebApplicationContext: initialization completed in 323 ms
DEBUG: com.silverchalice.api.filter.PerfLoggingFilter - initializing perf logging filter
…
INFO: Initializing Spring FrameworkServlet 'spring-mvc-dispatcher'
INFO : org.springframework.web.servlet.DispatcherServlet - FrameworkServlet 'spring-mvc-dispatcher': initialization started
INFO : org.springframework.web.context.support.AnnotationConfigWebApplicationContext - Refreshing WebApplicationContext for namespace 'spring-mvc-dispatcher-servlet': startup date [Tue Jan 01 19:21:34 MST 2013]; parent: Silver Chalice Web API
INFO : org.springframework.web.context.support.AnnotationConfigWebApplicationContext - Registering annotated classes: [class com.silverchalice.api.config.ServletConfig]
…
```
	
And that's it.

<p />
---
**From `<aop:aspectj-autoproxy />` to `@EnableAspectJAutoProxy`**

The single remaining item left in `web-context.xml` was this:

``` xml
<beans …>
		<!-- Enable AspectJ auto-wiring -->
		<aop:aspectj-autoproxy />
</beans>
```

We were using [AspectJ](http://www.eclipse.org/aspectj/) with [Perf4J](http://perf4j.codehaus.org/) to profile our web service. We had added the Perf4J `@Profiled` annotation (not to be confused with the Spring annotation `@Profile`) to our controllers and had created an `aop.xml` file configuring our timing aspect.

To remove `web-context.xml` completely we just needed to add the `@EnableAspectJAutoProxy` annotation to our `WebConfig` configuration class:

``` java
@ComponentScan(basePackageClasses = { SportsController.class })
@Configuration
@EnableAspectJAutoProxy
@EnableWebMvc
@Import({WebEnvDevConfig.class, WebEnvProdConfig.class})
public class WebConfig extends WebMvcConfigurerAdapter {

	…
	
}
```
	
Then the reference to `web-context.xml` was removed from `ServletConfig` and the file itself was deleted.