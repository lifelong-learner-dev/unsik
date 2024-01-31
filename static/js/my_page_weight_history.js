$(document).ready(function () {

    var ctx = document.getElementById('weightsChart');
    var chart = new Chart(ctx, {
        type: 'line', // 라인 차트 유형
        data: {
            labels: weight_dates, // x축 레이블로 날짜 사용
            datasets: [{
                label: '몸무게', // 데이터셋의 레이블
                backgroundColor: 'rgba(255, 99, 132, 0.2)', // 그래프 내부 색
                borderColor: 'rgba(255, 99, 132, 1)', // 선 색
                borderWidth: 1,
                data: weights, // y축 데이터로 칼로리 사용
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true // y축을 0부터 시작
                }
            },
            responsive: true,
            maintainAspectRatio: false,
        }
    });

})