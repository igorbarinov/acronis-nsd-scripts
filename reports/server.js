var express = require('express');
var app = express();

app.use(express.static(__dirname + '/public', {index: 'index.html'}));

console.log('Listening on http://0.0.0.0:8085');

app.listen(8085);
