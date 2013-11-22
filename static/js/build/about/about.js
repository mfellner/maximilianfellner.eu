/**
 * About.js
 */

define(['angular'], function (angular) {
    'use strict';

    return angular.module('myApp.about', [])
        .controller('AboutCtrl', ['$rootScope', '$scope', function ($rootScope, $scope) {
            $rootScope.title = 'Maximilian Fellner - About';
            $scope.loremIpsum = 'Hello, about!';
        }]);
});
