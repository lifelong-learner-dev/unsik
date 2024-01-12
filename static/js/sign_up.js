$(document).ready(function () {

    // 아이디 중복 검사 기능
    $('.id_check').click(function() {
        var username = $('#input_id').val();
        if (username) {
            let csrftoken = $('[name=csrfmiddlewaretoken]').val();
            $.ajax({
                type: 'post',
                url: 'http://127.0.0.1:8000/users_app/id_check',
                data: {'username': username},
                headers: {'X-CSRFToken': csrftoken},
                success: function(data) {
                    console.log(data)
                    if (data.is_taken) {
                        alert('이미 사용 중인 아이디입니다.');
                        $('#input_id').val('');
                    } else {
                        alert('사용 가능한 아이디입니다.');
                    }
                }
            });
        } else {
            alert("아이디를 입력해주십시오");
        };
    });
});