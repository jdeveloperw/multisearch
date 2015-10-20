'use strict';

// Declare app level module which depends on views, and components
angular.module('multisearch', ["isteven-multi-select", "angular-underscore"])
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
.controller('SearchController', ["$scope", "siteFactory", "searchFactory", function($scope, siteFactory, searchFactory) {
  $scope.searchInProgress = false;
  
  siteFactory.getAll()
    .then(function successCallback(response) {
      $scope.availableSites = $scope.map(response.data, function(site) {
        return $scope.extend({"selected": true}, site);
      });
    }, function errorCallback(response) {
      alert(response);
    });
  
  $scope.search = function() {
    $scope.results = {}
    $scope.each($scope.selectedSites, function(site) {
      searchFactory.search(site.id, $scope.query)
        .then(function successCallback(response) {
          $scope.results[site.id] = $scope.map(response.data, function(raw_result) {
            var result = $scope.extend({}, raw_result);
            result["title"] = result["title"] || "Go";
            return result;
          });
        }, function errorCallback(response) {
          alert(response);
        });
    });
  };
}])
;