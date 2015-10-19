'use strict';

// Declare app level module which depends on views, and components
angular.module('multisearch', [])
.factory('searchFactory', ['$http', function($http) {
  
  var urlBase = 'https://multisearch-server-jdeveloperw.c9.io/search/wikipedia?term=';
  
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
      .then(function successCallback(response) {
        $scope.results = response;
        $scope.isSearchInProgress = false;
      }, function errorCallback(response) {
        $scope.results = response;
        $scope.isSearchInProgress = false;
      });
  };
}])
;