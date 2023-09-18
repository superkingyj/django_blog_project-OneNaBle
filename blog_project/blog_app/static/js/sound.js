// Audio 객체 설정
const myAudio = new Audio();
myAudio.src = "./sounds/naruto.mp3";

// 오디오 재생: 크롬브라우저에서 작동 안함
myAudio.play();

// 버튼 취득
const btnPlay = document.getElementById("btnPlay");
const btnPause = document.getElementById("btnPause");
const btnStop = document.getElementById("btnStop");

// 재생 버튼
btnPlay.onclick = function () {
    myAudio.play();
}

// 일시정지 버튼
btnPause.onclick = function () {
    myAudio.pause();
}

// 정지 버튼
btnStop.onclick = function () {
    myAudio.pause();
    myAudio.currentTime = 0; // 재생시간을 처음으로 설정
}