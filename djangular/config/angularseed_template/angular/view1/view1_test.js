'use strict';

describe('{{ app_name }}.view1 module', function() {

  beforeEach(module('{{ app_name }}.view1'));

  describe('view1 controller', function(){

    it('should ....', inject(function($controller) {
      //spec body
      var view1Ctrl = $controller('View1Ctrl');
      expect(view1Ctrl).toBeDefined();
    }));

  });
});