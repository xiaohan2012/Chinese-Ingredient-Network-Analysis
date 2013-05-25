$(document).ready(function(){
    var list = $("#container ul")
    $(data).each(function(k, words){
	var li = $("<li>");
	var doms = words.map(function(word){
	    return "<li class='word ui-state-default'>" + word + "</li>";
	});
	console.log(words);
	li.html("<ul class='selectable word_sequence'>" + doms.join("") + "<div class='clear'></div></ul>");
	list.append(li);
    });

    $(".selectable").selectable();
});
