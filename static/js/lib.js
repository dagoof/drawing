var coord_data={'session_id':session_id, 'coordinates':{}};

function dumpdata(d){
    $.ajax({
        url:'/api/post',
        type:'POST',
        dataType:'json',
        contentType:'application/json; charset=utf-8',
        success:function(response){
            d.coordinates={};
        },
        data:JSON.stringify(d),
    });
}

function call_commit(){
    $.ajax({
        url:'/api/commit',
        type:'POST',
        dataType:'json',
        contentType:'application/json; charset=utf-8',
        success:function(response){
            coord_data._last_commit=(new Date()).getTime();
        },
        data:JSON.stringify(coord_data),
    });
}

$(document).mousemove(function(e){
    coord_data.coordinates[(new Date()).getTime()]=[e.pageX, e.pageY];
});

function dupdate(to, from){
    for(var e in from){
        to[e]=from[e];
    }
    return to;
}

function trigger_dumps(d, _cb, ms){
    setInterval(function(){
        _cb(d);
    }, ms);
}

$(function(){
    trigger_dumps(coord_data, dumpdata, 4000);

    $('#commit').bind('click', function(){
        call_commit();
    });
});
