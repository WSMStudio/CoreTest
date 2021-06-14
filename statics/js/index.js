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
                var len = response.data.length
                for (var i = 0; i < len; i ++) {
                    list += "<li>" + response.data[i] + "</li>";
                }
                $("#result_list").html(list);
                $("#search_input").val("");
                return false;
            }
        });
    }
    $('#search_input').bind('keypress', function(event) {
        if (event.keyCode == "13") { search_func(event); }});
    $("#search_btn").click(function(event){ search_func(event); });
});