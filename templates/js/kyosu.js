
var chatStart = 0; // 채팅 시작 상태 플래그
var isApiCalling = false; // API 호출 상태 플래그
var promptId; // 현재 프롬프트의 ID
var recognition; // 음성 인식 객체
var recognitionActive = false
var chatPlayPause = new Audio(); 
    chatPlayPause.preload = 'auto'; // 오디오 파일 미리 로드
    chatPlayPause.src = 'audio//start.mp3'    
var audioPlayer = new Audio(); // 오디오 플레이어 객체
audioPlayer.preload = 'auto'; // 오디오 파일 미리 로드
// audioPlayer.src = 'audio\\hello-GTalk.mp3'; // 오디오 파일 경로 설정
audioPlayer.src = 'audio//start.mp3'

var userIcon = '<i class="fa-solid fa-user text-secondary"></i> '; // 사용자 아이콘 HTML
var aiIcon = '<img  class="aiIcon" src="images/gtalk-white.png" width="20"> '; // AI 아이콘 HTML
var micIcon=`
        <div class="ps-3 micIcon chat-play-pause-button cursor-pointer ">
            <i class="standby-Mic fa-duotone fa-microphone fs-1"></i>
       </div>`
var stopWords  = ['종료', '그만', '바이','마이크'];   
var startWords = ['다시', '안녕', '지톡','톡톡'];       
clientDevicesId=""

$(document).ready(function() {
    binding()

    var selectedTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : 'light'; // 저장된 테마를 가져옵니다.
    clientDevicesId= localStorage.getItem('clientDevicesId') ?  localStorage.getItem('clientDevicesId'): randomKey(16);
    localStorage.setItem('clientDevicesId', clientDevicesId); 
    $("#clientDevicesId").text( clientDevicesId)
    
    $('#bg-theme').val(selectedTheme);

    bg_change( selectedTheme )

    
    $('.bg-theme').click(function() {
        var selectedTheme = $(this).attr("bg-theme"); // 선택된 테마 값을 가져옵니다.
        localStorage.setItem('theme', selectedTheme); // 선택된 테마를 localStorage에 저장합니다.
        bg_change( selectedTheme );
        $(this).blur();
        
    });
    $("#clientDevicesId").click( function(){
        $("#clientDevicesId").addClass("d-none")
    })
})
function binding(){
    $("#start-chat-button").unbind()
    $("#chat-play-pause").unbind()
    $("#chat-play-pause-button").unbind()
    $(".chat-play-pause-button").unbind()
    $("#start-chat-button").click(function() {
        isApiCalling = false; // API 호출 상태를 false로 초기화
        initializeRecognition(); // 음성 인식 초기화
        $(".start-info").hide(500,function(){
            $("#chat-play-pause-button").show(500)
            $(".micIcon").show(500)
            chatStart = 1; // 채팅 시작 플래그를 true로 설정
            audioPlayer.play(); // 오디오 재생
            chatPlayPause.play();
        })
    });
    $(".chat-play-pause-button").click(function(event) {
        event.stopPropagation();
        if ($('.standby-Mic').hasClass('text-secondary')) {
            chat_start()
        } else {
            chat_stop()
        } 

    });
    $("#chat-play-pause").click(function(event) {
        event.stopPropagation();
        if ($(this).attr("state-Chat")=='pause' ) {
            chat_start(this)
        } else {
            chat_stop(this)
        } 

    });
}    
function chat_start(_this){
    isApiCalling = false; // API 호출 상태를 false로 초기화
    initializeRecognition(); // 음성 인식 초기화
    $(".standby-Mic").remove()
    chatStart = 1; // 채팅 시작 플래그를 true로 설정
    //audioPlayer.play(); // 오디오 재생
    chatPlayPause.play();
    $("#chat-play-pause").attr("state-Chat",'chatStart')
    $(".start-info").hide(500)
    $("#chat-box").append(`${micIcon}`);  binding();
    $("#chat-play-pause-button").show(500)
    $(".micIcon").show(500)
    recognition.start(); // 음성 인식 시작
   
};
function chat_stop(){
    
    chatStart =0; // 채팅 시작 플래그
    isApiCalling = false; // API 호출 상태를 false로 초기화
    $(".standby-Mic").remove() 
    chatPlayPause.play();
    $("#chat-box").append(`${micIcon}`);  binding();
    $(".standby-Mic").addClass("text-secondary")
    $("#chat-play-pause").attr("state-Chat",'pause')
    recognition.stop(); // 음성 인식 종료
    
};
function downLoad(fileName) {    
    window.location.href = '/download/' + fileName; // 파일 이름을 URL에 추가하여 서버에 요청
}
// 오디오 재생 완료 이벤트 핸들러 설정
audioPlayer.onended = function() {
    if( chatStart==0 ) { 
        $("#chat-box").append(`${micIcon}`);
        $(".standby-Mic").addClass("text-secondary")
        
        $("#chat-play-pause").attr("state-Chat",'pause')
        binding();
        return  } 
    isApiCalling = false; // 오디오 재생 완료 후 API 호출 상태를 false로 변경
    if (chatStart) { // 사용자가 채팅을 시작한 상태라면
        recognition.start(); // 음성 인식을 재시작
    }
    $("#chat-play-pause").attr("state-Chat",'chatStart')
    $("#chat-box").append(`${micIcon}`);  binding();
    $('html, body').animate({
        scrollTop: $(document).height()
    }, 1000);
};

