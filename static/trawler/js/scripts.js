/*!
* Start Bootstrap - Modern Business v5.0.7 (https://startbootstrap.com/template-overviews/modern-business)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-modern-business/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

//let a = "HELLO";
//console.log(a)

$(".save-message").on("click", save_message)  // .save-message class from html

function save_message(e) {
//    console.log(e);
    e.preventDefault();
    let messageData = {
        tg_chat_username: this.dataset.username,
        tg_message_id: this.dataset.id
    }
    $.ajax(
        {
            url: "http://127.0.0.1:8000/save_message",
            method: "post",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(messageData),
            success: function (data) {
                console.log(data)
            },
            error: function (e) {
                console.log(e)
            }
        }
    )
    console.log(messageData);
}