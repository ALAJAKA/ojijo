$(document).ready(function () {
    listing();
    console.log('스크립트실행')
});

function listing() {
    $.ajax({
        type: 'GET',
        url: '/personal/site',
        data: {},
        success: function (response) {
            let rows = response['result']
            let user_nk = rows[0]['user_nk']
            let user_img = rows[0]['user_img']
            let user_fp = rows[0]['user_fp']
            let user_email = rows[0]['user_email']

            // profile append
            let temp_html = `<div class="profile">
                                <a href="https://velog.io/@squirrelswj"><img src="../static/personal_img/night.png"></a>
                                <div class="profile_text">
                                    <a href="https://velog.io/@squirrelswj"><div class="name">${user_nk}</div></a>
                                    <div class="discription">${user_fp}</div>
                                </div>
                            </div>
                            <div class="line"></div>
                            <div class="icon">
                                <a href="https://github.com/squirrelswj" target="_black" style="margin-left:0px"><img src="../static/personal_img/git_icon.svg"></a>
                                <a href="https://velog.io" target="_black"><img src="../static/personal_img/house.png"></a>
                                <a href="${user_email}" target="_black"><img src="../static/personal_img/email.png"></a>
                            </div>`
            $('#profile').append(temp_html)

            //contents append
            for (let i = 0; i < rows.length; i++) {
                let bd_title = rows[i]['bd_title']
                let bd_content = rows[i]['bd_content']
                let bd_writeDate = rows[i]['bd_writeDate']
                let bd_id = rows[i]['id']
                let bd_img = rows[i]['image']

                let temp_html1 = `<div class="contents">
                                    <a href="/boards/${bd_id}">${bd_title}</a>
                                    <p>${bd_content}</p>
                                    <div class="subinfo">${bd_writeDate} · 0개의 댓글 · ♥0</div>
                                 </div>`
                let temp_html2 = `<div class="contents">
                                    <a href="/boards/${bd_id}">
                                    <div class="content_img"><img src="../static/posting_images/${user_nk}/board_${bd_id}/${bd_img}" alt="post-thumbnail" ></div>
                                    </a>
                                    <a href="/boards/${bd_id}">${bd_title}</a>
                                    <p>${bd_content}</p>
                                    <div class="subinfo">${bd_writeDate} · 0개의 댓글 · ♥0</div>
                                 </div>`
                if (bd_img == null)
                    $('#contents').append(temp_html1)
                else
                    $('#contents').append(temp_html2)

            }
        }
    })

}