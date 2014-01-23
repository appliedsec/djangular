djangular
=========

A reusable app that provides better app integration with AngularJS. Djangular
allows you to create AngularJS content per app, instead of creating a single
massive AngularJS application inside of Django. This allows you to selectively
use apps per site, as well as create a consistent structure across all of your
Django apps.

This is intended to be a Django version of the Angular-Seed project
(https://github.com/angular/angular-seed). The current mindset is to limit the
amount of changes introduced by Djangular.


Requirements
------------

+ Currently requires Python 2.7.
+ Supports Django 1.4+ and Angular 1.2.3.
+ Local installs of Node.js and Karma for testing.


Installation
------------

+ You may install directly from pypi:

        pip install djangular

+ Or download the source and install it in a terminal/console:

        python setup.py install

+ Or download the source and move the djangular directory inside your django
  project as an app (this is the least recommended approach).


Configuration Changes Needed for Djangular
------------------------------------------

+ Djangular needs to be placed as an app inside a Django project and added to
  the INSTALLED_APPS setting. Also, the staticfiles contrib library will need to
  be included if it isn't.

        INSTALLED_APPS = (
            ...
            'django.contrib.staticfiles',
            'djangular',
            ...
        )

+ After you install Djangular inside a project, you will need to run the
  `makeangularsite` command to properly setup Karma into your default site
  directory. Note: You may need to edit these configuration templates to add any
  additional javascript libraries.

        python manage.py makeangularsite

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

+ To create an app that is already setup with the djangular (angular-seed)
  structure, run `python manage.py startangularapp <app_name>` from the command
  line. This will create the files and directory structures needed for you to
  get started.

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

+ Djangular also includes a JSON Vulnerability middleware that AngularJS knows
  how to process. To include this protection, add
  `djangular.middleware.AngularJsonVulnerabilityMiddleware` to the
  `MIDDLEWARE_CLASSES` setting. This only affects JSON requests (based on
  Content-Type), so this can be located fairly low in the middleware stack.

        MIDDLEWARE_CLASSES = (
            ...
            'djangular.middleware.AngularJsonVulnerabilityMiddleware'
        )


Comparison between Djangular and Angular-Seed
---------------------------------------------

+ Each app has its own AngularJS "app" folder, with directories for CSS, JS,
  images and partials supplied. As a result, the URLs for these get grouped into
  the STATIC_URL structure of Django. So, each resource inside an AngularJS app
  will have a `{{ STATIC URL }}/{{ app_name }}/` prefix.
    * Note: Because of these URLs, referring to AngularJS content in a separate
      app should use a `../<separate_app>/` URL. This will help significantly
      during testing to make sure paths are correct.
    * Note: It is recommended to namespace the AngularJS code the same name as the
      Django app. The created JS files do this already.
    * Example: If you have a Django app named `foo` and you are using the
      default `STATIC_URL` in your settings, the main AngularJS module named
      `foo` would be found at `/static/foo/js/app.js`.

+ Tests have moved from `test/` to `tests/`. There are `unit/` and `e2e/`
  subdirectories where the Karma tests go.

+ The `lib/` directory (containing the AngularJS code) has been moved to the
  static folder of the Djangular app. This will use the normal Django static
  urls: `{{ STATIC_URL }}/lib/angular/angular.js`

+ The `config/` directory is now placed inside of your default Django site. Each
  individual Django app doesn't need its own AngularJS or Karma config.

+ The `scripts/` directory has been removed, because the Angular-Seed scripts
  have been made into Django commands. These commands exist in the standard
  `management/` directory.
    * `makeangularsite` places the Karma configuration templates inside the
      given Django Site directory. This should be run after installing
      Djangular.
    * `runtestserver` runs a local Django Web Server configured to support
      running all e2e tests.
    * `startangularapp` creates a Django app with the AngularJS structure.
    * `testjs` runs the Karma Server for either the unit or e2e tests. Note that
      the e2e tests requires the `runtestserver` to be running beforehand.


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
STATIC_URL. Using 'sample' as the name of the Django/Angular JS app:

```javascript
angular.module('sample', [
    'djangular', 'sample.filters', 'sample.services', 'sample.directives',
    'sample.controllers'
    ]).config([
        '$routeProvider','DjangoProperties',
        function($routeProvider, DjangoProperties) {
            $routeProvider.when('/view1', {
                templateUrl: DjangoProperties.STATIC_URL +
                    'sample/partials/partial1.html', controller: 'MyCtrl1'});
            $routeProvider.when('/view2', {
                templateUrl: DjangoProperties.STATIC_URL +
                    'sample/partials/partial2.html', controller: 'MyCtrl2'});
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
    <script src="{{ STATIC_URL }}/lib/angular/angular-min.js"></script>

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

Enforcing the end slashes of your Angular Resources
---------------------------------------------------

$resource is a convenient way to create REST-like services in Angular.  However,
there currently [is a bug](https://github.com/angular/angular.js/issues/992) in
$resource that will strip the ending slash, which means that $resource is
unusable unless `settings.APPEND_SLASHES` is set to `FALSE`.

Djangular used to patch this automatically, but it now includes a separate file
(`djangular/static/js/resource_patch.js`) to handle this issue.  Simply include
that javascript file in your page after you have loaded `angular-resource.js`
and ending slashes will be preserved in $resource.


Enabling CSRF protection in AngularJS Templates
-----------------------------------------------

If you have enabled CSRF protection in Django by adding the middleware
`django.middleware.csrf.CsrfViewMiddleware` to the `MIDDLEWARE_CLASSES` setting,
you may use the same protection in AngularJS templates in addition to Django
template.  There are two different ways to enable this protection via djangular:

+ Make your main app dependent on the `djangular` module and use the included
  `csrf-token` directive (that wraps the Django `csrf_token` template tag)
  inside the appropriate `form` tags in your HTML.

        // Inside your JavaScript
        angular.module('myApp', ['djangular', ...]);
        ...
        <!-- In your Angular Template -->
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

Current Roadmap
---------------

+ Better support for Django 1.6 and Angular 1.2.
+ Auto-detection of node and karma installs.
+ Providing additional synchronization between Django models and AngularJS's
  $resource. This includes removing the patch for AngularJS's $resource, yet not
  having to require Django's `FORCE_SLASHES` setting to be False.
+ Using Django's ModelForms and Templates to provide an easy way to generate
  AngularJS partials.
