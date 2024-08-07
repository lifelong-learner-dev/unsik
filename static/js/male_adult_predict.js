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
            ajaxUrl = "http://127.0.0.1:8000/fitness_grade/male_adult_predict_ajax/";
        } else {
            // 웹 서버인 경우
            ajaxUrl = "http://18.180.43.72/fitness_grade/male_adult_predict_ajax/"; // 웹 서버의 실제 API 엔드포인트 URL로 대체해야 합니다.
        }


        var crossover_situp = parseInt($("#crossover_situp").val()) || 0;
        var sit_and_reach = parseInt($("#sit_and_reach").val()) || 0;
        var standingLongJump = parseInt($("#standing_long_jump").val()) || 0;
        var step_test_output = parseInt($("#step_test_output").val()) || 0;
        var grip_strength_left = parseInt($("#grip_strength_left").val()) || 0;
        var grip_strength_right = parseFloat($("#grip_strength_right").val()) || 0;

        if (crossover_situp >= 78) {
            crossover_situp_text = "🟢 당신의 교차윗몸일으키기 운동능력은 최상등급에 속합니다.";
        } else if (78 > crossover_situp && crossover_situp >= 50) {
            crossover_situp_text = "🔵 당신의 교차윗몸일으키기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (50 > crossover_situp && crossover_situp >= 42) {
            crossover_situp_text = "🟡 당신의 교차윗몸일으키기 운동능력은 평균보다 높습니다.";
        } else if (42 > crossover_situp && crossover_situp >= 33) {
            crossover_situp_text = "🟠 당신의 교차윗몸일으키기 운동능력은 평균보다 낮습니다.";
        } else {
            crossover_situp_text = "🔴 당신의 교차윗몸일으키기 운동능력은 하위 그룹 25%에 속합니다.";
        }

        if (sit_and_reach >= 35.2) {
            sit_and_reach_text = "🟢 당신의 앉아윗몸앞으로 굽히기 운동능력은 최상등급에 속합니다.";
        } else if (35.2 > sit_and_reach && sit_and_reach >= 16.2) {
            sit_and_reach_text = "🔵 당신의 앉아윗몸앞으로 굽히기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (16.2 > sit_and_reach && sit_and_reach >= 11.2) {
            sit_and_reach_text = "🟡 당신의 앉아윗몸앞으로 굽히기 운동능력은 평균보다 높습니다.";
        } else if (11.2 > sit_and_reach && sit_and_reach >= 5.8) {
            sit_and_reach_text = "🟠 당신의 앉아윗몸앞으로 굽히기 운동능력은 평균보다 낮습니다.";
        } else {
            sit_and_reach_text = "🔴 당신의 앉아윗몸앞으로 굽히기 운동능력은 하위 그룹 25%에 속합니다.";
        }


        if (step_test_output >= 57.6) {
            step_test_output_text = "🟢 당신의 스텝검사출력(VO₂max) 운동능력은 최상등급에 속합니다.";
        } else if (57.6 > step_test_output && step_test_output >= 46.7) {
            step_test_output_text = "🔵 당신의 스텝검사출력(VO₂max) 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (46.7 > step_test_output && step_test_output >= 43.3) {
            step_test_output_text = "🟡 당신의 스텝검사출력(VO₂max) 운동능력은 평균보다 높습니다.";
        } else if (43.3 > step_test_output && step_test_output >= 39.4) {
            step_test_output_text = "🟠 당신의 스텝검사출력(VO₂max) 운동능력은 평균보다 낮습니다.";
        } else {
            step_test_output_text = "🔴 당신의 스텝검사출력(VO₂max) 운동능력은 하위 그룹 25%에 속합니다.";
        }


        if (grip_strength_left >= 63.1) {
            grip_strength_left_text = "🟢 당신의 왼쪽 악력 운동능력은 최상등급에 속합니다.";
        } else if (63.1 > grip_strength_left && grip_strength_left >= 46.1) {
            grip_strength_left_text = "🔵 당신의 왼쪽 악력 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (46.1 > grip_strength_left && grip_strength_left >= 41.4) {
            grip_strength_left_text = "🟡 당신의 왼쪽 악력 운동능력은 평균보다 높습니다.";
        } else if (41.4 > grip_strength_left && grip_strength_left >= 36.9) {
            grip_strength_left_text = "🟠 당신의 왼쪽 악력 운동능력은 평균보다 낮습니다.";
        } else {
            grip_strength_left_text = "🔴 당신의 왼쪽 악력 운동능력은 하위 그룹 25%에 속합니다.";
        }

        if (standingLongJump >= 295) {
            standingLongJump_text = "🟢 당신의 제자리 멀리뛰기 운동능력은 최상등급에 속합니다.";
        } else if (295 > standingLongJump && standingLongJump >= 228) {
            standingLongJump_text = "🔵 당신의 제자리 멀리뛰기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (228 > standingLongJump && standingLongJump >= 211) {
            standingLongJump_text = "🟡 당신의 제자리 멀리뛰기 운동능력은 평균보다 높습니다.";
        } else if (211 > standingLongJump && standingLongJump >= 190) {
            standingLongJump_text = "🟠 당신의 제자리 멀리뛰기 운동능력은 평균보다 낮습니다.";
        } else {
            standingLongJump_text = "🔴 당신의 제자리 멀리뛰기 운동능력은 하위 그룹 25%에 속합니다.";
        }

        if (grip_strength_right >= 67.2) {
            grip_strength_right_text = "🟢 당신의 오른쪽 악력 운동능력은 최상등급에 속합니다.";
        } else if (67.2 > grip_strength_right && grip_strength_right >= 49.1) {
            grip_strength_right_text = "🔵 당신의 오른쪽 악력 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (49.1 > grip_strength_right && grip_strength_right >= 44) {
            grip_strength_right_text = "🟡 당신의 오른쪽 악력 운동능력은 평균보다 높습니다.";
        } else if (44 > grip_strength_right && grip_strength_right >= 39.3) {
            grip_strength_right_text = "🟠 당신의 오른쪽 악력 운동능력은 평균보다 낮습니다.";
        } else {
            grip_strength_right_text = "🔴 당신의 오른쪽 악력 운동능력은 하위 그룹 25%에 속합니다.";
        }

        const result_text_box = document.querySelector('.result-text-box');
        const resultText = document.createElement('div');
        resultText.classList.add('result-text');
        resultText.innerHTML = `
    <p style="text-align: left; margin-top: 10px;">${crossover_situp_text}</p>
    <p style="text-align: left;">${sit_and_reach_text}</p>
    <p style="text-align: left;">${standingLongJump_text}</p>
    <p style="text-align: left;">${step_test_output_text}</p>
    <p style="text-align: left;">${grip_strength_left_text}</p>
    <p style="text-align: left;">${grip_strength_right_text}</p>
    <p style="text-align: right;">(체력데이터 출처: 국민체육진흥공단)</p>
  `;
        result_text_box.appendChild(resultText);

        crossover_situp = ((crossover_situp / 78) * 100)
        if (crossover_situp > 100) {
            crossover_situp = 100;
        }

        sit_and_reach = ((sit_and_reach / 35.2) * 100)
        if (sit_and_reach > 100) {
            sit_and_reach = 100;
        } else if (sit_and_reach == 0) {
            sit_and_reach = 25;
        }
        step_test_output = ((step_test_output / 57.6) * 100)
        if (step_test_output > 100) {
            step_test_output = 100;
        }
        grip_strength_left = ((grip_strength_left / 63.1) * 100)
        if (grip_strength_left > 100) {
            grip_strength_left = 100;
        }
        standingLongJump = ((standingLongJump / 295) * 100)
        if (standingLongJump > 100) {
            standingLongJump = 100;
        }
        grip_strength_right = ((grip_strength_right / 67.2) * 100)
        if (grip_strength_right > 100) {
            grip_strength_right = 100;
        }


        // 차트 데이터 생성 및 업데이트
        updateCharts({
            crossover_situp: crossover_situp,
            sit_and_reach: sit_and_reach,
            step_test_output: step_test_output,
            standingLongJump: standingLongJump,
            grip_strength_left: grip_strength_left,
            grip_strength_right: grip_strength_right
        });

        function updateCharts(data) {
            // 차트 데이터 생성 및 업데이트
            var chartData = [
                data.crossover_situp,
                data.sit_and_reach,
                data.standingLongJump,
                data.step_test_output,
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
                labels: ['교차윗몸일으키기', '앉아윗몸앞으로 굽히기', '제자리 멀리뛰기', '스텝검사출력', '악력_좌', '악력_우'],
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