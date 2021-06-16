$(function() {
    function search_func(event) {
        event.preventDefault();
        $.ajax({
            method: "POST",
            url: "/search",
            data: {
                "query": $("#search_input").val()
            },
            success: function(response) {
                console.log(response);
                var list = "";
                var flag = true;
                for (var doc_id in response.data) {
                    list += "<li style='list-style: none;'><a class='from'>Document " + doc_id.toString() + "</a><ul class='list-group'>";
                    for (var ans in response.data[doc_id]) {
                        list += "<a class='list-group-item list-group-item-action'>... " + response.data[doc_id][ans] + " ... </a>";
                    }
                    list += "</ul></li>";
                    flag = false;
                }
                if (flag) {
                    list = "No result found !";
                }
                $("#result_list").hide()
                $("#result_list").html(list);
                $("#result_list").fadeIn(500);
                $('#search_input').focus().select();
                return false;
            }
        });
    }
    $('#search_input').bind('keypress', function(event) {
        if (event.keyCode == "13") {
            search_func(event);
        }
    });
    $("#search_btn").click(function(event) {
        search_func(event);
    });
});