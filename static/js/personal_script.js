$(document).ready(function () {
    listing();
});

function listing() {    //서버로부터 데이터 GET
    $('#cards-box').empty()
    $.ajax({
        type: 'GET',
        url: '/sung',
        data: {},
        success: function (response) {
            let rows = response['teams']
            for (let i = 0; i < rows.length; i++) {
                let name = rows[i]['name']     //이름 변수
                let star = rows[i]['star']
                let comment = rows[i]['comment']//코멘트 변수
                let num = rows[i]['num']        //선택한 데이터 삭제하기 위한 번호 기록 변수
                let randomNum = rows[i]['randomNum']//이미지 랜덤출력을위한 1~8 사이 숫자를 가진 변수

                let star_image = '⭐'.repeat(star) //평점 변수

                let temp_html = `<div class="col">
                                            <div class="card h-100" style="margin-bottom :25px">
                                                <img src="http://squirrelswj.shop/static/` + randomNum + `.png" class="card-img-top" alt="">
                                                <div class="card-body">
                                                    <h5 class="card-title">${name}</h5><p class="card-star">${star_image}</p>
                                                    <p class="card-text"><hr></p>
                                                    <p class="mycomment">${comment}</p>
                                                    <div class="delete-btn">
                                                        <button onclick="data_delete(${num})" type="button" class="btn btn-outline-secondary">삭제</button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>`
                $('#cards-box').append(temp_html)
            }
        }
    })
}

function posting() {    //방명록 기록하기 버튼 클릭 시 POST
    let name = $('#name').val()
    let star = $('#star').val()
    let comment = $('#comment').val()

    let randomNum = Math.floor((Math.random() * 10));     //랜덤이미지를 위한 1~8까지 랜덤숫자
    randomNum = parseInt(randomNum % 8) + 1;

    $.ajax({
        type: 'POST',
        url: '/sung',
        data: {'name_give': name, 'star_give': star, 'comment_give': comment, 'randomNum_give': randomNum},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}

function data_delete(num) {    //방명록 삭제 버튼 클릭시 num_give POST
    $.ajax({
        type: 'POST',
        url: '/sung/delete',
        data: {'num_give': num},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}

function open_box() {   //방명록 기록하기 hidden해제
    $('#post-box').show()
}

function close_box() {  //방명록 기록하기 hidden
    $('#post-box').hide()
}