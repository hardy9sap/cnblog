

$(function () {

    // 表单数据ajax方式提交
    $("#id_register_btn").click(function (event) {
        // 方式一，循环添加
        var formdata = new FormData();
        // var fieldsName = {
        //     email: "#id_email",
        //     tel: "#id_tel",
        //     loginname: "#id_name_for_login",
        //     nickname: "#id_nickname",
        //     pwd: "#id_pwd",
        //     confirmpwd: "#id_confirm_pwd",
        //     csrfmiddlewaretoken: "[name=csrfmiddlewaretoken]",
        // };
        // for (let key in fieldsName) {
        //     formdata.append(String(key), $(fieldsName[key]).val());
        // }

        // 方式二
        var requestingData = $("#id_form").serializeArray();
        $.each(requestingData, function (index, data) {
            formdata.append(data.name, data.value);
        });
        formdata.append("file", $("#id_avatar_file").get(0).files[0]);
        $.ajax({
            url: "",
            type: "post",
            dataType: "json",
            contentType: false,
            processData: false,
            async: true,
            data: formdata,
            success: function (data, status, xhr) {
                if (!data["status"]) {
                     for (let key in data) {
                         if (key === "status") continue;
                         var selector = `[name=${key}]`;
                         $(selector).next().text(data[key]);
                         $(selector).parents("div[class='form-group class-form-group']").addClass("has-error");
                         $(selector).get(0).addEventListener("input", function () {
                             $(this).parents("div[class='form-group class-form-group has-error']").removeClass("has-error");
                             $(this).next().text("");
                         })
                     }
                } else {
                    location.href = data["msg"];
                }

            }
        });
    });

    // 头像预览功能
    $("#id_avatar_file").change(function (event) {
        // 1. 获取file对象
        var avatarImgObj = $(this).get(0).files[0];

        // 2. 实例化一个FileReader
        var reader = new FileReader();

        // 3. 获取图像文件路径
        reader.readAsDataURL(avatarImgObj);
        // reader.readAsBinaryString(avatarImgObj);

        // 4. 绑定事件，当读取完成后，给img的src赋值
        reader.onload = function () {  // 因为readAsDataURL的读取时间很长，而且与attr的操作是异步的，如果不添加onload事件，
            // 那么img的src值为unknown
            $("#id_avatar_img").attr("src", reader.result);
        };


    });
});