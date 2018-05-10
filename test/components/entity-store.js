/* global suite, test, expect, suiteSetup, suiteTeardown, sinon */

'use strict';

suite('entity-store', function() {

	var sandbox;

	suiteSetup(function() {
		sandbox = sinon.sandbox.create();
	});

	suiteTeardown(function() {
		sandbox.restore();
	});

	suite('smoke test', function() {

		test('can fetch leaf entity', function(done) {
			window.D2L.Rubric.EntityStore.addListener(
				'data/rubrics/organizations/text-only/199/groups/176/criteria/623/0.json',
				'foozleberries',
				function(entity) {
					var description = entity && entity.getSubEntityByClass('description').properties.html;
					expect(description).to.equal('Proper use of grammar');
					if (!done.done) {
						done();
						done.done = true;
					}
				});
			window.D2L.Rubric.EntityStore.fetch('data/rubrics/organizations/text-only/199/groups/176/criteria/623/0.json', 'foozleberries');
		});

		test('expands embedded entity children', function(done) {
			window.D2L.Rubric.EntityStore.addListener(
				'data/rubrics/organizations/text-only/199/groups/176/criteria/623/0.json',
				'foozleberries',
				function(entity) {
					var description = entity && entity.getSubEntityByClass('description').properties.html;
					expect(description).to.equal('Proper use of grammar');
					if (!done.done) {
						done();
						done.done = true;
					}
				});
			window.D2L.Rubric.EntityStore.fetch('data/rubrics/organizations/text-only/199/groups/176/criteria/623.json', 'foozleberries');
		});

		test('expands embedded entity descendants', function(done) {
			window.D2L.Rubric.EntityStore.addListener(
				'data/rubrics/organizations/text-only/199/groups/176/criteria/623/0.json',
				'foozleberries',
				function(entity) {
					var description = entity && entity.getSubEntityByClass('description').properties.html;
					expect(description).to.equal('Proper use of grammar');
					if (!done.done) {
						done();
						done.done = true;
					}
				});
			window.D2L.Rubric.EntityStore.fetch('data/rubrics/organizations/text-only/199/groups/176/criteria.json', 'foozleberries');
		});
	});
});
