$(function(){
    $('.spamshit').bind('click', function(){
        $.ajax({
            url:'/api/post',
            type:'POST',
            dataType:'json',
            contentType:'application/json; charset=utf-8',
            success:function(response){
                
            },
            data:JSON.stringify({'this is some shit':'why cant you own so much','yeap':$(this).text()}),
        });
    });
});
