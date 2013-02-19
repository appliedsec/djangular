'use strict';

/* jasmine specs for filters go here */

describe('filter', function() {
    beforeEach(module('djangular'));

    describe('django', function() {
        it('should replace STATIC_URL inside of percent signs', inject(function(djangoFilter) {
            expect(djangoFilter('before %STATIC_URL% after')).
                toEqual('before {% get_static_prefix %} after');
        }));

        it('should replace STATIC_URL without percent signs', inject(function(djangoFilter) {
            expect(djangoFilter('before STATIC_URL after')).
                toEqual('before {% get_static_prefix %} after');
        }));

        it('should replace MEDIA_URL inside of percent signs', inject(function(djangoFilter) {
            expect(djangoFilter('before %MEDIA_URL% after')).
                toEqual('before {% get_media_prefix %} after');
        }));

        it('should replace MEDIA_URL without percent signs', inject(function(djangoFilter) {
            expect(djangoFilter('before MEDIA_URL after')).
                toEqual('before {% get_media_prefix %} after');
        }));

        it('should replace USER_NAME inside of percent signs', inject(function(djangoFilter) {
            expect(djangoFilter('before %USER_NAME% after')).
                toEqual('before {{ user.username|escapejs }} after');
        }));

        it('should replace USER_NAME without percent signs', inject(function(djangoFilter) {
            expect(djangoFilter('before USER_NAME after')).
                toEqual('before {{ user.username|escapejs }} after');
        }));

        it('should replace IS_AUTHENTICATED inside of percent signs', inject(function(djangoFilter) {
            expect(djangoFilter('before %IS_AUTHENTICATED% after')).
                toEqual('before false after');
        }));

        it('should replace IS_AUTHENTICATED without percent signs', inject(function(djangoFilter) {
            expect(djangoFilter('before IS_AUTHENTICATED after')).
                toEqual('before false after');
        }));
    });
});
