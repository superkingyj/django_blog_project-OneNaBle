const MAIN_URL = "http://127.0.0.1:8000/";
const FILTERTING_API = "http://127.0.0.1:8000/api/post/filter/?category=";
const SEARCH_API = "http://127.0.0.1:8000/search?q=";

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
function moveToMain() {
    window.location.href = MAIN_URL;
}

async function filtering(filteringId) {
    const response = await fetch(FILTERTING_API + filteringId, {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });

    if (response.ok) {
        const data = await response.json();
        const postsContainer = document.getElementsByClassName('posting_list')[0];
        let postHTML = '';

        for (let i = 0; i < data.length; i++) {
            const currData = data[i]
            const newContent = currData.content.replace(/<[^>]*>?/g, '');
            postHTML += `
                <div class='posting' onclick=window.location.href="${BOARD_URL}/${currData.id}">
                    <div class="posting-img">
                        <img src=${currData.img}> 
                    </div>
                    <div class="posting-info">
                        <div class="posting_date">${currData.upload_date}</div>
                        <div class="posting_title">${currData.title}</div>
                        <div class="posting_content">${newContent}</div>
                    </div>
                </div>
            `;

        }
        postsContainer.innerHTML = postHTML;
    } else {
        console.error('Error fetching data:', error.message);
    }
}

function fetchSearchPostList(data) {
    const postsContainer = document.getElementsByClassName('posting_list')[0];
    let postHTML = '';

    for (let i = 0; i < data.length; i++) {
        const currData = data[i];
        const newContent = currData.content.replace(/<[^>]*>?/g, '');
        postHTML += `
            <div class='posting' onclick=window.location.href="${BOARD_URL}/${currData.id}">
                <div class="posting-img">
                    <img src=${currData.img}> 
                </div>
                <div class="posting-info">
                    <div class="posting_date">${currData.upload_date}</div>
                    <div class="posting_title">${currData.title}</div>
                    <div class="posting_content">${newContent}</div>
                </div>
            </div>
        `;

    }
    postsContainer.innerHTML = postHTML;

}

// 검색 기능
async function search() {
    const q = document.querySelector("#search_box").value;
    const response = await fetch(SEARCH_API + q, {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });

    const data = await response.json();
    fetchSearchPostList(data);
}

document.querySelector("#search_box").addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        search();
    }
});
