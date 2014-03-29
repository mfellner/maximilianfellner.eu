/**
 * Admin.js
 */

define(['angular', 'restangular', 'bootstrap'], function (angular) {
    'use strict';

    return angular.module('myApp.admin', [])
        /*
         * Main controller for /admin route.
         */
        .controller('AdminCtrl', ['$rootScope', '$scope', '$cookieStore', 'authService', 'Restangular', 'base64',
            function ($rootScope, $scope, $cookieStore, authService, Restangular, base64) {
                $rootScope.title = 'Maximilian Fellner - Admin';

                Restangular.addFullRequestInterceptor(function (element, operation, what, url, headers, params) {
                    var request = {headers: headers, params: params, element: element};
                    var token = $cookieStore.get('auth_token');
                    if (token != undefined)
                        request.headers.Authorization = 'Basic ' + base64.encode(token + ':undefined');
                    return request;
                });

                // If we're not authorized this will cause a 401, prompting the login.
                // This is only for UX purposes, not security, because the API is secured on the backend.
                Restangular.all('admin').customGET('login').then(function () {
                    // If the controller is reloaded while the stored token is still valid, we don't
                    // need to log in and must set this variable 'true' in order to hide the dialog.
                    $scope.isAuthorized = true;
                });

                $scope.$watch('isAuthorized', function (authorized) {
                    if (authorized === true) {
                        // Populate page with list of blog posts.
                        $scope.allBlogPosts = Restangular.all('blog/posts').getList().$object;

                    } else {
                        $scope.allBlogPosts = [];
                    }
                });

                $scope.$on('pushNewPost', function (event, blogPost) {
                    $scope.allBlogPosts.push(blogPost);
                });

                $scope.$on('removePost', function (event, id) {
                    for (var i = 0; i < $scope.allBlogPosts.length; i++) {
                        if ($scope.allBlogPosts[i].id === id)
                            $scope.allBlogPosts.splice(i, 1);
                    }
                });

                $scope.$on('event:auth-loginRequired', function () {
                    $cookieStore.remove('auth_token'); // $cookies don't support expiration yet...
                    $scope.isAuthorized = false;
                });

                $scope.$on('event:auth-loginConfirmed', function (event, token) {
                    $cookieStore.put('auth_token', token);
                    $scope.isAuthorized = true;
                });
            }])
        /*
         * Controller for blog post panel directive.
         */
        .controller('BlogPostPanelCtrl', ['$scope', '$timeout', 'Restangular', function ($scope, $timeout, Restangular) {
            var ctrl = this;

            ctrl.toggleOpen = function () {
                $scope.isOpen = !$scope.isOpen;
            };

            ctrl.resetForm = function () {
                // We defer the reset of the form because Twitter Bootstrap must reset
                // the loading button first, otherwise the button won't be disabled.
                $timeout(function () {
                    $scope.blogPostForm.$setPristine();
                    if ($scope.isNewPost()) $scope.blogPost = {};
                }, 100);
            };

            ctrl.cancel = function () {
                $scope.alerts = [];
                $scope.isOpen = false;
                $scope.isSaving = false;
                $scope.isLoading = false;
                $scope.isDeleting = false;
            };

            ctrl.addAlert = function (alert) {
                if (angular.isDefined($scope.alerts)) {
                    $scope.alerts.push(alert);
                } else {
                    $scope.alerts = [alert];
                }
            };

            $scope.closeAlert = function (i) {
                $scope.alerts.splice(i, 1);
            };

            $scope.isNewPost = function () {
                return !angular.isDefined($scope.blogPost) || !($scope.blogPost.id > 0);
            };

            $scope.isInputInvalid = function (input) {
                return $scope.blogPostForm.$dirty && input === undefined;
            };

            $scope.onTitleButtonClicked = function () {
                ctrl.toggleOpen();
                if (!$scope.isOpen) {
                    ctrl.cancel();
                    ctrl.resetForm();
                }
            };

            $scope.onEditButtonClicked = function () {
                if ($scope.isOpen) {
                    ctrl.cancel();
                    ctrl.resetForm();
                } else {
                    $scope.isLoading = true;

                    Restangular.one('blog/posts', $scope.blogPost.id).get({format: 'full'})
                        .then(function (response) {
                            $scope.blogPost = response;
                        })
                        .catch(function (err) {
                            var message = 'Could not load post. ' + '(' + (err.data.data || err.status) + ')';
                            ctrl.addAlert({title: 'Error!', message: message, type: 'danger'});
                        })
                        .finally(function () {
                            $scope.isOpen = true;
                            $scope.isLoading = false;
                        });
                }
            };

            $scope.onSaveButtonClicked = function () {
                $scope.isSaving = true;

                if ($scope.isNewPost()) {
                    // Create a new blog post with POST.
                    Restangular.all('blog/posts').post($scope.blogPost)
                        .then(function (response) {
                            $scope.isOpen = false;
                            $scope.$emit('pushNewPost', response);
                            ctrl.resetForm();
                        })
                        .catch(function (err) {
                            var message = 'Could not create post. ' + '(' + (err.data.data || err.status) + ')';
                            ctrl.addAlert({title: 'Error!', message: message, type: 'danger'});
                        })
                        .finally(function () {
                            $scope.isSaving = false;
                        });
                } else {
                    // Edit an existing blog post with PUT.
                    var blogPost = {};

                    if ($scope.blogPostForm.blogPostAuthor.$dirty)
                        blogPost.author = $scope.blogPost.author;
                    if ($scope.blogPostForm.blogPostTitle.$dirty)
                        blogPost.title = $scope.blogPost.title;
                    if ($scope.blogPostForm.blogPostContent.$dirty)
                        blogPost.content = $scope.blogPost.content;
                    if ($scope.blogPost.updateTime === true)
                        blogPost.time = true;

                    Restangular.one('blog/posts', $scope.blogPost.id).customPUT(blogPost)
                        .then(function (response) {
                            $scope.isOpen = false;
                            $scope.blogPost = response;
                            ctrl.resetForm();
                        })
                        .catch(function (err) {
                            var message = 'Could not update post. ' + '(' + (err.data.data || err.status) + ')';
                            ctrl.addAlert({title: 'Error!', message: message, type: 'danger'});
                        })
                        .finally(function () {
                            $scope.isSaving = false;
                        });
                }
            };

            $scope.onDeleteButtonClicked = function () {
                $scope.isDeleting = true;
                Restangular.one('blog/posts', $scope.blogPost.id).remove()
                    .then(function () {
                        $scope.isOpen = false;
                        $scope.$emit('removePost', $scope.blogPost.id);
                        // Do not reset form because the whole panel will be removed.
                    })
                    .catch(function (err) {
                        var message = 'Could not delete post. ' + '(' + (err.data.data || err.status) + ')';
                        ctrl.addAlert({title: 'Error!', message: message, type: 'danger'});
                    })
                    .finally(function () {
                        $scope.isDeleting = false;
                    });
            };

            $scope.onCancelButtonClicked = function () {
                ctrl.cancel();
                ctrl.resetForm();
            };
        }])
        /*
         * Panel to create a new blog post or edit an existing one.
         */
        .directive('blogPostPanel', ['appRevision', function (appRevision) {
            return {
                restrict: 'E',
                replace: true,
                controller: 'BlogPostPanelCtrl',
                templateUrl: '/static/partials/wdgt_blog_post_panel.html?v=' + appRevision,
                scope: {
                    blogPost: '=?',
                    txtTitleButton: '=?'
                },
                link: function (scope, element) {
                    scope.$watch('isOpen', function (isOpen) {
                        if (isOpen === true) {
                            $(element).find('.collapse').collapse('show');
                        } else if (isOpen === false) {
                            $(element).find('.collapse').collapse('hide');
                        }
                    });
                }
            }
        }])
        /*
         * Login dialog Bootstrap modal.
         */
        .directive('loginModal', ['authService', 'Restangular', 'base64', 'appRevision', function (authService, Restangular, base64, appRevision) {
            return {
                restrict: 'E',
                replace: true,
                templateUrl: '/static/partials/wdgt_login_modal.html?v=' + appRevision,
                link: function (scope, element) {
                    scope.$watch('isAuthorized', function (authorized) {
                        if (authorized === true) {
                            $(element).modal({backdrop: 'static', show: false});
                            $(element).modal('hide');
                        } else if (authorized === false) {
                            $(element).modal({backdrop: 'static', show: true});
                            $(element).modal('show');
                        }
                    });

                    scope.onLoginButtonClicked = function () {
                        var f = this;
                        scope.isLoggingIn = true;

                        f.onLoginFailed = function () {
                            scope.loginFailed = true;
                            scope.loginForm.$setPristine();
                        };

                        f.onLoginSuccess = function () {
                            scope.loginFailed = false;
                            scope.username = undefined;
                            scope.password = undefined;
                            scope.loginForm.$setPristine();
                        };

                        var headers = {
                            Authorization: 'Basic ' + base64.encode(scope.username + ':' + scope.password)
                        };
                        // Ignore http auth interceptor for login in order to prevent replaying any failed attempts.
                        Restangular.all('admin/login').withHttpConfig({ignoreAuthModule: true})
                            .customPOST(/*elem*/null, /*path*/null, /*params*/null, headers)
                            .then(function (token) {
                                f.onLoginSuccess();
                                authService.loginConfirmed(/*arg for $broadcast*/token, /*configUpdater*/function (config) {
                                    // Update the auth header for the buffered (originally failed) request(s).
                                    config.headers.Authorization = 'Basic ' + base64.encode(token + ':none');
                                    return config;
                                });
                            })
                            .catch(function (err) {
                                f.onLoginFailed();
                            })
                            .finally(function () {
                                scope.isLoggingIn = false;
                            });
                    };
                }
            };
        }])
        /*
         * Bootstrap button with loading animation.
         */
        .directive('btnLoading', function () {
            return {
                restrict: 'A',
                link: function (scope, element, attrs) {
                    scope.$watch(function () {
                        return scope.$eval(attrs.btnLoading);
                    }, function (loading) {
                        if (loading === true)
                            $(element).button('loading');
                        else if (loading === false)
                            $(element).button('reset');
                    });
                }
            };
        })
        /*
         * Bootstrap alert.
         */
        .directive('bsAlert', ['appRevision', function (appRevision) {
            return {
                restrict: 'E',
                replace: true,
                templateUrl: '/static/partials/wdgt_alert.html?v=' + appRevision,
                scope: {
                    type: '=',
                    close: '&',
                    title: '=',
                    message: '='
                }
            };
        }]);
});
