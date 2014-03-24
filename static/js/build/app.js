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
        .config(['$routeProvider', '$locationProvider', 'RestangularProvider', 'appRevision', function ($routeProvider, $locationProvider, RestangularProvider, appRevision) {
            $routeProvider.when('/blog', {
                templateUrl: 'static/partials/partial_blog.html?v=' + appRevision,
                controller: 'BlogCtrl'
            });
            $routeProvider.when('/about', {
                templateUrl: 'static/partials/partial_about.html?v=' + appRevision,
                controller: 'AboutCtrl'
            });
            $routeProvider.when('/source', {
                templateUrl: 'static/partials/partial_source.html?v=' + appRevision,
                controller: 'SourceCtrl'
            });
            $routeProvider.when('/admin', {
                templateUrl: 'static/partials/partial_admin.html?v=' + appRevision,
                controller: 'AdminCtrl'
            });
            $routeProvider.otherwise({
                redirectTo: '/blog'
            });
            // Add #-prefix for SEO.
            $locationProvider.hashPrefix('!');
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
         * Main sidebar widget.
         */
        .directive('sidebar', ['$compile', '$http', '$templateCache', '$window', 'appRevision',
            function ($compile, $http, $templateCache, $window, appRevision) {

                var getTemplate = function (process) {
                    var templateUrl = 'static/partials/wdgt_sidebar.html?v=' + appRevision;
                    $http.get(templateUrl, {cache: $templateCache}).success(function (html) {
                        process(html);
                    });
                };

                var link = function (scope, element) {
                    scope.revision = appRevision.substring(0, 7);
                    scope.year = new Date().getFullYear();
                    scope.windowWidth = $($window).width();
                    scope.loaded = false;

                    var isWithinBounds = function (width) {
                        if (!scope.minWidth) {
                            scope.minWidth = 0;
                        }
                        if (!scope.maxWidth) {
                            scope.maxWidth = 99999;
                        }
                        return (width >= scope.minWidth && width <= scope.maxWidth);
                    };

                    $($window).on('resize', function () {
                        scope.$apply(function () {
                            scope.windowWidth = $($window).width();
                        });
                    });

                    scope.$watch(function () {
                            return scope.windowWidth;
                        },
                        function (width) {
                            // Load the sidebar template only if it will actually be displayed (meaning
                            // if the viewport has the right size). 'min-width' and 'max-width' should
                            // be the the same as in the less-layout, e.g, '@screen-md-min'.
                            if (!scope.loaded && isWithinBounds(width)) {
                                getTemplate(function (html) {
                                    element.html(html);
                                    element.replaceWith($compile(element.html())(scope));
                                    scope.loaded = true;
                                });
                            }
                        });
                };
                return {
                    restrict: 'E',
                    link: link,
                    scope: {
                        minWidth: '=?',
                        maxWidth: '=?'
                    }
                };
            }])
        /*
         * Directive for a navigation component.
         */
        .directive('appNav', ['$location', function ($location) {
            return {
                restrict: 'A',
                link: function (scope, element) {

                    var setActiveNav = function () {
                        angular.forEach(element.find('a'), function (a) {
                            if (a.href.substring(a.href.lastIndexOf('/')) === $location.path()) {
                                angular.element(a).parent('li').addClass('active');
                            } else {
                                angular.element(a).parent('li').removeClass('active');
                            }
                        });
                    };

                    scope.$on('$routeChangeSuccess', function () {
                        setActiveNav();
                    });

                    setActiveNav();
                }
            };
        }])
        /*
         * Template-directive for the header.
         */
        .directive('appHeader', ['appRevision', function (appRevision) {
            return {
                restrict: 'E',
                replace: true,
                templateUrl: 'static/partials/partial_header.html?v=' + appRevision
            };
        }]);
});
