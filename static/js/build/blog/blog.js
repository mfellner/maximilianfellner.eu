/**
 * Blog.js
 */

define(['angular', 'showdown', 'prettify', 'sdCodify', 'restangular'], function (angular, showdown) {
    'use strict';

    return angular.module('myApp.blog', ['restangular'])
        .controller('BlogCtrl', ['$rootScope', '$scope', 'Restangular', function ($rootScope, $scope, Restangular) {
            $rootScope.title = 'Maximilian Fellner - Blog';

            Restangular.all('blog/posts').getList({format: 'full'}).then(function (posts) {
                $scope.allBlogPosts = posts;
            });
        }])
        .factory('convertMD', function () {
            var converter = new Showdown.converter({extensions: ['codify']});
            return function (markdown) {
                return converter.makeHtml(markdown);
            };
        })
        .directive('blogPost', ['$sanitize', 'convertMD', function ($sanitize, convertMD) {
            return {
                restrict: 'E',
                replace: true,
                templateUrl: 'static/partials/wdgt_blog_post.html',
                link: function (scope) {
                    scope.post.html = convertMD(scope.post.content);

                    require(['google-code-prettify'], function (pretty) {
                        pretty.prettyPrint();
                    });
                }
            };
        }]);
});
