var express = require('express');
var app = express();

app.use(express.static(__dirname + '/public', {index: 'index.html'}));

console.log('Listening on http://localhost:8080');

app.listen(8080);
