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
            ajaxUrl = "http://127.0.0.1:8000/fitness_grade/male_senior_predict_ajax/";
        } else {
            // 웹 서버인 경우
            ajaxUrl = "http://18.180.43.72/fitness_grade/male_senior_predict_ajax/"; // 웹 서버의 실제 API 엔드포인트 URL로 대체해야 합니다.
        }


        // 사용자 입력 값 가져오기

        var sit_and_reach = parseInt($("#sit_and_reach").val()) || 0;
        var chair_stand_test = parseInt($("#chair_stand_test").val()) || 0;
        var two_minute_step_test = parseInt($("#two_minute_step_test").val()) || 0;
        var grip_strength_left = parseInt($("#grip_strength_left").val()) || 0;
        var grip_strength_right = parseFloat($("#grip_strength_right").val()) || 0;

        if (sit_and_reach >= 31.1) {
            sit_and_reach_text = "🟢 당신의 앉아윗몸앞으로 굽히기 운동능력은 최상등급에 속합니다.";
        } else if (31.1 > sit_and_reach && sit_and_reach >= 11.7) {
            sit_and_reach_text = "🔵 당신의 앉아윗몸앞으로 굽히기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (11.7 > sit_and_reach && sit_and_reach >= 6.1) {
            sit_and_reach_text = "🟡 당신의 앉아윗몸앞으로 굽히기 운동능력은 평균보다 높습니다.";
        } else if (6.1 > sit_and_reach && sit_and_reach >= 0.8) {
            sit_and_reach_text = "🟠 당신의 앉아윗몸앞으로 굽히기 운동능력은 평균보다 낮습니다.";
        } else {
            sit_and_reach_text = "🔴 당신의 앉아윗몸앞으로 굽히기 운동능력은 하위 그룹 25%에 속합니다.";
        }


        if (chair_stand_test >= 41) {
            chair_stand_test_text = "🟢 당신의 의자에앉았다일어서기 운동능력은 최상등급에 속합니다.";
        } else if (41 > chair_stand_test && chair_stand_test >= 28) {
            chair_stand_test_text = "🔵 당신의 의자에앉았다일어서기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (28 > chair_stand_test && chair_stand_test >= 24) {
            chair_stand_test_text = "🟡 당신의 의자에앉았다일어서기 운동능력은 평균보다 높습니다.";
        } else if (24 > chair_stand_test && chair_stand_test >= 20) {
            chair_stand_test_text = "🟠 당신의 의자에앉았다일어서기 운동능력은 평균보다 낮습니다.";
        } else {
            chair_stand_test_text = "🔴 당신의 의자에앉았다일어서기 운동능력은 하위 그룹 25%에 속합니다.";
        }

        if (two_minute_step_test >= 170) {
            two_minute_step_test_text = "🟢 당신의 2분제자리걷기 운동능력은 최상등급에 속합니다.";
        } else if (170 > two_minute_step_test && two_minute_step_test >= 125) {
            two_minute_step_test_text = "🔵 당신의 2분제자리걷기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (125 > two_minute_step_test && two_minute_step_test >= 114) {
            two_minute_step_test_text = "🟡 당신의 2분제자리걷기 운동능력은 평균보다 높습니다.";
        } else if (114 > two_minute_step_test && two_minute_step_test >= 104) {
            two_minute_step_test_text = "🟠 당신의 2분제자리걷기 운동능력은 평균보다 낮습니다.";
        } else {
            two_minute_step_test_text = "🔴 당신의 2분제자리걷기 운동능력은 하위 그룹 25%에 속합니다.";
        }


        if (grip_strength_left >= 52.2) {
            grip_strength_left_text = "🟢 당신의 왼쪽 악력 운동능력은 최상등급에 속합니다.";
        } else if (52.2 > grip_strength_left && grip_strength_left >= 37.5) {
            grip_strength_left_text = "🔵 당신의 왼쪽 악력 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (37.5 > grip_strength_left && grip_strength_left >= 33.5) {
            grip_strength_left_text = "🟡 당신의 왼쪽 악력 운동능력은 평균보다 높습니다.";
        } else if (33.5 > grip_strength_left && grip_strength_left >= 29.5) {
            grip_strength_left_text = "🟠 당신의 왼쪽 악력 운동능력은 평균보다 낮습니다.";
        } else {
            grip_strength_left_text = "🔴 당신의 왼쪽 악력 운동능력은 하위 그룹 25%에 속합니다.";
        }


        if (grip_strength_right >= 54.2) {
            grip_strength_right_text = "🟢 당신의 오른쪽 악력 운동능력은 최상등급에 속합니다.";
        } else if (54.2 > grip_strength_right && grip_strength_right >= 39.2) {
            grip_strength_right_text = "🔵 당신의 오른쪽 악력 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (39.2 > grip_strength_right && grip_strength_right >= 35.1) {
            grip_strength_right_text = "🟡 당신의 오른쪽 악력 운동능력은 평균보다 높습니다.";
        } else if (35.1 > grip_strength_right && grip_strength_right >= 31) {
            grip_strength_right_text = "🟠 당신의 오른쪽 악력 운동능력은 평균보다 낮습니다.";
        } else {
            grip_strength_right_text = "🔴 당신의 오른쪽 악력 운동능력은 하위 그룹 25%에 속합니다.";
        }

        const result_text_box = document.querySelector('.result-text-box');
        const resultText = document.createElement('div');
        resultText.classList.add('result-text');
        resultText.innerHTML = `
    <p style="text-align: left; margin-top: 10px;">${sit_and_reach_text}</p>
    <p style="text-align: left;">${chair_stand_test_text}</p>
    <p style="text-align: left;">${two_minute_step_test_text}</p>
    <p style="text-align: left;">${grip_strength_left_text}</p>
    <p style="text-align: left;">${grip_strength_right_text}</p>
    <p style="text-align: right;">(체력데이터 출처: 국민체육진흥공단)</p>
  `;
        result_text_box.appendChild(resultText);

        sit_and_reach = ((sit_and_reach / 31.1) * 100)
        if (sit_and_reach > 100) {
            sit_and_reach = 100;
        } else if (sit_and_reach == 0) {
            sit_and_reach = 25;
        }
        chair_stand_test = ((chair_stand_test / 41) * 100)
        if (chair_stand_test > 100) {
            chair_stand_test = 100;
        }
        grip_strength_left = ((grip_strength_left / 52.2) * 100)
        if (grip_strength_left > 100) {
            grip_strength_left = 100;
        }
        two_minute_step_test = ((two_minute_step_test / 170) * 100)
        if (two_minute_step_test > 100) {
            two_minute_step_test = 100;
        }
        grip_strength_right = ((grip_strength_right / 54.2) * 100)
        if (grip_strength_right > 100) {
            grip_strength_right = 100;
        }


        // 차트 데이터 생성 및 업데이트
        updateCharts({
            sit_and_reach: sit_and_reach,
            chair_stand_test: chair_stand_test,
            two_minute_step_test: two_minute_step_test,
            grip_strength_left: grip_strength_left,
            grip_strength_right: grip_strength_right
        });

        function updateCharts(data) {
            // 차트 데이터 생성 및 업데이트
            var chartData = [
                data.sit_and_reach,
                data.chair_stand_test,
                data.two_minute_step_test,
                data.grip_strength_left,
                data.grip_strength_right,
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
                labels: ['앉아윗몸앞으로 굽히기', '의자에앉았다일어서기', '2분제자리걷기', '악력_좌', '악력_우'],
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