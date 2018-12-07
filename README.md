# Simple website template with Contentful

Created by Nina Cecilie Højholdt

### Setup info 🍊 ###

This setup uses NodeJS, and [ExpressJS](http://expressjs.com/) is used for routing.  
 [EJS](http://www.embeddedjs.com/) is used as the templating language.

GulpJS is used for SCSS compiling and JS minifying, and a .gulpfile for this is included.

The template also comes with jQuery and an empty JS file included.


### Setting up the project ###
- Download/fork the repo, navigate to it, and run *npm install* in the terminal  
(make sure you have node installed first)

- To start the server, run *npm start* in the terminal. Navigate to http://localhost:7000/ and everything should be working 🙏 

Going to http://localhost:7000/ will render the index.ejs file.


To use the gulp setup, run *gulp* in another terminal tab.
I recommend installing the [Livereload](https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei) Chrome plugin, which works with the gulp task.
