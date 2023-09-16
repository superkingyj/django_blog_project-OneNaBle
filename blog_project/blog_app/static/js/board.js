const RETRIEVE_API = "http://localhost:8000/api/post/";
const DELETE_API = "http://localhost:8000/api/post/";
const WRITE_URL = "http://127.0.0.1:8000/write/";
const MAIN_URL = "http://127.0.0.1:8000/";

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

document.getElementById('edit').addEventListener('click', update);

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

document.getElementById('delete').addEventListener('click', deletePost);

function moveToRelatedPost(relatedPostId) {
    window.location.href = MAIN_URL + 'board/' + relatedPostId;
}