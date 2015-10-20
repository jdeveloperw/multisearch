'use strict';

// Declare app level module which depends on views, and components
angular.module('multisearch', ["ngRoute", "isteven-multi-select", "angular-underscore"])
.config(function($routeProvider) {
})
.factory('searchFactory', ['$http', function($http) {
  
  var urlBase = 'https://multisearch-server-jdeveloperw.c9.io/search/';
  
  var searchFactory = {};
  
  searchFactory.search = function(site_id, term) {
      return $http.get(urlBase + site_id + "?term=" + term);
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
.controller('SearchController', ["$scope", "$window", "$location", "siteFactory", "searchFactory", function($scope, $window, $location, siteFactory, searchFactory) {
  
  var search = function(searchSites) {
    $location.search({"query": $scope.query});
    
    $scope.results = {}
    $scope.each(searchSites, function(site) {
      searchFactory.search(site.id, $scope.query)
        .then(function successCallback(response) {
          $scope.results[site.id] = response.data;
        }, function errorCallback(response) {
          $window.alert(response);
        });
    });
  };
  
  $scope.each($location.search(), function(value, key) {
    $scope[key] = value;
  });
  
  siteFactory.getAll()
    .then(function successCallback(response) {
      $scope.availableSites = $scope.map(response.data, function(site) {
        return $scope.extend({"selected": true}, site);
      });
  
      // Run initial search if we have query parameters in the URL
      if ($scope.query) {
        search($scope.availableSites); 
      };
    }, function errorCallback(response) {
      $window.alert(response);
    });
  
  $scope.search = function() {
    search($scope.selectedSites);
  };
}]);