function initializeRecognition() {
    window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.interimResults = true;
    recognition.lang = 'ko-KR';
    recognition.onstart = function() {
        console.log("음성 인식 시작됨");
        promptId = "prompt-" + Math.random().toString(36).substring(2, 12);
    };
    recognition.onend = function() {
        if( chatStart==0 ) { return  } 
        recognitionActive = false
        console.log("음성 인식 종료됨");
        
        if ( ! isApiCalling ) { // API 호출 중이 아니면
            send_prompt(promptId); // send_prompt 함수 호출
        }
    };
    recognition.onerror = function(event) {
        if( chatStart==0 ) { return  } 
        recognitionActive = false
        console.log("음성 인식 오류 발생: " + event);
        
        if ( ! isApiCalling ) { 
            try {
                recognition.start()       
            } catch (error) {
                
            }
            
        }
        
    };
    recognition.onresult = function(event) {
        if( chatStart==0 ) { return  } 
        recognitionActive = true;
        var texts = Array.from(event.results).map(result => result[0].transcript).join("");
        if ($('#' + promptId).length == 0) {
            $('#chat-box').append($('<p>').attr('id', promptId));
        }
        
        $('#' + promptId).html(userIcon + texts);
    };
}


function send_prompt(currentPromptId) {
    var promptText = $('#' + currentPromptId).text().trim();
    if (promptText === "") {
        try { recognition.start()} catch (error) {}
       
        return; // 프롬프트가 비어 있으면 여기서 함수 종료
    }
    var shouldStop = stopWords.some(function(stopWord) { // Using Array.prototype.some for brevity.
        return promptText.includes(stopWord);
    });

    if (shouldStop) { 
        chat_stop();
        return
    }

    isApiCalling = true; // API 호출 상태를 true로 설정
    recognition.stop(); // 음성 인식 중지
    var aiChatId = "ai-" + Math.random().toString(36).substring(2, 10);
    $(".micIcon").hide(500,function(){ $(this).remove()})
    $("#chat-box").append(`<p id="${aiChatId}"><span id="loading" class="loading"></span></p>`);
    startLoadingAnimation();
    // alert( clientDevicesId )
    $.ajax({
        url: "/chatGPT_tts",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({  clientDevicesId: clientDevicesId, prompt: promptText, voice: "alloy", chat_id: aiChatId }),
        success: function(response) {
            // debugger
            // console.log( response)
            var htmlContent = aiIcon + response.answer;
            $('#' + aiChatId).html(htmlContent);
            stopLoadingAnimation()
            $('html, body').scrollTop($(document).height());
            audioPlayer.src = 'chat_audio/' + aiChatId + '.mp3'
            audioPlayer.play().then( function(){
                stopLoadingAnimation(); // 
                
                $('html, body').animate({
                    scrollTop: $(document).height()
                }, 3000);
            // var shouldStop = stopWords.some(function(word) {return  promptText.includes(word) ||  response.answer.includes(word);});
            //     if (shouldStop) {  $(".standby-Mic").remove();chat_stop()}
            }); 
            
        },
        error: function(err) {
            stopLoadingAnimation(); // 
            console.log("Error occurred:", err);
            $('#' + aiChatId).html("시험 버전에서는 1일 사용한도가  제한되어 있습니다. 약 10분 후에 다시 사용 가능합니다.");
            audioPlayer.src = 'audio//start.mp3'
            audioPlayer.play().then( function(){
                $('html, body').scrollTop($(document).height());
            })
        }
    });
   
}


function bg_change( selectedTheme ){
    var changColor=['bg-warning','bg-white','text-danger']
    if ( selectedTheme =="dark"){
           $(".aiIcon").attr("src","images/gtalk-white.png")
            $.each( changColor, function(index, colorClass){
                $(`.${colorClass}`).addClass(`${colorClass}-remove`).removeClass(`${colorClass}`);
            })

    } else {
          $(".aiIcon").attr("src","images/GTalk-trans-40.png")
            $.each( changColor, function(index, colorClass){
                $(`.${colorClass}-remove`).addClass(`${colorClass}`).removeClass(`${colorClass}-remove`);   
            })
   }
   $('html').attr('data-bs-theme', selectedTheme); 

}
var loadingAnimation; // Declare the variable to store interval ID globally
function startLoadingAnimation() {
    loadingAnimation = setInterval(function() {
        $('#loading').text(function(index, text) {
            return text.length < 30 ? text + '.' : '.';
        });
    }, 1000); // Start an interval to add a dot every 1000 milliseconds
}

function stopLoadingAnimation() {
    clearInterval(loadingAnimation); // Clear the interval
    $('#loading').text(''); // Clear the loading text
}
function randomKey(n){
   var randomStr=Math.random().toString(36).substring(2, 10) + Math.random().toString(36).substring(2, 10)
    return randomStr.substring(0, n-1);
}  
$(document).ready(function() {
    // ... (기존 코드)

    function addUserMessage(message) {
        $('#chat-box').append(`<p>${userIcon}${message}</p>`);
        $('html, body').animate({
            scrollTop: $(document).height()
        }, 1000);
    }

    $('#send-button').click(function() {
        const userInput = $('#user-input').val().trim();

        if (userInput === '') return;

        addUserMessage(userInput); // 사용자 입력을 채팅창에 추가

        // AI에게 userInput을 전달하고 응답을 받아오는 부분을 추가하셔야 해요.
        // 여기에 해당 부분을 추가하시면 사용자가 입력한 텍스트를 AI에게 전달할 수 있어요.
        // 응답을 받은 후, AI의 답변도 채팅창에 추가해주시면 됩니다.
        
        $('#user-input').val(''); // 입력창 초기화
    });

    // …
});
