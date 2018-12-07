require('dotenv').config();

var express = require('express');
var app = express();
var ejsLayouts = require("express-ejs-layouts");
var favicon = require('serve-favicon');
var contentful = require('contentful');

app.set('port', (process.env.PORT || 7000));

app.use(express.static(__dirname + '/public'));
app.use(ejsLayouts);
//app.use(favicon('favicon.png'));

// views is directory for all template files
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');


var index = require('./routes/index.js');

app.use('/', index);

// Handle unhandled routes
app.use(function (req, res, next) {
    next({
        status: 404,
        message: 'Not Found'
    });
});

// General error handling
app.use(function (err, req, res, next) {
    console.log(err.status);
    if (!err.message && err.statusText) {
        err.message = err.statusText;
    }
    if (err.status == 404) {
        res.status(404).render('error', {
            error: err
        });
    } else {
        res.status(500).render('error', {
            error: err
        });
    }
});

app.listen(app.get('port'), function () {
    console.log('Node app is running on port', app.get('port'));
});