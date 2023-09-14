document.addEventListener('DOMContentLoaded', function () {
    fetchAndDisplayData();
});

async function fetchAndDisplayData() {
    const postListApi = 'http://127.0.0.1:8000/api/post';

    try {
        const response = await fetch(postListApi);
        if (!response.ok) {
            throw new Error('API 호출에 실패하였습니다.');
        }
        const data = await response.json();
        const postsContainer = document.getElementById('posts-container');
        // console.log('data', data)//데이터 불러오는지 체크

        data.forEach((post) => {
            // console.log(post.upload_date);//날짜불러오는지 체크
            const postElement = document.createElement('div');
            postElement.className = 'posting';
            postElement.innerHTML = `
                <div class="posting-img">
                </div>
                <div class="posting-info">
                    <div class="posting_date">${post.upload_date}</div>
                    <div class="posting_title">${post.title}</div>
                    <div class="posting_content">${post.content}</div>
                </div>
            `;
            postsContainer.appendChild(postElement);
        });
    } catch (error) {
        console.error('Error fetching data:', error.message);
    }
}

fetchAndDisplayData();