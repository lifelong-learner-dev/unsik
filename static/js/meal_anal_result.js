$(document).ready(function(){
    // remove_input 클래스가 부여된 버튼을 클릭했을 때
    $('#meal_result_form').on('click', '.remove_input', function(event) {
        // 해당 개체의 이전 값 input 태그를 지우고
        // 자기 자신도 지워버린다.
        $(this).prev('input').remove();
        $(this).remove();
    });

    // add_input_box 즉 '입력창 추가' 버튼을 클릭했을 때
    $('#add_input_box').on('click', function(event) {
        const last_input = $('#meal_result_form').find(':input:last');

        // input을 하나 만든다
        const add_input = $('<input>', {
            type: 'text',
            name: 'food_info[]'
        });

        // input을 없앨 수 있는 버튼
        const remove_btn = $('<button>', {
            class: 'remove_input',
            text: '입력창 삭제'
        });

        last_input.after(add_input, remove_btn);
    });

    // 일반적으로 Django에서 csrf_token의 추적을 받지 않는 입력창이 임의로 추가되면
    // Django에서 csrf 보안 경고를 날린다. 때문에 새로 추가된 input 박스도
    // csrf의 관리 하에 들어가게 만들어야 한다.

    // 이 부분은 알아내기 특히 어려웠다.
    $('#submit_form').on('click', function() {
        const form = $('#meal_result_form');
        const formData = form.serialize();
        const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: 'http://127.0.0.1:8000/meal/meal_to_analyze', // url 수정 필요. (폼을 보낼 페이지로)
            type: 'POST',
            data: formData + '&csrfmiddlewaretoken=' + csrf_token,
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            processData: false,
            success: function(response) {
                console.log('성공', response)
            },
            error: function (error) {
                console.error('CSRF 토큰 오류 발생', error);
            }
        });
    });
});