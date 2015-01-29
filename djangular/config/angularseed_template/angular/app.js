'use strict';

// Declare app level module which depends on views, and components
angular.module('{{ app_name }}', [
  'ngRoute',
  '{{ app_name }}.view1',
  '{{ app_name }}.view2',
  '{{ app_name }}.version'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/view1'});
}]);
