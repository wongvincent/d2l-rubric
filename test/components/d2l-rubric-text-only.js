/* global suite, test, fixture, expect, suiteSetup, suiteTeardown, sinon */

'use strict';

suite('<d2l-rubric-text-only>', function() {

	var myElement, sandbox;
	function myAsyncFunction(callback) {
		// 500ms delay before callback
		setTimeout(function() {
		  callback(myElement);
		}, 500);
	  }

	suiteSetup(function() {
		sandbox = sinon.sandbox.create();
		myElement = fixture('rub-text-only');
	});

	suiteTeardown(function() {
		sandbox.restore();
	});

	suite('Text Only Rubric', function() {
		test('Out of container is hidden if using a text only rubric', function(done) {
			myAsyncFunction(function(myElement){
				var outOfContainer;
				outOfContainer = Polymer.dom(myElement.root).querySelector('.out-of-container');
				expect(outOfContainer.attributes).to.have.ownProperty('hidden');
				done();
			});
		});
	});
});
