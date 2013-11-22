/**
 * Source.js
 */

define(['angular'], function (angular) {
    'use strict';

    return angular.module('myApp.source', [])
        .controller('SourceCtrl', ['$rootScope', '$scope', function ($rootScope, $scope) {
            $rootScope.title = 'Maximilian Fellner - Source';
            $scope.loremIpsum = 'Hello, source!';
        }]);
});
