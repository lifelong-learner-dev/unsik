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
            ajaxUrl = "http://127.0.0.1:8000/fitness_grade/male_adolescent_predict_ajax/";
        } else {
            // 웹 서버인 경우
            ajaxUrl = "http://18.180.43.72/fitness_grade/male_adolescent_predict_ajax/"; // 웹 서버의 실제 API 엔드포인트 URL로 대체해야 합니다.
        }

        // 사용자 입력 값 가져오기
        var sit_and_reach = parseInt($("#sit_and_reach").val()) || 0;
        var repeatedJumps = parseInt($("#repeated_jumps").val()) || 0;
        var shuttleRun = parseInt($("#shuttle_run").val()) || 0;
        var standingLongJump = parseInt($("#standing_long_jump").val()) || 0;
        var hangTime = parseFloat($("#hang_time").val()) || 0;

        if (sit_and_reach >= 37) {
            sit_and_reach_text = "🟢 당신의 앉아윗몸앞으로 굽히기 운동능력은 최상등급에 속합니다.";
        } else if (37 > sit_and_reach && sit_and_reach >= 13.9) {
            sit_and_reach_text = "🔵 당신의 앉아윗몸앞으로 굽히기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (13.9 > sit_and_reach && sit_and_reach >= 7.5) {
            sit_and_reach_text = "🟡 당신의 앉아윗몸앞으로 굽히기 운동능력은 평균보다 높습니다.";
        } else if (7.5 > sit_and_reach && sit_and_reach >= 1) {
            sit_and_reach_text = "🟠 당신의 앉아윗몸앞으로 굽히기 운동능력은 평균보다 낮습니다.";
        } else {
            sit_and_reach_text = "🔴 당신의 앉아윗몸앞으로 굽히기 운동능력은 하위 그룹 25%에 속합니다.";
        }


        if (repeatedJumps >= 80) {
            repeatedJumps_text = "🟢 당신의 반복점프 운동능력은 최상등급에 속합니다.";
        } else if (80 > repeatedJumps && repeatedJumps >= 52) {
            repeatedJumps_text = "🔵 당신의 반복점프 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (52 > repeatedJumps && repeatedJumps >= 46) {
            repeatedJumps_text = "🟡 당신의 반복점프 운동능력은 평균보다 높습니다.";
        } else if (46 > repeatedJumps && repeatedJumps >= 38) {
            repeatedJumps_text = "🟠 당신의 반복점프 운동능력은 평균보다 낮습니다.";
        } else {
            repeatedJumps_text = "🔴 당신의 반복점프 운동능력은 하위 그룹 25%에 속합니다.";
        }


        if (shuttleRun >= 99) {
            shuttleRun_text = "🟢 당신의 왕복오래달리기 운동능력은 최상등급에 속합니다.";
        } else if (99 > shuttleRun && shuttleRun >= 52) {
            shuttleRun_text = "🔵 당신의 왕복오래달리기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (52 > shuttleRun && shuttleRun >= 37) {
            shuttleRun_text = "🟡 당신의 왕복오래달리기 운동능력은 평균보다 높습니다.";
        } else if (37 > shuttleRun && shuttleRun >= 24) {
            shuttleRun_text = "🟠 당신의 왕복오래달리기 운동능력은 평균보다 낮습니다.";
        } else {
            shuttleRun_text = "🔴 당신의 왕복오래달리기 운동능력은 하위 그룹 25%에 속합니다.";
        }

        if (standingLongJump >= 305) {
            standingLongJump_text = "🟢 당신의 제자리 멀리뛰기 운동능력은 최상등급에 속합니다.";
        } else if (305 > standingLongJump && standingLongJump >= 217) {
            standingLongJump_text = "🔵 당신의 제자리 멀리뛰기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (217 > standingLongJump && standingLongJump >= 197) {
            standingLongJump_text = "🟡 당신의 제자리 멀리뛰기 운동능력은 평균보다 높습니다.";
        } else if (197 > standingLongJump && standingLongJump >= 173) {
            standingLongJump_text = "🟠 당신의 제자리 멀리뛰기 운동능력은 평균보다 낮습니다.";
        } else {
            standingLongJump_text = "🔴 당신의 제자리 멀리뛰기 운동능력은 하위 그룹 25%에 속합니다.";
        }

        if (hangTime >= 0.89) {
            hangTime_text = "🟢 당신의 체공시간 운동능력은 최상등급에 속합니다.";
        } else if (0.89 > hangTime && hangTime >= 0.589) {
            hangTime_text = "🔵 당신의 체공시간 굽히기 운동능력은 상위 그룹 25%에 속합니다.";
        } else if (0.589 > hangTime && hangTime >= 0.539) {
            hangTime_text = "🟡 당신의 체공시간 굽히기 운동능력은 평균보다 높습니다.";
        } else if (0.539 > hangTime && hangTime >= 0.489) {
            hangTime_text = "🟠 당신의 체공시간 굽히기 운동능력은 평균보다 낮습니다.";
        } else {
            hangTime_text = "🔴 당신의 체공시간 굽히기 운동능력은 하위 그룹 25%에 속합니다.";
        }

        const result_text_box = document.querySelector('.result-text-box');
        const resultText = document.createElement('div');
        resultText.classList.add('result-text');
        resultText.innerHTML = `
    <p style="text-align: left; margin-top: 10px;">${sit_and_reach_text}</p>
    <p style="text-align: left;">${repeatedJumps_text}</p>
    <p style="text-align: left;">${shuttleRun_text}</p>
    <p style="text-align: left;">${standingLongJump_text}</p>
    <p style="text-align: left;">${hangTime_text}</p>
    <p style="text-align: right;">(체력데이터 출처: 국민체육진흥공단)</p>
  `;
        result_text_box.appendChild(resultText);

        sit_and_reach = ((sit_and_reach / 37) * 100)
        if (sit_and_reach > 100) {
            sit_and_reach = 100;
        } else if (sit_and_reach == 0) {
            sit_and_reach = 25;
        }
        repeatedJumps = ((repeatedJumps / 80) * 100)
        if (repeatedJumps > 100) {
            repeatedJumps = 100;
        }
        shuttleRun = ((shuttleRun / 99) * 100)
        if (shuttleRun > 100) {
            shuttleRun = 100;
        }
        standingLongJump = ((standingLongJump / 305) * 100)
        if (standingLongJump > 100) {
            standingLongJump = 100;
        }
        hangTime = ((hangTime / 0.89) * 100)
        if (hangTime > 100) {
            hangTime = 100;
        }


        console.log(sit_and_reach);
        console.log(repeatedJumps);
        console.log(shuttleRun);
        console.log(standingLongJump);
        console.log(hangTime);

        // 차트 데이터 생성 및 업데이트
        updateCharts({
            sit_and_reach: sit_and_reach,
            repeatedJumps: repeatedJumps,
            shuttleRun: shuttleRun,
            standingLongJump: standingLongJump,
            hangTime: hangTime
        });

        function updateCharts(data) {
            // 차트 데이터 생성 및 업데이트
            var chartData = [
                data.sit_and_reach,
                data.repeatedJumps, // 반복점프
                data.shuttleRun, // 왕복오래달리기
                data.standingLongJump, // 제자리 멀리뛰기
                data.hangTime, // 체공시간

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
                labels: ['앉아윗몸앞으로 굽히기', '반복점프', '왕복오래달리기', '제자리 멀리뛰기', '체공시간'],
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