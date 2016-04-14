djangular
=========

A reusable app that provides better app integration with AngularJS. Djangular
allows you to create AngularJS content per app, instead of creating a single
massive AngularJS application inside of Django. This allows you to selectively
use apps per site, as well as create a consistent structure across all of your
Django apps.

This is intended to be a Django version of the angular-seed project
(https://github.com/angular/angular-seed). The current mindset is to limit the
amount of changes introduced by Djangular.


Features
--------

+ Allows namespacing AngularJS content per Django app.  This allows the
  AngularJS apps and modules to be included (or not) based on Django's settings,
  and enforces a consistent structure to your Django/AngularJS apps.
+ Includes an AngularJS module that includes a subset of features similar to
  what Django provides in its templates.
+ Adds a patch to AngularJS's $resource module, to enable end of URL slashes
  that Django requires.
+ Improves security by enabling of CSRF protection and JSON Vulnerability
  between Django and AngularJS.
+ ~~Scripts to allow running JS Unit and E2E tests, similar to the Django test
  command.~~ This was removed for the time being and will be (re-)included in a
  future release.
+ Does not dictate how you use AngularJS inside your Django app.


Requirements
------------

+ Currently requires Python 2.7.
+ Supports Django 1.5+ (including 1.8.x).
+ Supports AngularJS 1.2+ (including 1.3.x).
+ ~~Local installs of Node.js and Karma for testing.~~


Installation
------------

+ You may install directly from pypi:

        pip install djangular

+ Or download the source and install it in a terminal/console:

        python setup.py install

+ Or download the source and move the djangular directory inside your django
  project as an app (this is the least recommended approach).

+ Djangular needs to be placed as an app inside a Django project and added to
  the INSTALLED_APPS setting.

        INSTALLED_APPS = (
            ...
            'djangular',
            ...
        )

+ You will need to obtain a version of AngularJS and place it in the `static`
  folder of one of your Django apps.  Djangular no longer includes a version of
  AngularJS, since it updates too frequently.


Including AngularJS content in your Django Apps
-----------------------------------------------

The most popular feature of Djangular, this will both include and namespace your
AngularJS content inside your Django apps.  Each Django app has its own
"angular" folder, with a layout matching the angular-seed project. As a result,
the URLs for these get grouped into the `STATIC_URL` structure of Django.

+ The staticfiles contrib library will need to be included in the INSTALLED_APPS
  setting.

        INSTALLED_APPS = (
            ...
            'django.contrib.staticfiles',
            'djangular',
            ...
        )

+ The STATICFILES_FINDERS needs to be updated to include
  `djangular.finders.NamespacedAngularAppDirectoriesFinder`.

        STATICFILES_FINDERS = (
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            'djangular.finders.NamespacedAngularAppDirectoriesFinder'
        )

+ Because of this new finder, the `findstatic` and `collectstatic` commands will
  place the angular files in each app in an associated an `<app_name>/` folder.
  You will not need to namespace each of your static directories with the name
  of your Django application (unless you really want to).
    * Example: If you have a Django app named `foo` and you are using the
      default `STATIC_URL` in your settings, the main AngularJS module named
      `foo` would be found at `foo/angular/app.js` on the file system and at
      `static/foo/app.js` from the browser.
    * This namespacing is done automatically.  This a `foo` app and a `bar` app
      can both have an `app.js` inside their `angular` directories, and they
      will not collide.
    * Note: Because of these URLs, referring to AngularJS content in a separate
      app should use a `../<separate_app>/` URL. This will help significantly
      during testing to make sure paths are correct.
    * Note: It is recommended to namespace the AngularJS code the same name as
      the Django app. The created JS files do this already.

+ To create an app that is already setup with the djangular (or angular-seed)
  structure, run `python manage.py startangularapp <app_name>` from the command
  line. This will create the files and directory structures needed for you to
  get started.


Including some Django template-like features in your AngularJS templates
------------------------------------------------------------------------

One of the challenges in using AngularJS inside of Django is that you may not
have access to some needed variables that are always included in Django
templates.  Djangular includes an AngularJS module to help with that.

+ To use the AngularJS module that Djangular provides you, you'll need to add
  the djangular app to your projects URLs.

        urlpatterns = patterns('',
            ...
            url(r'^djangular/', include('djangular.urls')),
            ...
        )

+ Alternatively, you may specify the DjangularModuleTemplateView specifically,
  and customize the url.

        from djangular.views import DjangularModuleTemplateView
        ...

        urlpatterns = patterns('',
            ...
            url(r'<custom_path>/djangular.js',
                DjangularModuleTemplateView.as_view()),
            ...
        )

This will add a `djangular` AngularJS module to your front end code.  This
module includes a `DjangoProperties` constant that includes whether the current
user is authenticated, the username, groups and roles of the current user and
the static and media urls from Django settings.  It also includes a `django`
filter, which does some basic substitution based on the properties constant.


Enforcing the end slashes of your AngularJS Resources
-----------------------------------------------------

$resource is a convenient way to create REST-like services in AngularJS.
However, there currently
[is a bug](https://github.com/angular/angular.js/issues/992) in $resource that
will strip the ending slash, which means that $resource is unusable unless
`settings.APPEND_SLASHES` is set to `FALSE`.

Djangular used to patch this automatically, but it now includes a separate file
(`djangular/static/js/resource_patch.js`) to handle this issue.  Simply include
that javascript file in your page after you have loaded `angular-resource.js`
and ending slashes will be preserved in $resource.


Enabling CSRF protection in AngularJS Templates
-----------------------------------------------

Djangular includes a JSON Vulnerability middleware that AngularJS knows how to
process. To include this protection, add
`djangular.middleware.AngularJsonVulnerabilityMiddleware` to the
`MIDDLEWARE_CLASSES` setting. This only affects JSON requests (based on
Content-Type), so this can be located fairly low in the middleware stack.

        MIDDLEWARE_CLASSES = (
            ...
            'djangular.middleware.AngularJsonVulnerabilityMiddleware'
        )

Once you have enabled CSRF protection in Django by adding the middleware
`django.middleware.csrf.CsrfViewMiddleware` to the `MIDDLEWARE_CLASSES` setting,
you may use the same protection in AngularJS templates in addition to Django
template.  There are two different ways to enable this protection via djangular:

+ Make your main app dependent on the `djangular` module and use the included
  `csrf-token` directive (that wraps the Django `csrf_token` template tag)
  inside the appropriate `form` tags in your HTML.

        // Inside your JavaScript
        angular.module('myApp', ['djangular', ...]);
        ...
        <!-- In your AngularJS Template -->
        <div ng-app="my-app">
            ...
            <form ...>
                <csrf-token></csrf-token>
            </form>
        </div>

+ Make your main app dependent on the `djangular.csrf`, which will add the
  appropriate CSRF Token Header in all POSTs, PUTs and DELETEs.  Note that this
  way is vulnerable to cross-site scripting if you make a post to a domain
  outside your control.

        angular.module('myApp', ['djangular.csrf', ...]);

If you allow a user to login (or logout) and don't redirect or reload the page,
the tags and cookies provided by both methods above will be stale.  The second
option (using the `djangular.csrf` module) provides a `UpdateCSRFToken` function
that can be invoked with the new CSRF Token value.


Using Djangular in your Django Project
--------------------------------------

This section describes some best practices in using Djangular. Please note that
these are guidelines and recommendations, but not the only way to use this
project.

#### AngularJS as purely static content ####

The first way to use djangular is to have all of your static content live inside
an angular app. This is perhaps the "most correct" way from an AngularJS
standpoint and perhaps the "least correct" way from a traditional Django
perspective.

In doing this, you are only (or almost only) serving content from your static
domain and your Django development becomes strictly back-end focused for REST
and/or service calls. Few to none of your Django views will produce HTML. You
can provide a redirect from a Django view to your static pages (if you like),
although this can seem strange when your static content is served from a
completely different domain. You may need to configure your web servers to
allow remote Ajax calls from your static domain.

This approach allows you to use AngularJS with any number of back-ends, as
(again) your Django app becomes an API for your AngularJS code to call. This
approach can be very different from how your application is currently
architected.

From our experience, if you decide to do this, we would recommend using local,
relative URLs to navigate between the apps instead of specifying the full URL.
However, there are times when you will need to specify the full URL.

There is an AngularJS module called `djangular` that is rendered via the Django
templating engine to obtain common template variables like the `STATIC_URL`,
`MEDIA_URL`, the User object, etc.  This app includes a service called
`DjangoProperties`, which will enable you to get access to those variables, and
a `django` filter, which follows the standard AngularJS filtering rules. The URL
for this JavaScript is `/djangular/app.js` (note that is not static).

The following is a sample route config that uses the aforementioned djangular
angular app. Because AngularJS has not set up the $filter directive during the
route configuration, the DjangoProperties constant is the only way to obtain the
STATIC_URL. Using 'sample' as the name of the Django/AngularJS app:

```javascript
angular.module('sample', [
    'djangular', 'sample.filters', 'sample.services', 'sample.directives',
    'sample.controllers'
    ]).config([
        '$routeProvider','DjangoProperties',
        function($routeProvider, DjangoProperties) {
            $routeProvider.when('/view1', {
                templateUrl: DjangoProperties.STATIC_URL +
                    'sample/view1/view1.html', controller: 'View1Ctrl'});
            $routeProvider.when('/view2', {
                templateUrl: DjangoProperties.STATIC_URL +
                    'sample/view2/view2.html', controller: 'View2Ctrl'});
            $routeProvider.otherwise({redirectTo: '/view1'});
        }
    ]);
```

#### Django Templates as AngularJS Templates ####

Another way to integrate is to use your Django templates as your AngularJS
templates. To do this, we highly recommend using Django 1.5 and heavy use of
the `{% verbatim %}` tag, since the Django and AngularJS templating syntaxes are
identical.

The big advantage of this is that it allows you to use all of the existing
template tags and ways of thinking that you are accustomed to using. If you are
integrating AngularJS into an existing Django project, this will seem the most
appealing.

The downsides to this method are the following:
+ The AngularJS developers recommend not doing this, because it is very easy
  to get confused about which part of the template is being rendered on the
  server side and which is being rendered on the client side. Almost every
  developer on our team has tripped on this once or twice.
+ The vast majority of HTML that your app is producing is the same on every
  load... and should be static. However, without some cache configuration, the
  server will have to render the content on every single request, resulting in
  poorer performance.

#### Using Django Templates to render the skeleton of the app ####

What our team currently does is use a Django Template to render the skeleton of
every page, but the rest of the page (the partials, CSS and JS) are all included
in the AngularJS app. This way, none of the CSS/JS dependencies are duplicated
in multiple places.

When our app renders the content, we pass in two variables to the RequestContext
(and thus, to the template). The `app_name`, which is the name of the app, and
`app_dependencies`, which is a list of app names whom the AngularJS app is
dependent on. We make heavy use of Django Rest Framework
(http://django-rest-framework.org/) to produce our views/REST Services and
Django Pipeline (https://github.com/cyberdelia/django-pipeline) to do our app
packaging and JS/CSS Compression.

The template (more or less) looks like the following:
```html
{% load compressed %}  <!-- We use django-pipeline to do our packaging -->

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>App Title</title>
	<link rel="shortcut icon" href="{{ STATIC_URL }}images/app.ico" />

    <!--CSS imports-->
    {% for dependency in app_dependencies %}
        {% compressed_css dependency %}
    {% endfor %}
    {% compressed_css app_name %}

    <!--AngularJS library imports-->
    <script src="{{ STATIC_URL }}angular/angular-min.js"></script>

    <!--AngularJS app imports-->
    <script src="/djangular/app.js"></script>  <!-- The djangular app. -->
    {% for dependency in app_dependencies %}
        {% compressed_js dependency %}
    {% endfor %}
    {% compressed_js app_name %}

</head>
<body ng-app="{{app_name}}">
    <div class="app" ng-view>
    </div>
</body>
</html>
```