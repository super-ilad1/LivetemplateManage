function createNew() {
    $('#createNew').removeClass('hide');

}

//<editor-fold desc="删除弹出窗口">
//cancel create new FIle register
function cancelcreateNew() {
    $("#createNew").addClass('hide');
}

function cancelInsert() {
    $('#insertDiv').addClass('hide');

}

function canceldelete() {

    $('#deleteFile').addClass('hide');

}

//</editor-fold>


//<editor-fold desc="删除功能">
//窗口删除确认
function Delete() {
    var updatedId = $('#real_content div').first().attr('id').replace('content', '');
    console.log("1--updatedId: ", updatedId);
    //查找title中的最后一个id，如果updatedId是最后一个id，那么新显示的id要下调
    var lastId = $('#title a').last().attr('id').replace('title', '');
    console.log("1--lastId: ", lastId);


    $.ajax({
        data: {"id": updatedId},
        url: '/delete/',
        type: 'POST',
        success: function (data) {
            $('#title').html(data);

        }
    });

    // showFromID
    $.ajax({
        data: {'id': updatedId, "lastId": lastId},
        url: '/selectContent/delete/',
        type: "POST",
        success: function (data) {
            $('#real_content').html(data);

        }

    });


}

//真的删除
function certainDelete() {

    console.log($('.display div[class="select"] #value').text());


//    删除窗口
    $('#deleteFile').addClass('hide');

}

//</editor-fold>

function Insert() {

    //插入的时候你也要更新当前的编辑框的信息啊
    updateCurrentEdit();


    //<editor-fold desc="Ajax增加一个多的空项">
    $.ajax({
            url: '/insert/',
            data: {},
            type: "POST",
            success: function (data) {
                $('#title').html(data);


            }
        }
    );


    //</editor-fold>


    //<editor-fold desc="增加了新的项那就要对应的显示他">


    $.ajax({
        data: {'id': 3},
        url: '/selectContent/insert/',
        type: "POST",
        success: function (data) {
            $('#real_content').html(data);

        }

    });
    //</editor-fold>


}

//<editor-fold desc="插入功能">
function sendInsert() {
    //<editor-fold desc="获取指定元素的value">
    var pathname = window.location.pathname;
    var title = $("#insertDiv input[name=name]").val();
    var desc = $("#insertDiv input[name=desc]").val();
    var envi = $("#insertDiv select[name=envi]").val();
    var contents = $("#insertDiv textarea[name=contents]").val();
    //</editor-fold>

    //<editor-fold desc="print上面元素的值">
    console.log("title: ", title);
    console.log("pathname: ", pathname);
    console.log("desc: ", desc);
    console.log("envi: ", envi);
    console.log("contents: ", contents);
    //</editor-fold>

    //<editor-fold desc="Ajax传输数据">
    $.ajax({
        data: {"title": title, "desc": desc, "envi": envi, "contents": contents, "pathname": pathname},
        url: '/insert/',
        type: 'POST',
        dataType: 'html',
        success: function (infos) {
            console.log('Return');
            console.log(infos);
            $('#wrapper').html(infos);

            cancelInsert();


        }

    })
    //</editor-fold>
}

//</editor-fold>

function detectInput() {
    console.log("input");

    var id = $('#real_content div').first().attr('id').replace('content', '');
    $('#title' + id).text($('#NameInput').val())


}


$(document).ready(function () {
    $('#NameInput').keyup(function () {
        console.log("input");
        $('#title').last().text($('#NameInput').val())
    });
});

$(document).ready(function () {
    // $('#NameInput').on('input', function (e) {


    // });
});