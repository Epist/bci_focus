(function () {
    'use strict';

    angular.module('app.home')
        .directive('livestreamChart', ['livestreamService', LineChart]);


    var livestreamService, chart, linkFn, running, mockData, i, currData;


    function LineChart(livestream) {
        livestreamService = livestream;
        return {
            restrict: 'E',
            template: '<div id="hcContainer"></div>',
            replace: true,
            link: LineChartLinkFn
        };
    }

    function LineChartLinkFn(scope, element, attr) {
        linkFn = this;
        running = scope.getIsStreamRunning;
        currData = scope.incrementAndGetCurrentData;
        mockData = scope.mockData;
        i = 0;
        console.log(running);

        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'hcContainer',
                defaultSeriesType: 'spline',
                events: {
                    load: requestData
                }
            },
            title: {
                text: ''
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150,
                maxZoom: 20 * 1000
            },
            yAxis: {
                minPadding: 0.2,
                maxPadding: 0.2,
                minRange: 0,
                maxRange: 1,
                title: {
                    text: 'Concentration %',
                    margin: 80
                }
            },
            series: [{
                showInLegend: false,
                name: 'Concentration Values',
                data: []
            }]
        });

        // livestreamService.createConnection();
    }

    function requestData() {
        console.log('reached', running());

        if (!!chart && running()) {
            var series = chart.series[0],
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20
            if(i >= mockData.length){
                i = mockData.length - 2;
            }

            var point = [Date.now(), currData()];


            // add the point
            chart.series[0].addPoint(point, true, shift);
        }

        setTimeout(requestData, 1000);

    }

})();
