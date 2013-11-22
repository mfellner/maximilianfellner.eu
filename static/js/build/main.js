/*
 * Main.js
 */

require.config({
    // TODO: provide local fallbacks for all CDN resources.
    paths: {
        angular: '//ajax.googleapis.com/ajax/libs/angularjs/1.2.14/angular.min',
        angularRoute: '//ajax.googleapis.com/ajax/libs/angularjs/1.2.14/angular-route.min',
        angularCookies: '//ajax.googleapis.com/ajax/libs/angularjs/1.2.14/angular-cookies.min',
        angularSanitize: '//ajax.googleapis.com/ajax/libs/angularjs/1.2.14/angular-sanitize.min',
        jquery: '//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min',
        bootstrap: '//netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min',
        underscore: ['//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.5.2/underscore-min',
            'static/js/vendor/underscore/underscore-min'],
        restangular: ['//cdnjs.cloudflare.com/ajax/libs/restangular/1.3.1/restangular.min',
            'static/js/vendor/restangular/dist/restangular.min'],
        showdown: '../vendor/showdown/src/showdown'
    },
    shim: {
        angular: {
            exports: 'angular'
        },
        angularRoute: {
            deps: ['angular']
        },
        angularCookies: {
            deps: ['angular']
        },
        angularSanitize: {
            deps: ['angular']
        },
        bootstrap: {
            deps: ['jquery']
        },
        restangular: {
            deps: ['angular', 'underscore']
        },
        showdown: {
            exports: 'showdown'
        }
    },
    priority: [
        'angular'
    ]
});

//http://code.angularjs.org/1.2.1/docs/guide/bootstrap#overview_deferred-bootstrap
window.name = 'NG_DEFER_BOOTSTRAP!';

require([
    'angular',
    'app'
], function (angular, app) {
    'use strict';

    angular.element().ready(function () {
        angular.resumeBootstrap([app['name']]);
    });
});
