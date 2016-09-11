(function () {
  'use strict';

  angular.module('app', [
    'templates-app',
    'templates-common',
    'app.home',
    'app.about',
    'ui.router'
  ])

    .config(function myAppConfig($stateProvider, $urlRouterProvider) {
      $urlRouterProvider.otherwise('/home');
      $stateProvider
        .state('root', {
          url: '', 
          abstract: true, 
          views: {

          }
        });
    })

    .run(function run() {
    })

    .constant('API_URL', 'https://interactionservice-staging.ejenta.com/')

    .controller('AppCtrl', function AppCtrl($scope, $location) {
      // $scope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
      //   if (angular.isDefined(toState.data.pageTitle)) {
      //     $scope.pageTitle = toState.data.pageTitle + ' | Ejenta';
      //   }
      // });
    });

})();