/**
 * Blog.js
 */

define(['angular', 'showdown', 'showdownCodify', 'prettify', 'restangular'], function (angular, showdown) {
    'use strict';

    return angular.module('myApp.blog', ['restangular'])
        .controller('BlogCtrl', ['$rootScope', '$scope', '$routeParams', 'Restangular', function ($rootScope, $scope, $routeParams, Restangular) {
            $rootScope.title = 'Maximilian Fellner - Blog';

            $scope.getBlogPosts = function () {
                if (!angular.isDefined($scope.allBlogPosts)) {
                    $scope.allBlogPosts = Restangular.all('blog/posts').getList({format: 'full'}).$object;
                }
                return $scope.allBlogPosts;
            };
            $scope.onBlogPostClicked = function () {
                console.log('Clicked blog post #');
                $scope.post = {
                    id: '42',
                    title: 'Fuck!',
                    content: 'Fuuuuhuhuck!',
                    author: 'Steve',
                    time: '1989-08-14'
                };
            };
            $scope.getBlogPost = function () {
                if (!angular.isDefined($scope.post) && $routeParams.blogpost) {
                    var title = $routeParams.blogpost;
                    var id = title.substring(title.lastIndexOf('-') + 1);
                    $scope.post = Restangular.one('blog/posts', id).get({format: 'full'}).$object;
                }
                return $scope.post;
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
                templateUrl: '/static/partials/wdgt_blog_post.html?v=' + appRevision,
                scope: {
                    post: '='
                },
                link: function (scope) {
                    scope.$watch(function () {
                        return scope.post.content;
                    }, function (content) {
                        if (content) {
                            scope.post.html = convertMD(content);

                            require(['google-code-prettify'], function (pretty) {
                                pretty.prettyPrint();
                            });
                        }
                    });
                }
            };
        }]);
});
