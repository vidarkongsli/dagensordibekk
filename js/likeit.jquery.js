(function($) {

	function vis(element) {
		element.removeClass('hidden').addClass('visible');
	}
		
	function skjul(element) {
		element.removeClass('visible').addClass('hidden');
	}
	
	$.fn.likeIt = function(options) {
		var opts = $.extend({}, $.fn.likeIt.defaults, options);
	
		return this.each(function () {
			var doesNotLikeItSection = $('li:first', this);
			var likesItSection = $('+li', doesNotLikeItSection);
			
			var numberOfLikesElement = $(opts.numberOfLikesSelector, this.ownerDocument);
			
			function oppdaterLikerVisning(data) {
				if (data.errorCode != 0) {
					alert('Dette er flaut. Noe uforutsett skjedde. Feilkode=' + data.errorCode);
				}
				if (data.likerDuOrdet) {
					skjul(doesNotLikeItSection);
					vis(likesItSection);
				} else {
					vis(doesNotLikeItSection);
					skjul(likesItSection);
				}
				if (data.numberOfLikes != 0) {
					numberOfLikesElement.text(", " + data.numberOfLikes + " person" + (data.numberOfLikes == 1 ? "" : "er") + " liker dette ordet");
				} else numberOfLikesElement.text('');
			}
			
			$.getJSON(opts.urlGetAndDelete, oppdaterLikerVisning);
		
			$('a', doesNotLikeItSection).click(function() {
				$.post(opts.urlPost, { 'uri':$('#kommentar-uri').val() }, oppdaterLikerVisning, 'json');
			});
	
			$('a', likesItSection).click(function() {
				$.ajax({
					url 	: opts.urlGetAndDelete,
					type 	: 'delete',
					dataType: 'json',
					success	: oppdaterLikerVisning
				});
			});
		});
	};
	
	$.fn.likeIt.defaults = {
		numberOfLikesSelector : '#numberOfLikes'
	};
})(jQuery);