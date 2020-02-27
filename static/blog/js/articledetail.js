
$(function () {
   $("#div_digg .digg-action").click(function (event) {
      var $obj = $(this).children("span");
      var val = $obj.text();
      var isUp = $(this).hasClass("diggit");
      var diggTips = $("#digg_tips");

      $.ajax({
         url: "/diggit/",
         async: true,
         type: "post",
         data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            is_up: isUp,
            article_id: $("#id_article").text(),
         },
         success: function (data, status, xhr) {
            if (data.status) {
               $obj.text(parseInt(val) + 1);
            } else {
               var tips = data.handled?"你已经推荐了！":"你已经反对了！";
               diggTips.text(tips);
            }
         },
         error: function (xhr, data, status,) {
            console.log("error");
         }
      });
   });

   var pid = null;
   $("#id_btn_submit").click(function (event) {
      var content = $("#tbCommentBody").val();
      if (pid) {
         var index = content.indexOf("\n");
         content = content.slice(index + 1);
      }
      $.ajax({
         url: "/comment/",
         async: true,
         type: "post",
         data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            article_id: $("#id_article").text(),
            content: content,
            pid: pid,
         },
         success: function (data, status, xhr) {
            $("#tbCommentBody").val("");

            if (data["status"]) {
               $("#id_feedback").removeClass("invisible");
               var createTime = data["create_time"];
               var content = data["content"];
               var user = data["user"];
               var listGroup = $("#id_list_group");
               var listId = null;
               var btnObj = $("#id_list_group button");
               var commentId = data["comment_id"];
               var subComment = "";
               console.log(btnObj.length);
               if (btnObj.length) {
                  listId = parseInt($("#id_list_group button:last-child").attr("data-level")) + 1;
               } else {
                  listId = 1;
               }
               if (pid) {
                   var parContent = data["parent_comment"];
                   subComment = `<span class="help-block">@&nbsp;${user}: ${parContent}</span>`

               }
               var tmp = `
            <button type="button" class="list-group-item" data-level="${listId}">
                <a href="#"># ${listId}楼</a>&nbsp;&nbsp;
                <span>${createTime}</span>
                <a href="/${user}">${user}</a>
                <a title="发送站内短消息" class="sendMsg2This">&nbsp;</a>
                <a class="pull-right class-reply" data-username="${user}" data-commentId="${commentId}">回复</a>
                ${subComment}
                <span class="help-block">${content}</span>
            </button>
               `;
               listGroup.append(tmp);
            }
            pid = null;
         },
         error: function (xhr, data, status) {
            console.log("Error");
         }
      });
   });

   $(".class-reply").click(function (event) {
      var curUser = $(this).attr("data-username");
      $("#tbCommentBody").focus().val("@" + curUser + "\n");
      pid = $(this).attr("data-commentId");
   });

   $("#id_comment_tree_title").click(function (event) {
      $.ajax({
         url: "/get-comment-tree/",
         async: true,
         type: "get",
         data: {
            article_id: $("#id_article").text(),
         },
         success: function (data, status, xhr) {

            $.each(data, function (index, data) {
               var pk = data["pk"];
               var content = data["content"];
               var parentCommentId = data["parent_comment_id"];
               var tmp = `<div class="comment-item" data-commentId-tree="${pk}"><span>${content}</span></div>`;
               if (!parentCommentId) {
                  $("#id_comment_tree").append(tmp);
               } else {
                  var selector = `[data-commentId-tree=${parentCommentId}]`;
                  $(selector).append(tmp);
               }

            })
         },
         error: function (xhr, data, status) {
            console.log("Error");
         }
      });
   })
});