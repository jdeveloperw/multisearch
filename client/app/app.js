'use strict';

// Declare app level module which depends on views, and components
angular.module('multisearch', ["ngRoute", "isteven-multi-select", "angular-underscore", "ngNotificationsBar", "ngSanitize"])
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
.controller('SearchController', ["$scope", "$window", "$location", "notifications", "siteFactory", "searchFactory",
                                 function($scope, $window, $location, notifications, siteFactory, searchFactory) {
  
  // Query the server search API for the given site IDs and the term in the search box
  var search = function(siteIds) {
    $location.search({"query": $scope.query, "site": siteIds});
    
    $scope.results = {}
    $scope.each(siteIds, function(siteId) {
      searchFactory.search(siteId, $scope.query)
        .then(function successCallback(response) {
          $scope.results[siteId] = {
            "label": $scope.siteIdToSiteLabel[siteId],
            "results": response.data
          };
        }, function errorCallback(response) {
          notifications.showError("Unable to fetch results for " + siteId);
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
      
      // Create a mapping from Site ID (e.g. twitter) to the Site Label (e.g. Twitter)
      $scope.siteIdToSiteLabel = {}
      $scope.each(response.data, function(site) {
        $scope.siteIdToSiteLabel[site.id] = site.label;
      });
      
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