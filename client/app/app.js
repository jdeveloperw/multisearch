'use strict';

// Declare app level module which depends on views, and components
angular.module('multisearch', [
])
.controller('SearchController', ["$scope", function($scope) {
  $scope.search = function() {
    $scope.results = $scope.query;
  };
}]);
