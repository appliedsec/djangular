'use strict';

angular.module('{{ app_name }}.version', [
  '{{ app_name }}.version.interpolate-filter',
  '{{ app_name }}.version.version-directive'
])

.value('version', '0.1');
