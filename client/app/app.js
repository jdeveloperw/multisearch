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
.factory('siteFactory', ['$http', function($http) {
  /*
    I could use $resource here instead; but since all I want to do is list all
    of the sites, $http is simpler.
  */
  
  var urlBase = 'https://multisearch-server-jdeveloperw.c9.io/site/';
  
  var siteFactory = {};
  
  siteFactory.getAll = function() {
      return $http.get(urlBase);
  };
  
  return siteFactory;
}])
.controller('SearchController', ["$scope", "siteFactory", "searchFactory", function($scope, siteFactory, searchFactory) {
  $scope.searchInProgress = false;
  
  siteFactory.getAll()
    .then(function successCallback(response) {
      $scope.sites = response.data;
    }, function errorCallback(response) {
      alert(response)
    });
  
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