(function () {
    'use strict';

    angular.module('app.home')
        .directive('livestreamChart', ['livestreamService', LineChart]);


    var livestreamService, chart, linkFn;

    function LineChart(livestream) {
        livestreamService = livestream;
        return {
            restrict: 'E',
            template: '<div id="container"></div>',
            scope: {
                weights: '='
            },
            link: LineChartLinkFn
        };
    }

    function LineChartLinkFn(scope, element) {
        linkFn = this;
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'container',
                defaultSeriesType: 'spline',
                events: {
                    load: requestData
                }
            },
            title: {
                text: 'Live random data'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150,
                maxZoom: 20 * 1000
            },
            yAxis: {
                minPadding: 0.2,
                maxPadding: 0.2,
                title: {
                    text: 'Value',
                    margin: 80
                }
            },
            series: [{
                name: 'Random data',
                data: []
            }]
        });

        // livestreamService.createConnection();
    }

    function requestData() {

        if (!!chart) {

            console.log('reached');
            var series = chart.series[0],
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20
            var point = [Date.now(), Math.random()];

            // add the point
            chart.series[0].addPoint(point, true, shift);

            console.log(chart.series[0].data);
        }
        setTimeout(requestData, 1000);
    }

})();
