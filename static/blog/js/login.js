// {#        方式一#}
// {#        $(function () {#}
// {#            var btn = $('#id_btn_launch_myLoginModal');#}
// {#            $('#id_myLoginModal').modal({#}
// {#                keyboard: false,#}
// {#            });#}
// {#            btn.click(function (event) {#}
// {#                $('#id_myLoginModal').modal('show');#}
// {#            });#}
// {#            btn.triggerHandler('click');#}
// {#        });#}
// {#        方式二#}

$(function () {

    // 刷新验证码
    function flushCheckCode(obj) {
        $(obj).triggerHandler("click");
    }

    // 添加类
    function add(obj, str) {
        obj.addClass(str);
    }

    // 移除类
    function remove(obj, str) {
        obj.removeClass(str)
    }

    // 监听事件
    function addEvent(obj, event, func) {
        obj.get(0).addEventListener(event, func, false);
    }

    // 焦点事件
    function focusEvent(obj) {
        obj.focus();
    }

    // 选择事件
    function selectEvent(obj) {
        obj.select();
    }

    // 模态框启动部分
    var myModal = $("#id_myLoginModal");
    myModal.modal({
        keyboard: false,
    });
    myModal.modal("show");

    // 有时候地址栏刷新，JS文件不会改变
    // 可以尝试shift + 刷新

    // 验证码刷新部分
    var check_code_img = $("#id_check_code_img").get(0);
    var ori_src = check_code_img.src;
    var count = 0;
    check_code_img.onclick = function (event) {
        this.src = ori_src + "&count=" + count;
        count += 1;
    };

    // 登录按钮提交部分
    $("#id_btn_login").click(function (event) {
        // 1. 验证登录用户名和密码是否为空
        var divLoginNameFormGroup = $("#id_loginName_div");
        var divPasswordFormGroup = $("#id_password_div");
        var loginName = $("#id_login_name");
        var password = $("#id_pwd");
        var spanLoginNameFormGroupSub = $("#id_loginName_div span");
        var spanPasswordFormGroupSub = $("#id_password_div span");
        var inputLoinNameFormGroup = $("#id_loginName_div input");
        var inputPasswordFormGroup = $("#id_password_div input");
        var loginNameStatus = true;
        var passwordStatus = true;
        var hasError = "has-error";
        var hasFeedback = "has-feedback";
        var hidden = "hidden";

        // 1. 检测登录用户名是否为空
        if (!loginName.val()) {
            add(divLoginNameFormGroup, hasError);  // bootstrap表单校验状态效果显示 --> loginName
            remove(spanLoginNameFormGroupSub, hidden);
            addEvent(inputLoinNameFormGroup, "input", function () {  // 当获取输入的时候隐藏校验状态效果
                remove(divLoginNameFormGroup, hasError);
                add(spanLoginNameFormGroupSub, hidden);
            });
            loginNameStatus = false;
        }

        // 2. 检测密码是否为空
        if (!password.val()) {
            add(divPasswordFormGroup, hasError);  // bootstrap表单校验状态效果显示 --> password
            remove(spanPasswordFormGroupSub, hidden);
            addEvent(inputPasswordFormGroup, "input", function () {  // 当获取输入的时候隐藏校验状态效果
                remove(divPasswordFormGroup, hasError);
                add(spanPasswordFormGroupSub, hidden);
            });
            passwordStatus = false;
        }

        // 3. 给为空的input设置焦点获取
        if (!loginNameStatus) {
            focusEvent(inputLoinNameFormGroup);  // input ---> loginName
        } else if (!passwordStatus) {
            focusEvent(inputPasswordFormGroup);  // input ---> password
        } else {  // loginName和password都有值的情况下，提交请求
            $.ajax({
                url: "",  // http://127.0.0.1:8080/login/
                type: "post",
                async: true,  // 异步请求
                data: {
                    loginName: $("#id_login_name").val(),  // 登录名称
                    password: $("#id_pwd").val(),  // 密码
                    checkCode: $("#id_checkCode").val(),  // 验证码
                    csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),  // csrf_token
                },
                success: function (data, status, xhr) {
                    if (!data["check_code_status"]) {
                        // 1. 添加bootstrap表单校验状态
                        // 1.1 获取div(form-group)、div --> span、div --> input jQuery对象
                        var divCheckCodeFormGroup = $("#id_validate_checkCode");
                        var spanFormGroupSub = $("#id_validate_checkCode span");
                        var inputFormGroupSub = $("#id_validate_checkCode input");

                        // 1.2 显示校验状态效果
                        add(divCheckCodeFormGroup, hasError + ' ' + hasFeedback);  // 渲染bootstrap校验状态
                        remove(spanFormGroupSub, hidden);  // 移除hidden类，显示图标
                        focusEvent(inputFormGroupSub);  // 自动获取焦点
                        selectEvent(inputFormGroupSub);

                        // 1.3 按下清除按钮以及input框获得输入将隐藏校验状态效果
                        $("#id_btn_clear").click(function (event) {
                           inputFormGroupSub.val("");
                           focusEvent(inputFormGroupSub);
                           remove(divCheckCodeFormGroup, hasError + ' ' + hasFeedback);
                           add(spanFormGroupSub, hidden);
                        });
                        addEvent(inputFormGroupSub, "input", function () {
                            remove(divCheckCodeFormGroup, hasError + ' ' + hasFeedback);
                            add(spanFormGroupSub, hidden);
                        });

                        // 2. 更新验证码
                        flushCheckCode(check_code_img);
                    } else if (!data["auth_status"]) {
                        addEvent(inputLoinNameFormGroup, "input", function () {  // 当获取输入的时候隐藏校验状态效果
                            remove(divLoginNameFormGroup, hasError);
                            add(spanLoginNameFormGroupSub, hidden);
                            add(spanError, hidden);
                        });
                        addEvent(inputPasswordFormGroup, "input", function () {  // 当获取输入的时候隐藏校验状态效果
                            remove(divPasswordFormGroup, hasError);
                            add(spanPasswordFormGroupSub, hidden);
                            add(spanError, hidden);
                        });
                        var spanError = $("#id_error");
                        add(divLoginNameFormGroup, hasError);
                        add(divPasswordFormGroup, hasError);
                        add($("#id_error_div"), hasError);
                        remove(spanError, hidden);
                        spanError.html(data["msg"]);
                        flushCheckCode(check_code_img);
                    } else {
                        location.href = data["msg"];  // 验证正确，重定向到首页  http://127.0.0.1:8080/
                    }
                },
                error: function (xhr, data, status) {
                    console.log('error');
                },
            });
        }
    });


    $.ajax({
        url: "/pc-geetest/register?t=" + (new Date()).getTime(),
        type: "get",
        async: true,
        dataType: "json",
        success: function (data, status, xhr) {
            initGeetest({
                gt: data.gt,
                challenge: data.challenge,
                product: "popup",
                offline: !data.success,
            }, handlerPopup);
        },
    });
});