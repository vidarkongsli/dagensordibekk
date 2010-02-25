(function($){
	$.fn.comments = function(options) {
		var opts = $.extend({}, $.fn.comments.defaults, options);
		return this.each(function() {
			if (!(opts.urlPost && opts.urlGetAndDelete)) {
				alert("jQuery 'comments' plugin init failure. Url(s) not given");
				return false;
			}
			var headline = $('> h3 a', this);
			var list = $('> ul', this);
			var form = $('> form', this);
			var comment = $('textarea[name=kommentar]', form);
			var uri = $('input[name=uri]', form);
			
			function insertDataAndUpdateCommentsHeader(data) {
				list.empty().append(data);	
				var numberOfComments = list.children().size();
				var newText;
				if (numberOfComments == 0) {
					newText = "Ingen kommentarer";
				} else if (numberOfComments == 1) {
					newText = "Én kommentar";
				} else {
					newText = "" + numberOfComments + " kommentarer";
				}
				headline.text(newText);
			}
			
			$('button', form).click(function() {
				$.post(opts.urlPost, { 'kommentar':comment.val(), 'uri':uri.val() }, function(data) {
					insertDataAndUpdateCommentsHeader(data);
					comment.val("");
				},'html');
				return false;
			});
			
			$.get(opts.urlGetAndDelete, function (data) {
				insertDataAndUpdateCommentsHeader(data);
			}, 'html');
		});
	};
	
	$.fn.comments.defaults = {
	}
})(jQuery);