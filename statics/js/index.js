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
                var len = response.data.length;
                if (len == 0) {
                    list = "No result found !";
                } else {
                    for (var i = 0; i < len; i++) {
                        list += "<a href='#' class='list-group-item list-group-item-action'><span class='from'>Document " 
                        + response.data[i][1] + "</span> ... " + response.data[i][0] + " ... </a>";
                    }
                }
                $("#result_list").html(list);
                $("#search_input").val("");
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