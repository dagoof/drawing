var coord_data={'session_id':session_id, 'coordinates':{}};

function dumpdata(d){
    $.ajax({
        url:'/api/post',
        type:'POST',
        dataType:'json',
        contentType:'application/json; charset=utf-8',
        success:function(response){
            alert('success');
            d.coordinates={};
        },
        data:JSON.stringify(d),
    });
}

$(document).mousemove(function(e){
    coord_data.coordinates[(new Date()).getTime()]=[e.pageX, e.pageY];
});

function trigger_dumps(d, _cb, ms){
    setInterval(function(){
        _cb(d);
    }, ms);
}

$(function(){
    trigger_dumps(coord_data, dumpdata, 4000);
});
