/**
 * App.js
 */

define([
    'angular',
    'blog/blog',
    'about/about',
    'source/source',
    'admin/admin',
    'modules/http-auth-interceptor',
    'modules/js-base64',
    'angularRoute',
    'angularCookies',
    'angularSanitize'
], function (angular) {
    'use strict';

    return angular.module('myApp', [
            'ngRoute',
            'ngCookies',
            'ngSanitize',
            'myApp.blog',
            'myApp.about',
            'myApp.source',
            'myApp.admin',
            'http-auth-interceptor',
            'js-base64'
        ])
        /*
         * App configuration and frontend routes.
         */
        .config(['$routeProvider', '$locationProvider', 'RestangularProvider', function ($routeProvider, $locationProvider, RestangularProvider) {
            $routeProvider.when('/blog', {
                templateUrl: 'static/partials/partial_blog.html',
                controller: 'BlogCtrl'
            });
            $routeProvider.when('/about', {
                templateUrl: 'static/partials/partial_about.html',
                controller: 'AboutCtrl'
            });
            $routeProvider.when('/source', {
                templateUrl: 'static/partials/partial_source.html',
                controller: 'SourceCtrl'
            });
            $routeProvider.when('/admin', {
                templateUrl: 'static/partials/partial_admin.html',
                controller: 'AdminCtrl'
            });
            $routeProvider.otherwise({
                redirectTo: '/blog'
            });

            // Try using html5 history API to avoid '#' symbol in URLs.
            if (window.history && window.history.pushState) {
                $locationProvider.html5Mode(true);
            } else {
                console.warn('html5 history not available')
            }

            // Configure Restangular response extractor for JSend protocol.
            RestangularProvider.setResponseExtractor(function (response) {
                var newResponse;
                newResponse = response.data || {};
                newResponse.status = response.status;
                return newResponse;
            });
        }])
        /*
         * Main navigation widget.
         */
        .directive('mainNav', ['$location', function ($location) {
            return {
                restrict: 'E',
                replace: true,
                templateUrl: 'static/partials/wdgt_main_nav.html',
                link: function (scope, element) {
                    var f = this;
                    f.setActiveNav = function () {
                        angular.forEach(element.find('a'), function (a) {
                            if (a.href.substring(a.href.lastIndexOf('/')) === $location.path()) {
                                angular.element(a).parent('li').addClass('active');
                            } else {
                                angular.element(a).parent('li').removeClass('active');
                            }
                        });
                    };
                    scope.$on('$routeChangeSuccess', function () {
                        f.setActiveNav();
                    });
                    f.setActiveNav();
                }
            };
        }]);
});
