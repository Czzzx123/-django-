$(function() {
    function bindCaptchaBtnClick() {
        $('#captcha-btn').click(function() {
            let $this = $(this);
            let email = $("input[name='email']").val();
            if (!email) {
                alert("请先输入邮箱！");   // ✅ 正确拼写
                return;
            }
            $this.off('click');

            //发送ajax请求
            $.ajax('/auth/captcha?email='+email,{
                method:'GET',
                success:function(result){
                    if(result['code'==200]){
                        alert('验证码发送成功！');
                    }else{
                        alert(result['message']);
                    }
                },
                fail:function(error){
                    console.log(error);
                }
            })

            let countdown = 60;
            let timer = setInterval(function() {
                if (countdown <= 0) {
                    $this.text("获取验证码");
                    clearInterval(timer);
                    bindCaptchaBtnClick(); // 倒计时结束重新绑定
                } else {
                    countdown--;
                    $this.text(countdown + "s");
                }
            }, 1000);
        });
    }
    bindCaptchaBtnClick();
});