basePath = '../../';

files = [
  JASMINE,
  JASMINE_ADAPTER,
  'djangular/static/lib/angular/angular.js',
  'djangular/static/lib/angular/angular-*.js',
  'djangular/tests/lib/angular/angular-mocks.js',
  'djangular/templates/app.js',
  '*/app/js/**/*.js',
  '*/tests/unit/**/*.js'
];

autoWatch = true;

browsers = ['Chrome'];

junitReporter = {
  outputFile: 'test_out/unit.xml',
  suite: 'unit'
};
