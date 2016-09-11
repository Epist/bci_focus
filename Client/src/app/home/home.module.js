(function(){
  'use strict';
  angular.module( 'app.home', [
    'ui.router'
  ])
    
    .config(function config( $stateProvider ) {
      $stateProvider.state( 'root.home', {
        url: '/home',
        views: {
          "main@": {
            controller: 'HomeCtrl as ctrl',
            templateUrl: 'home/home.tpl.html'
          }
        },
        data:{ pageTitle: 'Home' }
      });
    })

  ;
  


})();