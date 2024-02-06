$(document).ready(function () {
    $('#bdSearchFrm').on('submit', function (event) {
        // submit 이벤트 기본 기능 : 페이지 새로고침
        // 페이지 새로고침 되지 않도록
        event.preventDefault();

        // 폼에 입력한 값들을 쿼리 스트링 방식의 데이터로 변환
        // type=bookname&keyword=자전거
        // serializer() 사용 : 쿼리 스트링 방식의 데이터로 변환
        let formData = $(this).serialize();
        const isLocalhost = Boolean(
            window.location.hostname === "localhost" ||

            window.location.hostname === "[::1]" ||

            window.location.hostname.match(
                /^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/
            )
        );

        let ajaxUrl = ""; // 이 변수에 API 엔드포인트 URL을 설정합니다.
        let detailUrl = "";
        if (isLocalhost) {
            // 로컬 호스트인 경우
            ajaxUrl = "http://127.0.0.1:8000/board/search/";
            detailUrl = "http://127.0.0.1:8000/board/detail/";
        } else {
            // 웹 서버인 경우
            ajaxUrl = "http://18.180.43.72/board/search/"; // 웹 서버의 실제 API 엔드포인트 URL로 대체해야 합니다.
            detailUrl = "http://18.180.43.72/board/detail/";
        }

        $.ajax({
            type: "post",
            // url: "/book/get_data/",
            url: ajaxUrl,
            data: formData,
            dataType: 'json', // "datatype"가 아닌 "dataType"로 수정
            success: function (result) {
                console.log(result);
                console.log(result.bd_list_json);
                let bd_list = result.bd_list_json;
                //반환된 결과를 searchResultBox에 테이블 형태로 출력 (삽입)
                // div 태그에 삽입 : append()
                // 실행할 때마다 append() 이전 결과 뒤에 계속 append 됨 그래서 삭제하고 다시 시작
                $('#searchResultBox').empty();

                // 테이블 태그 문자열로 생성
                let tableHTML = `
                    <table class="table">
                        <thead class="thead-dark">
                            <tr> 
                                <th scope="col" class="text-center">제목</th>
                                <th scope="col" class="text-center">내용</th>
                                <th scope="col" class="text-center">카테고리</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                //데이터 추출해서 append
                if (bd_list.length == 0) {
                    tableHTML += '<tr class="align-middle"><td colspan="4" class="text-center">찾는 게시물이 없습니다.</td></tr>';
                } else {
                    for (let i = 0; i < bd_list.length; i++) {
                        const boardDetailURL = detailUrl;
                        const link = `<a href="${boardDetailURL}${bd_list[i].pk}/">${bd_list[i].pk}</a>`;
                        tableHTML += `
                            <tr class="align-middle">
                                <td class="text-center" scope="row">${link}</td>
                                <td class="text-center" scope="row">${bd_list[i].fields.title}</td>
                                <td class="text-center" scope="row">${bd_list[i].fields.category}</td>
                            </tr>
                        `;
                    }
                }

                // 테이블 닫는 태그를 추가
                tableHTML += '</tbody></table>';

                // HTML을 searchResultBox에 추가
                $('#searchResultBox').append(tableHTML);
            },
            error: function () {
                // 오류 발생했을 때
                alert("오류 발생");
            },
            complete: function () {
                // 완료되었을 때 수행된 함수
            }
        });
    });
});