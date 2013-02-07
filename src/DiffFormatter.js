/***
|''Name''|DiffFormatter|
|''Description''|highlighting of text comparisons|
|''Author''|FND|
|''Version''|0.9.0|
|''Status''|beta|
|''Source''|http://svn.tiddlywiki.org/Trunk/contributors/FND/formatters/DiffFormatter.js|
|''CodeRepository''|http://svn.tiddlywiki.org/Trunk/contributors/FND/|
|''License''|[[BSD|http://www.opensource.org/licenses/bsd-license.php]]|
|''Keywords''|formatting|
!Description
Highlights changes in a unified [[diff|http://en.wikipedia.org/wiki/Diff#Unified_format]].
!Notes
Based on Martin Budden's [[DiffFormatterPlugin|http://svn.tiddlywiki.org/Trunk/contributors/MartinBudden/formatters/DiffFormatterPlugin.js]].
!Usage
The formatter is applied to blocks wrapped in <html><code>{{{diff{..}}}</code></html> within tiddlers tagged with "diff".
!Revision History
!!v0.9 (2010-04-07)
* initial release; fork of DiffFormatterPlugin
!StyleSheet
.diff { white-space: pre; font-family: monospace; }
.diff ins, .diff del { display: block; text-decoration: none; }
.diff ins { background-color: #dfd; }
.diff del { background-color: #fdd; }
.diff .highlight { background-color: [[ColorPalette::SecondaryPale]]; }
!Code
***/
//{{{
(function() {

config.shadowTiddlers.StyleSheetDiffFormatter = store.getTiddlerText(tiddler.title + "##StyleSheet");
store.addNotification("StyleSheetDiffFormatter", refreshStyles);

var formatters = [{
		name: "diffWrapper",
		match: "^\\{\\{diff\\{\n", // XXX: suboptimal
		termRegExp: /(.*\}\}\})$/mg,
		handler: function(w) {
			var el = createTiddlyElement(w.output, "div", null, "diff");
			w.subWikifyTerm(el, this.termRegExp);
		}
	}, {
		name: "diffRange",
		match: "^(?:@@|[+\\-]{3}) ",
		lookaheadRegExp: /^(?:@@|[+\-]{3}) .*\n/mg,
		handler: function(w) {
			createTiddlyElement(w.output, "div", null, "highlight").
				innerHTML = "&#8230;";
			this.lookaheadRegExp.lastIndex = w.matchStart;
			var lookaheadMatch = this.lookaheadRegExp.exec(w.source);
			if(lookaheadMatch && lookaheadMatch.index == w.matchStart) {
				w.nextMatch = this.lookaheadRegExp.lastIndex;
			}
		}
	}, {
		name: "diffAdded",
		match: "^\\+",
		termRegExp: /(\n)/mg,
		handler: function(w) {
			var el = createTiddlyElement(w.output, "ins", null, "added");
			w.subWikifyTerm(el, this.termRegExp);
		}
	}, {
		name: "diffRemoved",
		match: "^-",
		termRegExp: /(\n)/mg,
		handler: function(w) {
			var el = createTiddlyElement(w.output, "del", null, "removed");
			w.subWikifyTerm(el, this.termRegExp);
		}
	}
];

config.parsers.diffFormatter = new Formatter(formatters);
config.parsers.diffFormatter.format = "diff";
config.parsers.diffFormatter.formatTag = "diff";

})();
//}}}
