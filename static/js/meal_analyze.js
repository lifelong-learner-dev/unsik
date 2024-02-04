
$(document).ready(function () {


    // 이미지 업로드 & 보여주기
    document.getElementById('fileUpload').addEventListener('change', function (event) {
        var file = event.target.files[0];
        var reader = new FileReader();

        reader.onload = function (e) {
            var img = document.createElement('img');
            img.src = e.target.result;
            img.style.maxWidth = '696px';
            img.style.maxHeight = '492px';

            var preview = document.getElementById('preview');
            preview.innerHTML = '';
            preview.appendChild(img);
        };

        reader.readAsDataURL(file);
    });

    // '분석' 버튼 클릭시 함수
    document.getElementById('analyze-button').addEventListener('click', function () {
        // document.getElementById('current-section').style.display = 'none'; // 현재 섹션을 숨깁니다.
        document.getElementById('analysis-section').style.display = 'block'; // 분석 섹션을 표시합니다.
    });
});