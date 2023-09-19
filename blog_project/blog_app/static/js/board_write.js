const RETRIEVE_API = "http://localhost:8000/api/post/";
const UPDATE_API = "http://localhost:8000/api/post/";
const TEMP_POST_API = "http://localhost:8000/api/post/temp_post/";

const POST_URL = "http://127.0.0.1:8000/api/post/";
const REDIRECT_URL = "http://127.0.0.1:8000/board/";
// const MAIN_URL = "http://127.0.0.1:8000/";

let FLAG = "write";
let blogPostId = 0;

async function initPost(url) {
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        }
    });
    if (response.ok) {
        const data = await response.json();
        if (data.title !== "") {
            FLAG = "update";
            const title = document.getElementById('id_title');
            let noteEditable = document.querySelector('iframe').contentWindow.document.querySelector(".note-editable");
            title.value = data.title;
            noteEditable.innerHTML = data.content;
            blogPostId = data.id;
        }
    }
}

const iframe = document.querySelector('iframe');
iframe.addEventListener("load", function () {
    const tmp = document.location.href.split('/');
    blogPostId = tmp[4];
    if (blogPostId) {
        initPost(RETRIEVE_API + blogPostId);
    }
    else {
        initPost(TEMP_POST_API);
    }
})

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

function getCategory() {
    const categoryNodeList = document.getElementsByName('post_category');
    for (let i = 0; i < categoryNodeList.length; i++) {
        if (categoryNodeList[i].checked) {
            return categoryNodeList[i].value;
        }
    }
}

// 작성
async function writePost(flag) {
    let formData = new FormData();
    let noteEditable = document.querySelector('iframe').contentWindow.document.querySelector(".note-editable");

    const content = noteEditable.innerHTML;
    const title = document.getElementById('id_title').value;

    formData.append('title', title);
    formData.append('content', content);
    formData.append('user', 1); // TODO: 유저 1로 고정해놓음

    if (flag == "temp") {
        formData.append('status', 'false'); // 임시저장
    } else {
        formData.append('status', 'true'); // 저장
    }

    formData.append('category', getCategory());


    if (FLAG == 'write') {
        var response = await fetch(POST_URL, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
    }
    else if (FLAG == 'update') {
        var response = await fetch(POST_URL + blogPostId, {
            method: 'PUT',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
    }

    if (response.ok) {
        const result = await response.json();
        if (flag == "temp") {
            alert("게시글이 성공적으로 임시 저장 되었습니다! ");
            window.location.href = MAIN_URL;
        }
        else {
            alert("게시글이 성공적으로 포스팅 되었습니다! ");
            window.location.href = REDIRECT_URL + result.id;
        }
    }
};