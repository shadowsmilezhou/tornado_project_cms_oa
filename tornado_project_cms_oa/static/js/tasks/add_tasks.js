/**
 * Created by Administrator on 2018/1/28/028.
 */
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]

}

$(document).ready(function () {
    $('#submit-article-btn').click(function () {
        //获取输入函数

        var content = $('#task_content').val();
        var category = $('#category-select').val();

        console.log(content,category);
        $.ajax({
            'url': '/tasks/publisher',
            'type': 'post',
            'data': {

                'category_id':category,
                'content': content,

            },
            'headers': {
                "X-XSRFTOKEN":get_cookie("_xsrf")
            },
            'success': function (data) {
                if (data['status'] == 200) {
                    swal({
                        'title': '正确',
                        'text': data['msg'],
                        'type': 'success',
                        'showCancelButton': false,
                        'showConfirmButton': false,
                        'timer': 1000,
                    },function () {
                       window.location = '/tasks/publisher';
                    });
                }else{
                    swal({
                        'title': '错误',
                        'text': data['msg'],
                        'type': 'error',
                        'showCancelButton': false,
                        'showConfirmButton': false,
                        'timer': 1000,
                    })
                }
            }
        })
    });
});