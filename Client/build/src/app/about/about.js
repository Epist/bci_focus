(function(){
  'use strict';
  
  angular.module( 'app.about', [
    'ui.router',
    'placeholders',
    'ui.bootstrap'
  ])

    .config(["$stateProvider", function config( $stateProvider ) {
      $stateProvider.state( 'root.about', {
        url: '/about',
        views: {
          "main@": {
            controller: 'AboutCtrl as ctrl',
            templateUrl: 'about/about.tpl.html'
          }
        },
        data:{ pageTitle: 'What is It?' }
      });
    }])

    .controller( 'AboutCtrl', ["$scope", function AboutCtrl( $scope ) {
      // This is simple a demo for UI Boostrap.
      $scope.dropdownDemoItems = [
        "The first choice!",
        "And another choice for you.",
        "but wait! A third!"
      ];
    }]);

})();