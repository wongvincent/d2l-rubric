# d2l-rubric
[![Build Status](https://travis-ci.org/Brightspace/d2l-rubric.svg?branch=master)](https://travis-ci.org/Brightspace/d2l-rubric)

Polymer based web-component to display a rubric

## Usage
Include the [webcomponents.js](http://webcomponents.org/polyfills/) "lite" polyfill (for browsers who don't natively support web components), then import `d2l-rubric.html`:

##### Display a Rubric without it's title:
```html
<head>
	<link rel="import" href="../d2l-rubric/d2l-rubric.html">
	<d2l-rubric href="href for rubric" token="User token"/>
</head>
```
##### Display a Rubric with it's title:
```html
<head>
	<link rel="import" href="../d2l-rubric/d2l-rubric.html">
	<link rel="import" href="../d2l-rubric/d2l-rubric-title.html">
	<d2l-rubric href="href for rubric" token="User token">
		<h3>
			<d2l-rubric-title href="href for rubric" token="User token"/>
		</h3>
	</d2l-rubric>
</head>
```

## Viewing Your Element

```
$ polymer serve
```

The demo can be viewed at http://127.0.0.1:8081/components/d2l-rubric/demo/index.html

## Running Tests

```
$ npm run test:wct:local
```
#### Updating Test and Demo Data
The data used for the demo and for running test can be updated from QA sites.

```
$ npm run regenerate_data <qa site url> <daily pwd> (optional: copy_files)
```
If the optional argument copy_files is specified, the generated files will be automatically copied to the demo and test folders, otherwise they will stay in the regen_api_data folder
