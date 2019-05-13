$(function(){
    var $a = $('.edit');
    var $add = $('.addtype');
    var $delete = $('.delete');
    var $pop = $('.pop_con');
    var $cancel = $('.cancel');
    var $confirm = $('.confirm');
    var $error = $('.error_tip');
    var $input = $('.input_txt3');
    var sHandler = 'edit';
    var sId = 0;

    $a.click(function(){
        sHandler = 'edit';
        sId = $(this).parent().siblings().eq(0).html();
        $pop.find('h3').html('修改分类');
        $pop.find('.input_txt3').val($(this).parent().prev().html());
        $pop.show();
    });

    $add.click(function(){
        sHandler = 'add';
        $pop.find('h3').html('新增分类');
        $input.val('');
        $pop.show();
    });

    $delete.click(function(){
           if(confirm("确定要删除吗?")){
            var cstoken = $('.csrf_token').val();
            //ajax请求删除
            sId = $(this).parent().siblings().eq(0).html();
            params = {
                "id": sId,
                "csrf_token":cstoken
            };
            ajax_post('/admin/deletecate',params)
           }
    });

    $cancel.click(function(){
        $pop.hide();
        $error.hide();
    });

    $input.click(function(){
        $error.hide();
    });

    $confirm.click(function(){
        //修改
        if(sHandler=='edit')
        {
            
        }
        else
        {
            //添加
            var name = $input.val()
            var token = $('.csrf_token').val()

            var param = {'name':name,'csrf_token':token}
            $.ajax({
                url:'/admin/addcate',
                type:'post',
                data:param,
                dataType:'json',
                success:function(res){
                    console.log(res)
                    if(res.code == 200){
                        window.location.reload()
                    }else{
                        alert(res.message)
                    }
                }

            })
            
        }
      

    })

    function ajax_post(url,params){
         //jquery ajax提交数据
        $.ajax({
            url:url,
            type:'POST',
            data:params,
            dataType:'json',
            success:function(res){
            console.log(res)
                if(res.code == 200){
                    location.reload();
                }else{
                    $error.html(res.message).show();
                }
            }

        })
    }
})