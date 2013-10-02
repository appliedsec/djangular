// {% load static %} - This is put in a comment so this can be loaded as a normal JS file.
angular.module('djangular', []).
    constant('DjangoProperties', {
        'STATIC_URL': '{% get_static_prefix %}',
        'MEDIA_URL': '{% get_media_prefix %}',
        'USER_NAME': '{{ user.username|escapejs }}',
        'GROUP_NAMES': [ // {% for group in user.groups.all %}
            '{{ group.name|escapejs }}', // {% endfor %}
        ],
        'IS_AUTHENTICATED': 'True' === '{{ user.is_authenticated|escapejs }}'
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
            priority: 98, // same as ng-href
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
            priority: 98, // same as ng-src
            link: function(scope, elem, attrs) {
                attrs.$observe('djangoSrc', function(value) {
                    if (!value) return;
                    attrs.$set('src', $filter('django')(value));
                });
            }
        };
    }]);

var djangularCsrf = angular.module('djangular.csrf', ['ngCookies']).
    directive('csrfToken', function() {
        return {
            restrict: 'E',
            template: "{% csrf_token %}",
            replace: true
        };
    });

// {% if not disable_csrf_headers %}
// Assign the CSRF Token as needed, until Angular provides a way to do this properly (https://github.com/angular/angular.js/issues/735)
djangularCsrf.
    config(['$httpProvider', function($httpProvider) {
        // cache $httpProvider, as it's only available during config...
        djangularCsrf.$httpProvider = $httpProvider;
    }]).
    run(['$cookies', function($cookies) {
        // now assign the $httpProvider the cookie which Django assigns...
        djangularCsrf.$httpProvider.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
        djangularCsrf.$httpProvider.defaults.headers.put['X-CSRFToken'] = $cookies['csrftoken'];
        if (!djangularCsrf.$httpProvider.defaults.headers.delete)
            djangularCsrf.$httpProvider.defaults.headers.delete = {};
        djangularCsrf.$httpProvider.defaults.headers.delete['X-CSRFToken'] = $cookies['csrftoken'];
    }]);
// {% endif %}
