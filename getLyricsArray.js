var request = require('request');
var async = require('async');
var fs = require('fs');

var ourSongs = ["Crazy In Love", "Naughty Girl", "Baby Boy", "Daddy", "Get Me Bodied",
    "Upgrade U", "Freakum Dress", "Irreplaceable", "If I Were A Boy", "Halo",
    "Single Ladies (Put A Ring On It)", "Run The World (Girls)",
    "Drunk In Love", "Yoncé / Partition", "Formation", "Flawless"];

// very important shared mutable state for later.
var object = [];

// get page with links to all Beyonce lyrics.
request.get("http://www.azlyrics.com/k/knowles.html", function (error, response, body) {
    var links = body.split('\n')

    // empty all lines not containing links to song lyrics.
    .map(function (el) {
        if (el.substring(0, 33) === "<a href=\"../lyrics/beyonceknowles")
            return el;
        return null;
    })

    // filter out blanks
    .filter(function (el) {
        return (el !== null);
    })

    // empty out lines for songs other than ones we care about
    .map(function (el) {
        for (idx in ourSongs) {
            if (el.indexOf(ourSongs[idx]) > -1) {
                return el;
            }
        }

        return null;
    })

    // filter out blanks again
    .filter(function (el) {
        return (el !== null);
    })

    // get only the links
    .map(function (el) {
        return el.match(/"(.*?)"/)[1];
    })

    // make relative links full links
    .map(function (el) {
        return el.replace("..", "http://www.azlyrics.com");
    });

    // async loop to get each link
    async.each(links, function (link, cb) {
        return request.get(link, function (error, response, body) {
            var start = body.indexOf("<!-- Usage of azlyrics.com content by any third-party lyrics " 
                + "provider is prohibited by our licensing agreement. Sorry about that. -->");
            var end = body.indexOf("<!-- MxM banner -->");

            // get only the lyrics part of the page
            var result = body.substring(start, end)
            
            // remove "Usage of azlyrics.com content [...]" line
            .split("\n").slice(1)

            // removing html tags with regex :)
            .map(function (el) {
                return el.replace(/(<)((\/*)[A-Za-z /\/]*)(>)/g, "");
                // return el;
            })

            .map(function (el) {
                return el.trim();
            })

            // removing empty lines
            .filter(function (el) {
                return (!((el.indexOf('[') > -1) || el.length === 0));
            });

            // storing results in global array from earlier
            object = object.concat(result);
            cb(null);  // notify loop function (async.each) that we are done.
        });

    }, function () {

        // make safe for ascii default python 2 strings
        object = object.map(function cleanString(input) {
            var output = "";
            for (var i=0; i<input.length; i++) {
                if (input.charCodeAt(i) <= 127) {
                    output += input.charAt(i);
                }
            }
            return output;
        });

        // write stringified array to 'lyrics.txt'.
        return fs.writeFile('lyrics.txt', JSON.stringify(object), function () {
            console.log("done");
        });
    });
});
