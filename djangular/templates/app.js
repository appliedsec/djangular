// Dynamic JS File to load Django values.  Add additional values as needed.
// {% load static %} - This is put in a comment so this can be loaded as a normal JS file.
var djangular = angular.module('djangular', ['ngCookies']).
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
            priority: 100,  // one above the ngHref directive.
            link: function postLink(scope, elem, attrs) {
                var newHref = $filter('django')(attrs.djangoHref);
                attrs.$set('href', newHref);
                // TODO: Do we set ngHref as well?
            }
        };
    }]).
    directive('djangoSrc', ['$filter', function($filter) {
        return {
            priority: 100,  // one above the hgSrc directive.
            link: function postLink(scope, elem, attrs) {
                var newSrc = $filter('django')(attrs.djangoSrc);
                attrs.$set('src', newSrc);
                // TODO: Do we set ngSrc as well?
            }
        };
    }]).
    directive('csrfToken', function() {
        return {
            restrict: 'E',
            template: "{% csrf_token %}",
            replace: true
        };
    });

// Assign the CSRF Token as needed, until Angular provides a way to do this properly (https://github.com/angular/angular.js/issues/735)
djangular.
    config(['$httpProvider', function($httpProvider) {
        // cache $httpProvider, as it's only available during config...
        djangular.$httpProvider = $httpProvider;
    }]).
    run(['$cookies', function($cookies) {
        // now assign the $httpProvider the cookie which Django assigns...
        // TODO: Only for same origin sites...
        djangular.$httpProvider.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
        djangular.$httpProvider.defaults.headers.put['X-CSRFToken'] = $cookies['csrftoken'];
        if (!djangular.$httpProvider.defaults.headers.delete)
            djangular.$httpProvider.defaults.headers.delete = {};
        djangular.$httpProvider.defaults.headers.delete['X-CSRFToken'] = $cookies['csrftoken'];
    }]);
