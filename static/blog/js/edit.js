
// http://kindeditor.net/demo.php

KindEditor.ready(function (K) {
    window.editor = K.create("#article_content", {
       width: "800px",
       height: "600px",
       uploadJson: "/upload/",
       extraFileUploadParams: {
            csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()
       },
       filePostName:"upload_img"
    });
});