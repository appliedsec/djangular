// All template syntax is commented so this can be loaded as a normal JS file.
// {% load static %}
var djangular = angular.module('djangular', []).
    constant('DjangoProperties', {
        'STATIC_URL': '{% get_static_prefix %}',
        'MEDIA_URL': '{% get_media_prefix %}',
        'USER_NAME': '{{ user.username|escapejs }}',
        'GROUP_NAMES': [ // {% for group in user.groups.all %}
            '{{ group.name|escapejs }}', // {% endfor %}
        ],
        'IS_AUTHENTICATED': 'True' === '{{ user.is_authenticated|escapejs }}',
        'IS_STAFF': 'True' === '{{ user.is_staff }}',
        'IS_SUPERUSER': 'True' === '{{ user.is_superuser }}'
    }).
    filter('django', ['DjangoProperties', function(DjangoProperties) {
        return function(text) {
            for (var constant in DjangoProperties) {
                text = text.replace('%' + constant + '%', DjangoProperties[constant]);
                text = text.replace(constant, DjangoProperties[constant]);
            }
            return text;
        }
    }]).
    directive('djangoHref', ['$filter', function($filter) {
        return {
            restrict: 'A',
            priority: 99, // same as ng-href
            link: function(scope, elem, attrs) {
                attrs.$observe('djangoHref', function(value) {
                    if (!value) return;
                    attrs.$set('href', $filter('django')(value));
                });
            }
        };
    }]).
    directive('djangoSrc', ['$filter', function($filter) {
        return {
            restrict: 'A',
            priority: 99, // same as ng-src
            link: function(scope, elem, attrs) {
                attrs.$observe('djangoSrc', function(value) {
                    if (!value) return;
                    attrs.$set('src', $filter('django')(value));
                });
            }
        };
    }]).
    directive('csrfToken', function() {
        return {
            restrict: 'E',
            template: "{% csrf_token %}" || "<span></span>",
            replace: true
        };
    });

// {% if not disable_csrf_headers %}
// Assign the CSRF Token as needed, until Angular provides a way to do this properly (https://github.com/angular/angular.js/issues/735)
var djangularCsrf = angular.module('djangular.csrf', ['ngCookies']).
    config(['$httpProvider', function($httpProvider) {
        // cache $httpProvider, as it's only available during config...
        djangularCsrf.$httpProvider = $httpProvider;
    }]).
    factory('UpdateCsrfToken', function() {
        return function(csrfToken) {
            djangularCsrf.$httpProvider.defaults.headers.post['X-CSRFToken'] = csrfToken;
            djangularCsrf.$httpProvider.defaults.headers.put['X-CSRFToken'] = csrfToken;
            if (!djangularCsrf.$httpProvider.defaults.headers.delete)
                djangularCsrf.$httpProvider.defaults.headers.delete = {};
            djangularCsrf.$httpProvider.defaults.headers.delete['X-CSRFToken'] = csrfToken;
        };
    }).
    run(['$cookies', 'UpdateCsrfToken', function($cookies, UpdateCsrfToken) {
        UpdateCsrfToken($cookies['csrftoken']);
    }]);
// {% endif %}
