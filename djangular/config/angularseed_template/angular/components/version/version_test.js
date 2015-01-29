'use strict';

describe('{{ app_name }}.version module', function() {
  beforeEach(module('{{ app_name }}.version'));

  describe('version service', function() {
    it('should return current version', inject(function(version) {
      expect(version).toEqual('0.1');
    }));
  });
});
