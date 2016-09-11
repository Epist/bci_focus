(function(){
    angular.module('app.home')
        .controller('HomeCtrl', ['RESTService', '$scope', '$timeout', '$interval', HomeController]);

    var ctrl, rest;

    function HomeController(RESTService, $scope, $timeout, $interval) {
        ctrl = this;
        rest = RESTService;

        //        //timer with timeout
        //  $scope.timerWithTimeout = 0;
        //  $scope.startTimerWithTimeout = function() {
        //   $scope.timerWithTimeout = 0;
        //   if($scope.myTimeout){
        //     $timeout.cancel($scope.myTimeout);
        //   }
        //   $scope.onTimeout = function(){
        //       $scope.timerWithTimeout++;
        //       $scope.myTimeout = $timeout($scope.onTimeout,1000);
        //   };
        //   $scope.myTimeout = $timeout($scope.onTimeout,1000);
        // };
        //
        // $scope.resetTimerWithTimeout = function(){
        //   $scope.timerWithTimeout = 0;
        //   $timeout.cancel($scope.myTimeout);
        // };

        //timer with interval
        $scope.timerWithInterval = 0;
        $scope.running = false;
        $scope.startStopTimerWithInterval = function () {
            if (!$scope.running) {
                $scope.timerWithInterval = 0;
                if ($scope.myInterval) {
                    $interval.cancel($scope.myInterval);
                }
                $scope.onInterval = function () {
                    $scope.timerWithInterval++;
                };
                $scope.myInterval = $interval($scope.onInterval, 10);
                document.getElementById("startStop").innerHTML = "Stop BCI";
                $scope.running = true;

                //Need to add code to start the BCI instance

            } else {
                $interval.cancel($scope.myInterval);
                $scope.running = false;
                document.getElementById("startStop").innerHTML = "Start BCI";

                //Need to add the code to stop the BCI instance
            }


        };

        $scope.resetTimerWithInterval = function () {
            $scope.timerWithInterval = 0;
            $interval.cancel($scope.myInterval);
        };


    }


    // HomeController.prototype.getChallengeData = function(){
    //   var data;
    //   rest.get('/challenge')
    //     .then(function(response){
    //       console.log(response.data);
    //       data = response.data;
    //
    //       ctrl.user = {
    //         firstName: data.first_name,
    //         lastName: data.last_name
    //       };
    //
    //       ctrl.user.name = ctrl.user.firstName + ' ' + ctrl.user.lastName;
    //
    //       ctrl.startWeight = data.start_weight_in_lbs;
    //
    //       ctrl.weights = data.weights;
    //
    //       ctrl.activities = data.activities;
    //
    //       ctrl.alerts = data.alerts;
    //
    //     }, function(err){
    //       console.log(err);
    //     });
    // };

})();