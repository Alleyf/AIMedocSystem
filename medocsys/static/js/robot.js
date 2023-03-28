$(function () {
    var count = 0;
    var classes = ["theme_1", "theme_2", "theme_3", "theme_4"];
    var length = classes.length;
    $(function () {
        $('.pvr_chat_wrapper').toggleClass('imactive');

        $('.pvr_chat_button, .pvr_chat_wrapper .close_chat').on('click', function () {
            $('.pvr_chat_wrapper').toggleClass('active');
            let now = getFormatDate()
            // console.log(now)
            $(".date-break").text(now)
            return false;
        });

        $('.message-input').on('keypress', function (e) {
            if (e.which === 13) {
                if ($(this).val() === '') {
                    $('.chat-messages').append('<div class="message"><div class="message-content">' + "请输入你的问题，小医很荣幸为您解答哦！" + '</div></div>');
                    return false;
                } else {
                    let val = $(this).val();
                    $('.chat-messages').append('<div class="message self"><div class="message-content">' + val + '</div></div>');
                    $(this).val('');
                    let answer
                    // 获取chatgpt的回答
                    $.ajax({
                        url: "/chat/",
                        type: "post",
                        DataType: "json",
                        data: {
                            "question": val
                        },
                        success: function (res) {
                            answer = res.answer
                            console.log(res)
                            setTimeout(function () {
                                $('.chat-messages').append('<div class="message"><div class="message-content">' + answer + '</div></div>');
                                $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                                $messages_w.perfectScrollbar('update');
                            }, 200)
                            var $messages_w = $('.pvr_chat_wrapper .chat-messages');
                            $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                            $messages_w.perfectScrollbar('update');
                            return false;
                        }
                    })
                }


            }
        });

        $('.pvr_chat_wrapper .chat-messages').perfectScrollbar();
        $(".change_chat_theme").on('click', function () {
            $(".chat-messages").removeAttr("class").addClass("chat-messages " + classes[count]);
            if (parseInt(count, 10) === parseInt(length, 10) - 1) {
                count = 0;
            } else {
                count = parseInt(count, 10) + 1;
            }
            var $messages_w = $('.pvr_chat_wrapper .chat-messages');
            $messages_w.scrollTop($messages_w.prop("scrollHeight"));
            $messages_w.perfectScrollbar('update');
        })
    });
});

function getFormatDate() {
    var nowDate = new Date();
    var year = nowDate.getFullYear();
    var month = nowDate.getMonth() + 1 < 10 ? "0" + (nowDate.getMonth() + 1) : nowDate.getMonth() + 1;
    var date = nowDate.getDate() < 10 ? "0" + nowDate.getDate() : nowDate.getDate();
    var hour = nowDate.getHours() < 10 ? "0" + nowDate.getHours() : nowDate.getHours();
    var minute = nowDate.getMinutes() < 10 ? "0" + nowDate.getMinutes() : nowDate.getMinutes();
    var second = nowDate.getSeconds() < 10 ? "0" + nowDate.getSeconds() : nowDate.getSeconds();
    return year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second;
}