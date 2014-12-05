$(document).ready(function() {
	$("#btn_predict").click(function() {
		var title = $("#title").val();
		var p_party = $("#proposing_party").val();
		var c_category = $("#case_category").val();
        var p_type = $("#proposal_type").val();
        var sum = $("#resume").val();
        alert("Hallo");
			$.ajax({
					url : "/query_folketinget/predict", 
					type : "POST",
                    cache : false,
					dataType: "text", 
					data : {
							title: title,
							proposing_party : p_party,
							case_category : c_category,
                            proposal_type : p_type,
                            summary : sum,
							csrfmiddlewaretoken: csrftoken
							},
					success : function(data) {
							$('#prediction_results').html(data);
					},
					error : function(xhr,errmsg,err) {
									alert(xhr.status + ": " + xhr.responseText);
					}
			});
			return false;
	});
});

