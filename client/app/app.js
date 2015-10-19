'use strict';

// Declare app level module which depends on views, and components
angular.module('multisearch', [
])
.factory('searchFactory', ['$http', function($http) {

  var urlBase = 'http://localhost:8000/search/twitter?term=';
  
  var searchFactory = {};
  
  searchFactory.search = function(term) {
      return $http.get(urlBase + term);
  };
  
  return searchFactory;
}])
.controller('SearchController', ["$scope", "searchFactory", function($scope, searchFactory) {
  $scope.searchInProgress = false;
  
  $scope.search = function() {
    $scope.isSearchInProgress = true;
    searchFactory.search($scope.query)
      .success(function(value) {
        $scope.results = value;
        $scope.isSearchInProgress = false;
      })
      .error(function(error) {
        $scope.results = error;
        $scope.isSearchInProgress = false;
      });
  };
}])
;