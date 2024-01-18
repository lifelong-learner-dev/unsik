
$(document).ready(function(){


    // 이미지 업로드 & 보여주기
    document.getElementById('fileUpload').addEventListener('change', function(event) {
        var file = event.target.files[0];
        var reader = new FileReader();
        
        reader.onload = function(e) {
            var img = document.createElement('img');
            img.src = e.target.result;
            img.style.maxWidth = '700px'; 
            img.style.maxHeight = '500px';
            
            var preview = document.getElementById('preview');
            preview.innerHTML = ''; 
            preview.appendChild(img); 
        };
        
        reader.readAsDataURL(file);
    });

    // '분석' 버튼 클릭시 함수
    document.getElementById('analyze-button').addEventListener('click', function() {
        // document.getElementById('current-section').style.display = 'none'; // 현재 섹션을 숨깁니다.
        document.getElementById('analysis-section').style.display = 'block'; // 분석 섹션을 표시합니다.
    });

    // 맞음 버튼 클릭 로직
    document.getElementById('confirm-button').addEventListener('click', function() {
    });

    // 틀림 버튼 클릭 로직
    document.getElementById('deny-button').addEventListener('click', function() {
    });

    updateComment()

    // document.addEventListener('DOMContentLoaded', updateComment);
})

// 시간별 코멘트
function updateComment() {
    var now = new Date();
    var hours = now.getHours();
    var commentText = '';

    if (hours >= 6 && hours <= 9) {
        // 아침 시간대 (6시-9시)
        commentText = '아침 식사가 중요합니다! 오늘 하루도 활기차게 시작하세요.';
    } else if (hours >= 11 && hours <= 14) {
        // 점심 시간대 (11시-14시)
        commentText = '점심 시간입니다! 균형 잡힌 식사로 에너지를 충전하세요.';
    } else if (hours >= 18 && hours <= 20) {
        // 저녁 시간대 (18시-20시)
        commentText = '저녁 시간이네요. 하루를 마무리하는 든든한 식사를 즐기세요.';
    } else {
        // 그 외
        commentText = '식사 시간이 아닙니다. 건강한 간식을 섭취해 보세요!';
    }

    document.getElementById('time_comment').textContent  = commentText;
}

updateComment()