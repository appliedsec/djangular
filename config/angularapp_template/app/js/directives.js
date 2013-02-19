'use strict';

/* Directives */


angular.module('{{ app_name }}.directives', []).
  directive('appVersion', ['version', function(version) {
    return function(scope, elm, attrs) {
      elm.text(version);
    };
  }]);
