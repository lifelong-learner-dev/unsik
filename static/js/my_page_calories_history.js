$(document).ready(function () {

    var ctx = document.getElementById('caloriesChart');
    var chart = new Chart(ctx, {
        type: 'bar', // 라인 차트 유형
        data: {
            labels: graph_dates, // x축 레이블로 날짜 사용
            datasets: [{
                label: '식사 칼로리', // 두 번째 데이터셋의 레이블
                backgroundColor: 'rgba(54, 162, 235, 0.2)', // 그래프 내부 색
                borderColor: 'rgba(54, 162, 235, 1)', // 선 색
                borderWidth: 1,
                data: graph_meal_calories, // 두 번째 데이터셋의 데이터
            },
            {
                label: '운동 칼로리', // 세 번째 데이터셋의 레이블
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // 그래프 내부 색
                borderColor: 'rgba(75, 192, 192, 1)', // 선 색
                borderWidth: 1,
                data: graph_exercise_calories, // 세 번째 데이터셋의 데이터
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true // y축을 0부터 시작
                }
            },
            responsive: true,
            maintainAspectRatio: true,
        }
    });

})