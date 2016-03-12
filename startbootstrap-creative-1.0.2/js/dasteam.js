/*!
 * Start Bootstrap - Creative Bootstrap Theme (http://startbootstrap.com)
 * Code licensed under the Apache License v2.0.
 * For details, see http://www.apache.org/licenses/LICENSE-2.0.
 */

(function ($) {

	"use strict"; // Start of use strict
	
	//Tipped Tooltips
	$(document).ready(function () {
		Tipped.create('#javiTooltip', 'As a group, we are indebted to him for his efforts in compiling the reports and tying up loose ends wherever gaps have been left. The backbone of NeuroSpell, his organisation and resolve have resulted in the smooth running of the project.', {
			position: 'bottom',
			hideOthers: 'true',
			fadeIn: 500,
			offset: {y:23},
			maxWidth: 250
		});
		Tipped.create('#nicoTooltip', 'The mastermind behind the whole project. Responsible for the bigger picture, directing and coordinating, as well as researching the background and principles of operation of BCI. A man with a plan, he will stop at nothing to achieve his goal.', {
			position: 'bottomleft',
			hideOthers: 'true',
			fadeIn: 500,
			offset: {y:20},
			maxWidth: 200
		});
		Tipped.create('#aaronTooltip', 'Whether designing the next script for our interface or chuckling at a piece of code, nobody dares question the flawless technique of one of our top developers – partly out of respect, partly out of fear.', {
			position: 'left',
			hideOthers: 'true',
			fadeIn: 500,
			maxWidth: 200
		});
		Tipped.create('#samTooltip', 'The legal representative of the group - arranging meetings with postgraduates and professors, in addition to booking hours of intense development sessions in the laboratory for crucial testing and implementation using the Emotiv.', {
			position: 'leftbottom',
			hideOthers: 'true',
			fadeIn: 500,
			maxWidth: 200
		});
		Tipped.create('#jornTooltip', "With his unparallelled knowledge of HTML and style sheets, he has taken charge of our cyber identity and online presence.  He is the 'Sell' in NeuroSpell, and is primarily responsible for putting the company into the public eye.", {
			position: 'right',
			hideOthers: 'true',
			fadeIn: 500,
			maxWidth: 200
		});
		Tipped.create('#junTooltip', "As well as designing the User Interface for our project, his prowess in 3D design has led to an array of interesting and attractive strongboxes to keep our circuitry safe from damage – modern craftsmanship at its finest.", {
			position: 'bottomright',
			hideOthers: 'true',
			fadeIn: 500,
			offset: {y:20},
			maxWidth: 200
		});
		Tipped.create('#vinayTooltip', "Head of testing and development of hardware, his unique solutions to unforeseen obstacles are the reason our product exists today. He attests to the fact that any problem can be solved with a voltmeter and a little bit of faith.", {
			position: 'rightbottom',
			hideOthers: 'true',
			fadeIn: 500,
			maxWidth: 200
		});
	});
	
	// jQuery for page scrolling feature - requires jQuery Easing plugin
	$('a.page-scroll').bind('click', function (event) {
		var $anchor = $(this);
		$('html, body').stop().animate({
			scrollTop: ($($anchor.attr('href')).offset().top - 50)
		}, 1250, 'easeInOutExpo');
		event.preventDefault();
	});

	// Highlight the top nav as scrolling occurs
	$('body').scrollspy({
		target: '.navbar-fixed-top',
		offset: 0
	});

	// Closes the Responsive Menu on Menu Item Click
	$('.navbar-collapse ul li a').click(function () {
		$('.navbar-toggle:visible').click();
	});

	// Fit Text Plugin for Main Header
	$("h1").fitText(
		1.2, {
			minFontSize: '35px',
			maxFontSize: '65px'
		}
	);

	// Offset for Main Navigation
	$('#mainNav').affix({
		offset: {
			top: 100
		}
	})

	// Initialize WOW.js Scrolling Animations
	new WOW().init();

})(jQuery); // End of use strict
