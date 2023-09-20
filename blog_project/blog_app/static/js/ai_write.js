$(document).ready(function () {
    $('#content').summernote();
});

document.getElementById('aiAutocompleteButton').addEventListener('click', function () {
    // 로딩 애니메이션 
    document.getElementById('loading-animation').style.display = 'block';
    document.getElementById('ai-img').style.display = 'none';

    let title = document.getElementById('id_title').value;
    fetch('/autocomplete/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: new URLSearchParams({
            'title': title
        })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('loading-animation').style.display = 'none';
            document.getElementById('ai-img').style.display = 'block';

            //기존 내용에 자동완성 된 내용 더함
            // let currentContent = summernote.activeEditor.getContent();
            // data.message = data.message.replace(/\n/g, '<br>');
            // summernote.activeEditor.setContent(currentContent + data.message);
            //gpt 생성
            //기존 내용에 자동완성 된 내용 더함
            // let currentContent = $('#content').summernote('code'); // get current content
            // data.message = data.message.replace(/\n/g, '<br>');
            // $('#content').summernote('code', currentContent + data.message); // set new content
            // console.log(data);
            data.message = data.message.replace(/\n/g, '<br>');
            let noteEditable = document.querySelector('iframe').contentWindow.document.querySelector(".note-editable");
            noteEditable.innerHTML += data.message;

        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('loading-animation').style.display = 'none';
        });
});
