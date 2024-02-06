$(document).ready(function () {
    $("#predict-form").submit(function (e) {
        e.preventDefault();
        const isLocalhost = Boolean(
            window.location.hostname === "localhost" ||

            window.location.hostname === "[::1]" ||

            window.location.hostname.match(
                /^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/
            )
        );

        let ajaxUrl = ""; // 이 변수에 API 엔드포인트 URL을 설정합니다.

        if (isLocalhost) {
            // 로컬 호스트인 경우
            ajaxUrl = "http://127.0.0.1:8000/fitness_grade/male_child_predict_ajax/";
        } else {
            // 웹 서버인 경우
            ajaxUrl = "http://18.180.43.72/fitness_grade/male_child_predict_ajax/"; // 웹 서버의 실제 API 엔드포인트 URL로 대체해야 합니다.
        }


        // 사용자 입력 값 가져오기
        var sit_and_reach = parseInt($("#sit_and_reach").val()) || 0;
        var sit_ups = parseInt($("#sit_ups").val()) || 0;
        var shuttleRun = parseInt($("#shuttle_run").val()) || 0;
        var standingLongJump = parseInt($("#standing_long_jump").val()) || 0;

        if (sit_and_reach >= 35) {
            sit_and_reach_text = "🟢 당신의 앉아윗몸앞으로 굽히기 운동능력은 최상등급에 속합니다.";
        } else if (35 > sit_and_reach && sit_and_reach >= 9.8) {
            sit_and_reach_text = "🔵 당신의 앉아윗몸앞으로 굽히기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (9.8 > sit_and_reach && sit_and_reach >= 5) {
            sit_and_reach_text = "🟡 당신의 앉아윗몸앞으로 굽히기 운동능력은 평균보다 높습니다.";
        } else if (5 > sit_and_reach && sit_and_reach >= 0) {
            sit_and_reach_text = "🟠 당신의 앉아윗몸앞으로 굽히기 운동능력은 평균보다 낮습니다.";
        } else {
            sit_and_reach_text = "🔴 당신의 앉아윗몸앞으로 굽히기 운동능력은 하위 그룹 25%에 속합니다.";
        }


        if (sit_ups >= 117) {
            sit_ups_text = "🟢 당신의 윗몸말아올리기 운동능력은 최상등급에 속합니다.";
        } else if (117 > sit_ups && sit_ups >= 40) {
            sit_ups_text = "🔵 당신의 윗몸말아올리기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (40 > sit_ups && sit_ups >= 26) {
            sit_ups_text = "🟡 당신의 윗몸말아올리기 운동능력은 평균보다 높습니다.";
        } else if (26 > sit_ups && sit_ups >= 16) {
            sit_ups_text = "🟠 당신의 윗몸말아올리기 운동능력은 평균보다 낮습니다.";
        } else {
            sit_ups_text = "🔴 당신의 윗몸말아올리기 운동능력은 하위 그룹 25%에 속합니다.";
        }


        if (shuttleRun >= 168) {
            shuttleRun_text = "🟢 당신의 왕복오래달리기 운동능력은 최상등급에 속합니다.";
        } else if (168 > shuttleRun && shuttleRun >= 72) {
            shuttleRun_text = "🔵 당신의 왕복오래달리기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (72 > shuttleRun && shuttleRun >= 50) {
            shuttleRun_text = "🟡 당신의 왕복오래달리기 운동능력은 평균보다 높습니다.";
        } else if (50 > shuttleRun && shuttleRun >= 31) {
            shuttleRun_text = "🟠 당신의 왕복오래달리기 운동능력은 평균보다 낮습니다.";
        } else {
            shuttleRun_text = "🔴 당신의 왕복오래달리기 운동능력은 하위 그룹 25%에 속합니다.";
        }

        if (standingLongJump >= 262) {
            standingLongJump_text = "🟢 당신의 제자리 멀리뛰기 운동능력은 최상등급에 속합니다.";
        } else if (262 > standingLongJump && standingLongJump >= 173) {
            standingLongJump_text = "🔵 당신의 제자리 멀리뛰기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (173 > standingLongJump && standingLongJump >= 155) {
            standingLongJump_text = "🟡 당신의 제자리 멀리뛰기 운동능력은 평균보다 높습니다.";
        } else if (155 > standingLongJump && standingLongJump >= 135) {
            standingLongJump_text = "🟠 당신의 제자리 멀리뛰기 운동능력은 평균보다 낮습니다.";
        } else {
            standingLongJump_text = "🔴 당신의 제자리 멀리뛰기 운동능력은 하위 그룹 25%에 속합니다.";
        }


        const result_text_box = document.querySelector('.result-text-box');
        const resultText = document.createElement('div');
        resultText.classList.add('result-text');
        resultText.innerHTML = `
    <p style="text-align: left; margin-top: 10px;">${sit_and_reach_text}</p>
    <p style="text-align: left;">${sit_ups_text}</p>
    <p style="text-align: left;">${standingLongJump_text}</p>
    <p style="text-align: left;">${shuttleRun_text}</p>
    <p style="text-align: right;">(체력데이터 출처: 국민체육진흥공단)</p>
  `;
        result_text_box.appendChild(resultText);

        sit_and_reach = ((sit_and_reach / 35) * 100)
        if (sit_and_reach > 100) {
            sit_and_reach = 100;
        }
        else if (sit_and_reach == 0) {
            sit_and_reach = 25;
        }
        sit_ups = ((sit_ups / 117) * 100)
        if (sit_ups > 100) {
            sit_ups = 100;
        }
        shuttleRun = ((shuttleRun / 168) * 100)
        if (shuttleRun > 100) {
            shuttleRun = 100;
        }
        standingLongJump = ((standingLongJump / 262) * 100)
        if (standingLongJump > 100) {
            standingLongJump = 100;
        }


        // 차트 데이터 생성 및 업데이트
        updateCharts({
            sit_and_reach: sit_and_reach,
            sit_ups: sit_ups,
            shuttleRun: shuttleRun,
            standingLongJump: standingLongJump
        });

        function updateCharts(data) {
            // 차트 데이터 생성 및 업데이트
            var chartData = [
                data.sit_and_reach,
                data.sit_ups, // 반복점프
                data.standingLongJump, // 제자리 멀리뛰기
                data.shuttleRun // 왕복오래달리기
            ];

            createPolarAreaChart('performanceChart', chartData);
        }

        $.ajax({
            type: 'POST',
            url: ajaxUrl,
            data: $(this).serialize(),

            success: function (response) {
                document.getElementById("predict-section").style.display = "none";
                document.getElementById("result-section").style.display = "block";
                console.log(response.class_name);
                $("#prediction_result").text("예측 결과: " + response.class_name);
                console.log(data)
                updateCharts(data);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
    function createPolarAreaChart(canvasId, chartData) {
        console.log(chartData)
        var ctx = document.getElementById(canvasId).getContext('2d');
        var chart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['앉아윗몸앞으로 굽히기', '윗몸말아올리기', '제자리 멀리뛰기', '왕복오래달리기'],
                datasets: [{
                    label: '나의 운동 능력치',
                    data: chartData,
                    backgroundColor: [
                        'rgba(153, 102, 255, 0.3)',
                    ],
                    borderColor: [
                        'rgba(153, 102, 255, 1)',
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    r: {
                        angleLines: {
                            display: false
                        },
                        suggestedMin: 10,
                        suggestedMax: 100
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            // This more specific font property overrides the global property
                            font: {
                                size: 17
                            }
                        }
                    }
                }
            }
        });
    }

});