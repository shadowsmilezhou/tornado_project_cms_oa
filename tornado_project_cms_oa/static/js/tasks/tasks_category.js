// /**
//  * Created by Administrator on 2018/1/28/028.
//  */
// /**
//  * Created by Administrator on 2018/1/28/028.
//  */
// function get_cookie(name) {
//     var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
//     return xsrf_cookies[1]
//
// }
//
// $(document).ready(function () {
//     $('#tasks-category-btn').click(function () {
//         //获取输入函数
//         event.preventDefault();
//         // var content = $('#task_content').val();
//         var category = $('#category-select').val();
//
//         console.log(category);
//         $.ajax({
//             'url': '/tasks/accept',
//             'type': 'post',
//             'data': {
//
//                 'category_id':category,
//                 // 'content': content,
//
//             },
//             'headers': {
//                 "X-XSRFTOKEN":get_cookie("_xsrf")
//             },
//             'success': function (data) {
//                 window.location = '/tasks/accept';
//             }
//         })
//     });
// });
