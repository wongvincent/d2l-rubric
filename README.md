# d2l-rubric
[![Build Status](https://travis-ci.org/Brightspace/d2l-rubric.svg?branch=master)](https://travis-ci.org/Brightspace/d2l-rubric)

Polymer based web-component to display a rubric

## Usage
Include the [webcomponents.js](http://webcomponents.org/polyfills/) "lite" polyfill (for browsers who don't natively support web components), then import `d2l-rubric.html`:

```html
<head>
	<link rel="import" href="../d2l-rubric/d2l-rubric.html">
	<d2l-rubric href="href for rubric" token="User token"/>
</head>
```

## Viewing Your Element

```
$ npm run serve
```

Modify [demo/index.html](https://github.com/Brightspace/d2l-rubric/blob/master/demo/index.html) and supply your href and token.

## Running Tests

```
$ polymer test
```

Your application is already set up to be tested via [web-component-tester](https://github.com/Polymer/web-component-tester). Run `polymer test` to run your application's test suite locally.
