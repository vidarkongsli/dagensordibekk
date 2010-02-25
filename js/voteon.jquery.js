(function($){
	$.fn.voteOn = function(options) {
		var opts = $.extend({}, $.fn.voteOn.defaults, options);
		return this.each(function() {
			if (!(opts.urlPost))
			{
				alert("jQuery 'voteOn' plugin config error. 'urlPost' not given");
				return false;
			}
			var context = this;
			
			function avgiStemme(ordId, stemmeFor ) {
				$.post(opts.urlPost, { 'ord-nokkel' : ordId, 'erStemmeFor' : stemmeFor }, function(data) {
					if (data.errorCode == 0) {
						$('span.stemme' + (stemmeFor?'for':'mot'), context).text(data.antallStemmer);
						$('.message', context).text("Din stemme er registert.");
						$('.message', context).show();
					} else if (data.errorCode == 1) {
						alert('Dette er flaut. Det ser ut som at ordet ikke fins i databasen. Noe må ha gått galt...');
					} else {
						$('.errormessage', context).text("Du har allerede stemt på dette ordet.");
						$('.errormessage', context).show();
					}
				}, 'json');
			}			
			
			var ordId = this.id.split('-')[1];
			$('a.stemmefor', this).click(function() {
				avgiStemme(ordId, true);
				return false;
			});
			$('a.stemmemot', this).click(function() {
				avgiStemme(ordId, false);
				return false;
			});
		});
	};
	$.fn.voteOn.defaults = {
	}
})(jQuery);