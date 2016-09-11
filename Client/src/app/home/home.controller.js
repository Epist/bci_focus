(function () {
    angular.module('app.home')
        .controller('HomeCtrl', ['RESTService', '$scope', '$timeout', '$interval', HomeController]);

    var ctrl, rest, chart;

    function HomeController(RESTService, $scope, $timeout, $interval) {
        ctrl = this;
        rest = RESTService;

        //timer with interval
        $scope.timerWithInterval = 0;
        $scope.running = false;
        $scope.concentration = 80;
        $scope.isDisplayStreaming = false;
        $scope.isStreamRunning = false;

        $scope.mockData = [9.123476491040168890e-01, 9.208205958773957311e-01, 8.789335128510920025e-01, 9.107125468002098545e-01, 9.178983484539866566e-01, 8.891749212821938864e-01, 8.727452779687814299e-01, 8.966359791087173958e-01, 8.833053672639560316e-01, 8.876122843773018856e-01, 8.874093117196132363e-01, 8.868003100503120129e-01, 8.996695637314912064e-01, 8.709350130902400178e-01, 8.716567851773522335e-01, 8.546265874893658188e-01, 8.735240135430311081e-01, 8.572441691470482628e-01, 8.721770400415105318e-01, 8.438405000321698157e-01, 8.421774514036919346e-01, 8.457853570297018120e-01, 8.093400938029233771e-01, 8.112102832260273955e-01, 7.930060455781410278e-01, 7.624934446860337500e-01, 7.464773632334651410e-01, 7.167815210287221683e-01, 6.996472800952165949e-01, 6.776144266160259999e-01, 6.450599599596150702e-01, 6.242518265528511634e-01, 6.303626529827687230e-01, 5.895614431394654575e-01, 5.562321174990612072e-01, 5.248215635846509297e-01, 5.095580623843528612e-01, 4.796056796870948880e-01, 4.994461185160902206e-01, 4.837680384985213466e-01, 4.586990985319139846e-01, 4.529764811028964555e-01, 4.304921327751907723e-01, 5.570608464821389383e-01, 6.609586576290050752e-01, 6.485535185732630437e-01, 7.125428078507171081e-01, 7.613598992404403409e-01, 8.236601667590093268e-01, 8.543735760555806191e-01, 8.418934473185164524e-01, 8.574195972680135336e-01, 8.652168750632681649e-01, 8.354202038427361865e-01, 8.504714317037376237e-01, 8.697754303971967360e-01, 8.400596814561079873e-01, 8.339544302995457459e-01, 8.566102075640581459e-01, 8.502619774692494747e-01, 8.406822568308824906e-01];

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
                    if ($scope.timerWithInterval == 3000) {
                        $scope.playAlert();
                    }
                };
                $scope.myInterval = $interval($scope.onInterval, 10);
                document.getElementById("startStop").innerHTML = "Stop BCI";
                $scope.running = true;

                $scope.showStreamDisplay();
                $scope.startStreamDisplay();

                //Need to add code to start the BCI instance

            } else {
                $interval.cancel($scope.myInterval);
                $scope.running = false;
                document.getElementById("concentrationScore").innerHTML = '';
                document.getElementById("startStop").innerHTML = "Start BCI";

                $scope.stopStreamDisplay();
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

        $scope.playAlert = function () {
            var audio = new Audio('/assets/focus_alert.mp3');
            audio.play();
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