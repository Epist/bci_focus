(function(){
  angular.module('app.home')
    .controller( 'HomeCtrl', ['RESTService', HomeController]);

  var ctrl, rest;

  function HomeController(RESTService){
    ctrl = this;
    rest = RESTService;

    ctrl.getChallengeData();
  }

  HomeController.prototype.getChallengeData = function(){
    var data;
    rest.get('/challenge')
      .then(function(response){
        console.log(response.data);
        data = response.data;

        ctrl.user = {
          firstName: data.first_name,
          lastName: data.last_name
        };

        ctrl.user.name = ctrl.user.firstName + ' ' + ctrl.user.lastName;

        ctrl.startWeight = data.start_weight_in_lbs;

        ctrl.weights = data.weights;

        ctrl.activities = data.activities;

        ctrl.alerts = data.alerts;

      }, function(err){
        console.log(err);
      });
  };

})();