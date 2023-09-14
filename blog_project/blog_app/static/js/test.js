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

        // main_box에 가장 좋아요 수가 많은 글 띄우기
        if (maxLikePost) {
            displayMainBox(maxLikePost);
        }

        // 같은 카테고리의 글들을 smallbox에 띄우기
        data.forEach((post) => {
            if (post.category_name === maxLikePost.category_name && post.id !== maxLikePost.id) {
                displaySmallBox(post);
            }
        });
        // user_id가 1인 포스트 중에서 like_count가 가장 높은 포스트 찾기
        // 고쳐야 로그인한 유저 id 할껀대 잘모르곘슴당
        // let maxLikePost = null;
        // data.forEach((post) => {
        //     if (post.user_id === 1) {
        //         if (!maxLikePost || post.like_count > maxLikePost.like_count) {
        //             maxLikePost = post;
        //         }
        //     }
        // });

    } catch (error) {
        console.error('Error fetching data:', error.message);
    }
}

function displayMainBox(post) {
    const mainBoxContainer = document.querySelector('.main_posting');
    mainBoxContainer.innerHTML = `
     <div class="posting_date">${post.upload_date}</div>
     <div class="posting_title">${post.title}</div>
     <div class="writer">by ${post.user_id}</div>
     <div class="content_tag">${post.category_name}</div>
     <div class="posting_content">${post.content}</div>
     `;
}

function displaySmallBox(post) {
    const smallboxContainer = document.querySelector('.recommend');
    const subPostingElement = document.createElement('div');
    subPostingElement.className = 'sub_posting';

    subPostingElement.innerHTML = `
      <img class="sub_img" src="${post.image_url}">
      <div class="sub_title">${post.title}</displaySmallBox>`;

    smallboxContainer.appendChild(subPostingElement);
}
