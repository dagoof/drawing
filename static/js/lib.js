var coord_data={'session_id':session_id, 'coordinates':{}};
var pending_data={'session_id':session_id, 'data': {}};

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
            pending_data._last_commit=(new Date()).getTime();
            pending_data.data={}
        },
        data:JSON.stringify(pending_data),
    });
}

/*
$(document).mousemove(function(e){
    coord_data.coordinates[(new Date()).getTime()]=[e.pageX, e.pageY];
});
*/

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
    //trigger_dumps(coord_data, dumpdata, 4000);

    $('.option').bind('click', function(){
        ting=pending_data.data[$(this).text()] || {};
        ting[(new Date()).getTime()]=(new Date()).getTime();
        pending_data.data[$(this).text()]=ting;
    });

    $('#commit').bind('click', function(){
        call_commit();
    });
});
