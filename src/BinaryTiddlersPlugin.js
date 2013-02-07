/***
|''Name''|BinaryTiddlersPlugin|
|''Description''|renders base64-encoded binary tiddlers as images or links|
|''Author''|FND|
|''Version''|0.3.2|
|''Status''|@@beta@@|
|''Source''|http://svn.tiddlywiki.org/Trunk/association/plugins/BinaryTiddlersPlugin.js|
|''License''|[[BSD|http://www.opensource.org/licenses/bsd-license.php]]|
|''CoreVersion''|2.5|
!Code
***/
//{{{
(function($) {

var ctfield = "server.content-type";

var plugin = config.extensions.BinaryTiddlersPlugin = {
	isWikiText: function(tiddler) {
		var ctype = tiddler.fields[ctfield];
		if(ctype) {
			return !this.isBinary(tiddler) && !this.isTextual(ctype);
		} else {
			return true;
		}
	},
	// NB: pseudo-binaries are considered non-binary here
	isBinary: function(tiddler) {
		var ctype = tiddler.fields[ctfield];
		return ctype ? !this.isTextual(ctype) : false;
	},
	isTextual: function(ctype) {
		return ctype.indexOf("text/") == 0
			|| this.endsWith(ctype, "+xml")
			|| ctype == 'application/json'
			|| ctype == 'application/javascript';
	},
	endsWith: function(str, suffix) {
		return str.length >= suffix.length &&
			str.substr(str.length - suffix.length) == suffix;
	},
        isLink: function(tiddler) {
            return this.isBinary(tiddler) && tiddler.text.indexOf("<html>") != -1
        }
};

// Disable edit for linked tiddlers (for now)
// This will be changed to a GET then PUT
config.commands.editTiddler.isEnabled = function(tiddler) {
    var existingTest = config.commands.editTiddler.isEnabled;
    if (existingTest) {
        return existingTest && !plugin.isLink(tiddler);
    } else {
        return !plugin.isLink(tiddler);
    }
};

// hijack text viewer to add special handling for binary tiddlers
var _view = config.macros.view.views.wikified;
config.macros.view.views.wikified = function(value, place, params, wikifier,
		paramString, tiddler) {
	var ctype = tiddler.fields["server.content-type"];
	if(params[0] == "text" && ctype && !tiddler.tags.contains("systemConfig") && !plugin.isLink(tiddler)) {
		var el;
		if(plugin.isBinary(tiddler)) {
			var uri = "data:%0;base64,%1".format([ctype, tiddler.text]); // TODO: fallback for legacy browsers
			if(ctype.indexOf("image/") == 0) {
				el = $("<img />").attr("alt", tiddler.title).attr("src", uri);
			} else {
				el = $("<a />").attr("href", uri).text(tiddler.title);
			}
		} else {
			el = $("<pre />").text(tiddler.text);
		}
		el.appendTo(place);
	} else {
		_view.apply(this, arguments);
	}
};

// hijack edit macro to disable editing of binary tiddlers' body
var _editHandler = config.macros.edit.handler;
config.macros.edit.handler = function(place, macroName, params, wikifier,
		paramString, tiddler) {
	if(params[0] == "text" && plugin.isBinary(tiddler)) {
		return false;
	} else {
		_editHandler.apply(this, arguments);
	}
};

// hijack autoLinkWikiWords to ignore binary tiddlers
var _autoLink = Tiddler.prototype.autoLinkWikiWords;
Tiddler.prototype.autoLinkWikiWords = function() {
	return plugin.isWikiText(this) ? _autoLink.apply(this, arguments) : false;
};

})(jQuery);
//}}}
