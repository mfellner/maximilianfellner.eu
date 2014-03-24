/*
 * Main.js
 */

require.config({
    paths: {
        angular: ['//ajax.googleapis.com/ajax/libs/angularjs/1.2.14/angular.min',
            'static/js/vendor/angular/angular.min'],
        angularRoute: ['//ajax.googleapis.com/ajax/libs/angularjs/1.2.14/angular-route.min',
            'static/js/vendor/angular/angular-route.min'],
        angularCookies: ['//ajax.googleapis.com/ajax/libs/angularjs/1.2.14/angular-cookies.min',
            'static/js/vendor/angular/angular-cookies.min'],
        angularSanitize: ['//ajax.googleapis.com/ajax/libs/angularjs/1.2.14/angular-sanitize.min',
            'static/js/vendor/angular/angular-sanitize.min'],
        jquery: ['//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min',
            'static/js/vendor/jquery-1.11.0.min'],
        bootstrap: ['//netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min',
            'static/css/vendor/bootstrap/dist/js/bootstrap.min'],
        underscore: ['//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.5.2/underscore-min',
            'static/js/vendor/underscore/underscore-min'],
        restangular: ['//cdnjs.cloudflare.com/ajax/libs/restangular/1.3.1/restangular.min',
            'static/js/vendor/restangular/dist/restangular.min'],
        prettify: ['//cdnjs.cloudflare.com/ajax/libs/prettify/r298/prettify',
            'static/js/vendor/prettify.min'],
        showdown: '../vendor/showdown/src/showdown',
        showdownCodify: 'extensions/showdown-codify'
    },
    shim: {
        angular: {
            exports: 'angular',
            deps: ['jquery']
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

    angular.forEach(document.getElementsByTagName('meta'), function (meta) {
        if (meta.name === 'version') {
            app.constant('appRevision', meta.content);
        }
    });

    angular.element().ready(function () {
        angular.resumeBootstrap([app['name']]);
    });
});
