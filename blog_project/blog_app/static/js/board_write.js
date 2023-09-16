const RETRIEVE_API = "http://localhost:8000/api/post/";
const UPDATE_API = "http://localhost:8000/api/post/";

const POST_URL = "http://127.0.0.1:8000/api/post/";
const REDIRECT_URL = "http://127.0.0.1:8000/board/";


let FLAG = "write";
let blogPostId = 0;

document.addEventListener('DOMContentLoaded', async function () {
    const tmp = document.location.href.split('/');
    blogPostId = tmp[4];

    if (blogPostId) {
        const response = await fetch(RETRIEVE_API + blogPostId, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        console.log(response);

        if (response.ok) {
            FLAG = "update";
            const data = await response.json();
            let noteEditable = document.querySelector('iframe').contentWindow.document.querySelector(".note-editable");
            const title = document.getElementById('id_title');
            noteEditable.innerHTML = data.content;
            title.value = data.title;
        }
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
async function write() {
    let formData = new FormData();
    let noteEditable = document.querySelector('iframe').contentWindow.document.querySelector(".note-editable");

    const content = noteEditable.innerHTML;
    const title = document.getElementById('id_title').value;

    formData.append('title', title);
    formData.append('content', content);
    formData.append('user', 1); // TODO: 유저 1로 고정해놓음
    formData.append('status', 'true'); // 저장
    formData.append('category', getCategory());

    console.log(formData);

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
        console.log(result);
        window.location.href = REDIRECT_URL + result.id;
    }
};

document.getElementById('post_form_btn').addEventListener('click', write);