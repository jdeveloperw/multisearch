'use strict';

// Declare app level module which depends on views, and components
angular.module('multisearch', ["isteven-multi-select", "angular-underscore", "ngNotificationsBar", "ngSanitize"])
// Service wrapping the /search endpoint of the API
.factory('searchFactory', ['$http', function($http) {
  
  var urlBase = 'https://multisearch-server-jdeveloperw.c9.io/search/';
  
  var searchFactory = {};
  
  searchFactory.search = function(site_id, term) {
      return $http.get(urlBase + site_id + "?term=" + term);
  };
  
  return searchFactory;
}])
// Service wrapping the /site endpoint of the API
.factory('siteFactory', ['$http', function($http) {
  /*
    I could use $resource here instead; but since all I want to do is list all
    of the sites, $http is simpler.
  */
  
  var url = 'https://multisearch-server-jdeveloperw.c9.io/site/';
  
  var siteFactory = {};
  
  siteFactory.getAll = function() {
      return $http.get(url);
  };
  
  return siteFactory;
}])
.controller('SearchController', ["$scope", "$window", "$location", "notifications", "siteFactory", "searchFactory",
                                 function($scope, $window, $location, notifications, siteFactory, searchFactory) {
  
  // Query the server search API for the given site IDs and the term in the search box
  var search = function(siteIds) {
    // Set the URL params so they will be preserved on refresh
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
  // We may have zero, one, or multiple site IDs; make sure we convert to a list
  var rawSiteIds = $location.search()["site"]
  if (rawSiteIds && $scope.isArray(rawSiteIds)) {
    $scope.initialSiteIds = rawSiteIds;
  } else if (rawSiteIds) {
    $scope.initialSiteIds = [rawSiteIds];
  } else {
    $scope.initialSiteIds = [];
  }
  
  // Initialize by getting the list of all sites that are supported
  siteFactory.getAll()
    .then(function successCallback(response) {
      
      // Create a mapping from Site ID (e.g. twitter) to the Site Label (e.g. Twitter)
      $scope.siteIdToSiteLabel = {}
      $scope.each(response.data, function(site) {
        $scope.siteIdToSiteLabel[site.id] = site.label;
      });
      
      // Create multi-select for all available sites
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