// board.js 

const RETRIEVE_API = "http://localhost:8000/api/post/";
const DELETE_API = "http://localhost:8000/api/post/";
const COMMENT_API = "http://127.0.0.1:8000/api/comment/";
const LIKE_API = "http://127.0.0.1:8000/api/like/";
const WRITE_URL = "http://127.0.0.1:8000/write/";
const BLOGPOSTID = document.location.href.split('/')[4];
const LIKE_BTN_DIR = "/static/img/board/like_btn.svg";
const LIKE_ACTIVE_BTN_DIR = "/static/img/board/like_active_btn.svg";


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function update() {
    const tmp = document.location.href.split('/');
    const blogPostId = tmp[4];
    window.location.href = WRITE_URL + blogPostId;
}

document.getElementById('edit_btn').addEventListener('click', update);

// 삭제
async function deletePost() {
    const tmp = document.location.href.split('/');
    const blogPostId = tmp[4];
    const response = await fetch(DELETE_API + blogPostId, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });

    window.location.href = MAIN_URL;
}

document.getElementById('delete_btn').addEventListener('click', deletePost);

function moveToRelatedPost(relatedPostId) {
    window.location.href = MAIN_URL + 'board/' + relatedPostId;
}

function drawComment(result) {
    const commentList = document.getElementsByClassName('comment_list')[0];

    const commentHTML = `
    <div class="comment" data-comment-id="${result.id}">
        <div class="comment_user_img">
            <div style="width:50px; height: 50px; border-radius: 70%; overflow:hidden;">
                <img src="/static/img/board/profile.png" style="width:50px; height:50px; object-fit:cover; cursor:pointer;">
            </div>
            <div style="display:flex; flex-direction: column; justify-content:space-between;">
                <div class="comment_user">yjk</div>
                <span>${result.comment}</span>
            </div>
        </div>
        <div class="action-box"> 
            <div class="comment_date"> ${result.chrmt_upload_date} </div>
            <div style="display:flex; justify-content: end; gap:10px;">
                <div>
                    <img src="/static/img/board/like_btn.svg" onclick="likePost(event,'1')">
                    <span class="like_cnt"> ${result.like_cnt} </span>
                </div>
                <div class="comment_btn">
                    <button class="comment_delete" onclick="if (window.confirm('삭제하시겠습니까?')) { deleteComment('1'); }">삭제</button>
                </div>
            </div>
        </div>
    </div>
    `;

    commentList.insertAdjacentHTML(
        'beforeend',
        commentHTML
    );
}

// 댓글 작성
async function postComment() {
    let formData = new FormData();
    const user = 1; // TODO: 유저 1로 고정해놓음
    const comment = document.getElementById('comment_input').value;

    formData.append('comment', comment);
    formData.append('user', user);
    formData.append('blog_post', BLOGPOSTID);

    const response = await fetch(COMMENT_API, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });

    if (response.ok) {
        const result = await response.json();
        alert("댓글이 성공적으로 작성되었습니다.");
        drawComment(result);
    }
}

function eraseComment(commentId) {
    const commentList = document.getElementsByClassName('comment_list')[0];
    const targetComment = document.querySelector(`[data-comment-id="${commentId}"]`);
    commentList.removeChild(targetComment);
}


// 댓글 삭제
async function deleteComment(commentId) {
    const response = await fetch(COMMENT_API + commentId, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });

    if (response.ok) {
        eraseComment(commentId);
        alert("댓글이 성공적으로 삭제되었습니다.");
    }
}

// 좋아요 작성
async function likePost(event, commentId) {
    let formData = new FormData();
    const comment = commentId;
    const user = 1; // TODO: user_id 1로 고정
    const blogPost = BLOGPOSTID;
    const img = event.target;
    const span = img.nextElementSibling;

    formData.append('user', user);
    formData.append('comment', comment);
    formData.append('blog_post', blogPost);

    const response = await fetch(LIKE_API, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });

    // 만약 원래 좋아요가 활성화 되어 있었다면
    if (response.status == 204) {
        event.target.src = LIKE_BTN_DIR;
        span.innerText = parseInt(span.innerText) - 1
    }
    else {
        event.target.src = LIKE_ACTIVE_BTN_DIR;
        span.innerText = parseInt(span.innerText) + 1
    }
}