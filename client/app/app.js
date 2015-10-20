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
  
  var search = function(siteIds) {
    $location.search({"query": $scope.query, "site": siteIds});
    
    $scope.results = {}
    $scope.each(siteIds, function(siteId) {
      searchFactory.search(siteId, $scope.query)
        .then(function successCallback(response) {
          $scope.results[siteId] = response.data;
        }, function errorCallback(response) {
          $window.alert(response);
        });
    });
  };
  
  // Set variables from URL parameters
  $scope.query = $location.search()["query"];
  var rawSiteIds = $location.search()["site"]
  if (rawSiteIds && $scope.isArray(rawSiteIds)) {
    $scope.initialSiteIds = rawSiteIds;
  } else if (rawSiteIds) {
    $scope.initialSiteIds = [rawSiteIds];
  } else {
    $scope.initialSiteIds = [];
  }
  
  siteFactory.getAll()
    .then(function successCallback(response) {
      $scope.availableSites = $scope.map(response.data, function(site) {
        var selected = !$scope.initialSiteIds || $scope.contains($scope.initialSiteIds, site.id);
        return $scope.extend({"selected": selected}, site);
      });
  
      // Run initial search if we have query parameters in the URL
      if ($scope.query) {
        search($scope.initialSiteIds); 
      };
    }, function errorCallback(response) {
      $window.alert(response);
    });
  
  $scope.search = function() {
    var siteIds = $scope.pluck($scope.selectedSites, "id");
    search(siteIds);
  };
}]);