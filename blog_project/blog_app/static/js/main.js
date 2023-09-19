const POSTLIST_API = 'http://127.0.0.1:8000/api/post';
const POPULAR_POST_API = 'http://127.0.0.1:8000/api/post';
const BOARD_URL = 'http://127.0.0.1:8000/board';

document.addEventListener('DOMContentLoaded', function () {
    fetchPostList();
});

async function fetchPostList() {
    try {
        const response = await fetch(POSTLIST_API);
        if (!response.ok) { throw new Error('API 호출에 실패하였습니다.'); }
        const data = await response.json();
        const postsContainer = document.getElementsByClassName('posting_list')[0];
        let postHTML = '';

        for (let i = 0; i < data.length; i++) {
            const currData = data[i]

            if (i == 0) { fetchPopularPost(currData); }

            const newContent = currData.content.replace(/<[^>]*>?/g, '');

            let options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: true };
            let uploadDate = new Date(currData.upload_date);
            uploadDate = uploadDate.toLocaleString("ko-KR", options);
            // replace 위치 바꾸면 오전 AM 변환
            uploadDate = uploadDate.replace(/\./g, '').replace(/ /g, '').replace('오전', 'AM').replace('오후', 'PM');
            uploadDate = `${uploadDate.slice(0, 4)}년 ${uploadDate.slice(4, 6)}월 ${uploadDate.slice(6, 8)}일 ${uploadDate.slice(8)}`;

            postHTML += `
                <div class='posting' onclick=window.location.href="${BOARD_URL}/${currData.id}">
                    <div class="posting-img">
                        <img src=${currData.img}> 
                    </div>
                    <div class="posting-info">
                        <div class="posting_date">${uploadDate}</div>
                        <div class="posting_title">${currData.title}</div>
                        <div class="posting_content">${newContent}</div>
                    </div>
                </div>
            `;

        }
        postsContainer.innerHTML = postHTML;
    } catch (error) {
        console.error('Error fetching data:', error.message);
    }
}

function fetchPopularPost(data) {
    const newContent = data.content.replace(/<[^>]*>?/g, '');
    popTitle = document.getElementsByClassName('pop_title')[0];
    popContent = document.getElementsByClassName('pop_content')[0];
    popImg = document.getElementsByClassName('pop_img')[0];
    readMoreButton = document.getElementsByClassName('read_more')[0];

    popTitle.innerHTML = data.title;
    popContent.innerHTML = newContent;
    popImg.src = data.img;
    readMoreButton.setAttribute('onclick', `window.location.href="${BOARD_URL}/${data.id}"`);
}