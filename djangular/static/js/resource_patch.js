try {
    if (angular.version.full > "1.3") {
        angular.module('ngResource').config([
            '$resourceProvider', function($resourceProvider) {
                $resourceProvider.defaults.stripTrailingSlashes = false;
            }
        ]);
    } else {
        angular.module('ngResource').config([
            '$provide', '$httpProvider',
            function($provide, $httpProvider) {
                $provide.decorator('$resource', function($delegate) {
                    return function() {
                        if (arguments.length > 0) {  // URL
                            arguments[0] = arguments[0].replace(/\/$/, '\\/');
                        }

                        if (arguments.length > 2) {  // Actions
                            angular.forEach(arguments[2], function(action) {
                                if (action && action.url) {
                                    action.url = action.url.replace(/\/$/, '\\/');
                                }
                            });
                        }

                        return $delegate.apply($delegate, arguments);
                    };
                });

                $provide.factory('djangularEnforceSlashInterceptor', function() {
                    return {
                        request: function(config) {
                            config.url = config.url.replace(/[\/\\]+$/, '/');
                            return config;
                        }
                    };
                });

                $httpProvider.interceptors.push('djangularEnforceSlashInterceptor');
            }
        ]);
    }
} catch (err) {
    console.log('The ngResource module could not be found.');
}