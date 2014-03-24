/**
 * Blog.js
 */

define(['angular', 'showdown', 'showdownCodify', 'prettify', 'restangular'], function (angular, showdown) {
    'use strict';

    return angular.module('myApp.blog', ['restangular'])
        .controller('BlogCtrl', ['$rootScope', '$scope', '$window', 'Restangular', function ($rootScope, $scope, $window, Restangular) {
            $rootScope.title = 'Maximilian Fellner - Blog';

            Restangular.all('blog/posts').getList({format: 'full'}).then(function (posts) {
                $scope.allBlogPosts = posts;
            });
            $scope.windowWidth = function() {
                console.log('window width: ' + $($window).width());
                return $($window).width();
            };
        }])
        .factory('convertMD', function () {
            var converter = new showdown.converter({extensions: ['codify']});
            return function (markdown) {
                return converter.makeHtml(markdown);
            };
        })
        .directive('blogPost', ['$sanitize', 'convertMD', 'appRevision', function ($sanitize, convertMD, appRevision) {
            return {
                restrict: 'E',
                replace: true,
                templateUrl: 'static/partials/wdgt_blog_post.html?v=' + appRevision,
                link: function (scope) {
                    scope.post.html = convertMD(scope.post.content);

                    require(['google-code-prettify'], function (pretty) {
                        pretty.prettyPrint();
                    });
                }
            };
        }]);
});
