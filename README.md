djangular
=========

A reusable app that provides better app integration with Angular.  Djangular allows you to create Angular content per
app, instead of creating a single massive Angular application inside of Django.  This allows you to selectively use
apps per site, as well as create a consistent structure across all of your Django apps.

This is intended to be a Django version of the Angular Seed project (https://github.com/angular/angular-seed).  The
current mindset is to limit the amount of changes introduced by Djangular.


Requirements
------------

+ Local installs of Node.js and Testacular for testing.
+ Currently requires Python 2.7.
+ Required Django 1.4 or 1.5.


Configuration Changes Needed for Djangular
------------------------------------------

+ Djangular needs to be placed as an app inside a Django project and added to the INSTALLED_APPS setting.  Also, the
  staticfiles contrib library will need to be included if it isn't.

        INSTALLED_APPS = (
            ...
            'django.contrib.staticfiles',
            'djangular',
            ...
        )

+ The STATICFILES_FINDERS needs to be updated to include `djangular.finders.NamespacedAngularAppDirectoriesFinder`.

        STATICFILES_FINDERS = (
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            'djangular.finders.NamespacedAngularAppDirectoriesFinder'
        )

+ Because of this new finder, the `findstatic` and `collectstatic` commands will place the angular files underneath an
  `app_name/` folder.  You will not need to namespace each of your static directories (unless you really want to).

+ To create an app already setup with the djangular (angular-seed) structure, run `python manage.py startangularapp
  <app_name>` from the command line.  This will create the files and directory structures needed for you to get
  started.

+ To use the Angular module that Djangular provides you, you'll need to add the djangular app to your projects URLs.

        urlpatterns = patterns('',
            ...
            url(r'^djangular/', include('djangular.urls')),
            ...
        )

+ Djangular also includes a JSON Vulnerability middleware that AngularJS knows how to process.  To include this
  protection, add `djangular.middleware.AngularJsonVulnerabilityMiddleware` to the MIDDLEWARE_CLASSES setting.  This
  only affects JSON requests (based on Content-Type), so this can be located fairly low in the middleware stack.

        MIDDLEWARE_CLASSES = (
            ...
            'djangular.middleware.AngularJsonVulnerabilityMiddleware'
        )


Comparison between Djangular and Angular-Seed
---------------------------------------------

+ Each app has its own Angular "app" folder, with directories for CSS, JS, images and partials supplied.  As a result,
  the URLs for these get grouped into the STATIC_URL structure of Django.  So, each resource inside an Angular app will
  have a `{{ STATIC URL }}/{{ app_name }}/` prefix.
    * Note: Because of these URLs, referring to Angular content in a separate app should use a `../<separate_app>/`
      URL.  This will help significantly during testing to make sure paths are correct.
    * Note: It is recommended to namespace the Angular code the same name as the Django app.  The created JS files do
      this already.

+ Tests have moved from `test/` to `tests/`.  There are `unit/` and `e2e/` subdirectories where the Angular tests go.

+ The `lib/` directory (containing the AngularJS code) has been moved to the static folder of the Djangular app.  This
  will use the normal Django static urls: `{{ STATIC URL }}/lib/angular/angular.js`

+ The overall `config/` directory is placed inside of the Djangular app itself.  Each Django app doesn't need it's own
  Angular config.

+ The overall `scripts/` directory has been moved to the `management/` directory.  Scripts have been made into Django
  commands.  Django commands have been created instead of using the Angular Seed scripts.
    * `runtestserver` runs a local Django Web Server configured to support running all e2e tests.
    * `startangularapp` creates a Django app with the Angular structure.
    * `testngunit` runs the Testacular Server for all of the unit tests.
    * `testnge2e` runs the Testacular Server for all of the e2e tests.  This requires the `runtestserver` to be running
      beforehand.


How to obtain the Django Template variables into Angular
--------------------------------------------------------

There is an Angular module called `djangular` that is rendered via the Django templating engine to obtain common
template variables like the `STATIC_URL`, `MEDIA_URL`, the User object, etc.  This app includes a service called
`DjangoProperties`, which will enable you to get access to those variables, and a `django` filter, which follows the
standard Angular filtering rules.  The URL for this JavaScript is `/djangular/app.js` (Note that is not static).


Roadmap
-------

+ There are several configuration files that are meant to be editable inside the app.  While this is convenient for
  customization, it causes issues with packaging and upgrading djangular that need to be addressed.
+ Allow single app testing for testacular unit and e2e tests.
+ Auto-detection of node and testacular installs.
+ Providing additional synchronization between Django models and Angular's $resource.  This includes removing the patch
  for Angular's $resource, yet not having to require Django's `FORCE_SLASHES` setting to be False.
