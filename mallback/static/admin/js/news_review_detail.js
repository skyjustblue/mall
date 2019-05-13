function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function(){
    $(".news_review").submit(function (e) {
        e.preventDefault()

        var ctoken = $(".csrf_token").val()
        var id = $(".news_id").val()
        var action = $("input[name='action']:checked").val()
        var reason = $("input[name='reason']").val()


        params = {
            'csrf_token':ctoken,
            'id':id,
            'action':action,
            'reason':reason
        }

        // TODO 新闻审核提交
        $.ajax({
            url:'/admin/news_review_detail',
            type:'POST',
            data:params,
            dataType:'json',
            success:function(res){
                if(res.errno == '200'){
                    window.location.href="http://127.0.0.1:5000/admin/newsreview"
                }else{
                    alert(res.errmsg);
                }
            }

        })

    })
})

// 点击取消，返回上一页
function cancel() {
    history.go(-1)
}