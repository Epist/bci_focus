(function () {
    angular.module('app.home')
        .controller('HomeCtrl', ['RESTService', '$scope', '$timeout', '$interval', HomeController]);

    var ctrl, rest;

    function HomeController(RESTService, $scope, $timeout, $interval) {
        ctrl = this;
        rest = RESTService;

        //timer with interval
        $scope.timerWithInterval = 0;
        $scope.running = false;
        $scope.concentration = 80;
        $scope.isDisplayStreaming = false;
        $scope.isStreamRunning = false;

        $scope.startStopTimerWithInterval = function () {
            if (!$scope.running) {
                $scope.concentrationColor();
                document.getElementById("concentrationScore").innerHTML = $scope.concentration + '% Focused';
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
                document.getElementById("concentrationScore").innerHTML = '';
                document.getElementById("startStop").innerHTML = "Start BCI";


                //Need to add the code to stop the BCI instance
            }


        };

        $scope.resetTimerWithInterval = function () {
            $scope.timerWithInterval = 0;
            $interval.cancel($scope.myInterval);
        };

        //For coloring the concentration score
        $scope.concentrationColor = function () {
            if ($scope.concentration < 20) {
                document.getElementById("concentrationScore").style.color = "red";
            } else if ($scope.concentration < 50) {
                document.getElementById("concentrationScore").style.color = "yellow";
            } else {
                document.getElementById("concentrationScore").style.color = "green";
            }
        };


        $scope.showStreamDisplay = function () {
            $scope.isDisplayStreaming = true;
        };

        $scope.hideStreamDisplay = function () {
            $scope.isDisplayStreaming = false;
        };

        $scope.startStreamDisplay = function () {
            $scope.isStreamRunning = true;
        };

        $scope.stopStreamDisplay = function () {
            $scope.isStreamRunning = false;
        };

        $scope.getIsStreamRunning = function () {
            return $scope.isStreamRunning;
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