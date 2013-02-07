/***
|''Name''|ServerSideSavingPlugin|
|''Description''|server-side saving|
|''Author''|FND|
|''Version''|0.6.5|
|''Status''|stable|
|''Source''|http://svn.tiddlywiki.org/Trunk/association/plugins/ServerSideSavingPlugin.js|
|''License''|[[BSD|http://www.opensource.org/licenses/bsd-license.php]]|
|''CoreVersion''|2.5.3|
|''Keywords''|serverSide|
!Notes
This plugin relies on a dedicated adaptor to be present.
The specific nature of this plugin depends on the respective server.
!Revision History
!!v0.1 (2008-11-24)
* initial release
!!v0.2 (2008-12-01)
* added support for local saving
!!v0.3 (2008-12-03)
* added Save to Web macro for manual synchronization
!!v0.4 (2009-01-15)
* removed ServerConfig dependency by detecting server type from the respective tiddlers
!!v0.5 (2009-08-25)
* raised CoreVersion to 2.5.3 to take advantage of core fixes
!!v0.6 (2010-04-21)
* added notification about cross-domain restrictions to ImportTiddlers
!To Do
* conflict detection/resolution
* rename to ServerLinkPlugin?
* document deletion/renaming convention
!Code
***/
//{{{
(function($) {

readOnly = false; //# enable editing over HTTP

var plugin = config.extensions.ServerSideSavingPlugin = {};

plugin.locale = {
	saved: "%0 saved successfully",
	saveError: "Error saving %0: %1",
	saveConflict: "Error saving %0: edit conflict",
	deleted: "Removed %0",
	deleteError: "Error removing %0: %1",
	deleteLocalError: "Error removing %0 locally",
	removedNotice: "This tiddler has been deleted.",
	connectionError: "connection could not be established",
	hostError: "Unable to import from this location due to cross-domain restrictions."
};

plugin.sync = function(tiddlers) {
	tiddlers = tiddlers && tiddlers[0] ? tiddlers : store.getTiddlers();
	$.each(tiddlers, function(i, tiddler) {
		var changecount = parseInt(tiddler.fields.changecount, 10);
		if(tiddler.fields.deleted === "true" && changecount === 1) {
			plugin.removeTiddler(tiddler);
		} else if(tiddler.isTouched() && !tiddler.doNotSave() &&
				tiddler.getServerType() && tiddler.fields["server.host"]) { // XXX: server.host could be empty string
			delete tiddler.fields.deleted;
			plugin.saveTiddler(tiddler);
		}
	});
};

plugin.saveTiddler = function(tiddler) {
	try {
		var adaptor = this.getTiddlerServerAdaptor(tiddler);
	} catch(ex) {
		return false;
	}
	var context = {
		tiddler: tiddler,
		changecount: tiddler.fields.changecount,
		workspace: tiddler.fields["server.workspace"]
	};
	var serverTitle = tiddler.fields["server.title"]; // indicates renames
	if(!serverTitle) {
		tiddler.fields["server.title"] = tiddler.title;
	} else if(tiddler.title != serverTitle) {
		return adaptor.moveTiddler({ title: serverTitle },
			{ title: tiddler.title }, context, null, this.saveTiddlerCallback);
	}
	var req = adaptor.putTiddler(tiddler, context, {}, this.saveTiddlerCallback);
	return req ? tiddler : false;
};

plugin.saveTiddlerCallback = function(context, userParams) {
	var tiddler = context.tiddler;
	if(context.status) {
		if(tiddler.fields.changecount == context.changecount) { //# check for changes since save was triggered
			tiddler.clearChangeCount();
		} else if(tiddler.fields.changecount > 0) {
			tiddler.fields.changecount -= context.changecount;
		}
		plugin.reportSuccess("saved", tiddler);
		store.setDirty(false);
	} else {
		if(context.httpStatus == 412) {
			plugin.reportFailure("saveConflict", tiddler);
		} else {
			plugin.reportFailure("saveError", tiddler, context);
		}
	}
};

plugin.removeTiddler = function(tiddler) {
	try {
		var adaptor = this.getTiddlerServerAdaptor(tiddler);
	} catch(ex) {
		return false;
	}
	var context = {
		host: tiddler.fields["server.host"],
		workspace: tiddler.fields["server.workspace"],
		tiddler: tiddler
	};
	var req = adaptor.deleteTiddler(tiddler, context, {}, this.removeTiddlerCallback);
	return req ? tiddler : false;
};

plugin.removeTiddlerCallback = function(context, userParams) {
	var tiddler = context.tiddler;
	if(context.status) {
		if(tiddler.fields.deleted === "true") {
			store.deleteTiddler(tiddler.title);
		} else {
			plugin.reportFailure("deleteLocalError", tiddler);
		}
		plugin.reportSuccess("deleted", tiddler);
		store.setDirty(false);
	} else {
		plugin.reportFailure("deleteError", tiddler, context);
	}
};

plugin.getTiddlerServerAdaptor = function(tiddler) { // XXX: rename?
	var type = tiddler.fields["server.type"] || config.defaultCustomFields["server.type"];
	return new config.adaptors[type]();
};

plugin.reportSuccess = function(msg, tiddler) {
	displayMessage(plugin.locale[msg].format([tiddler.title]));
};

plugin.reportFailure = function(msg, tiddler, context) {
	var desc = (context && context.httpStatus) ? context.statusText :
		plugin.locale.connectionError;
	displayMessage(plugin.locale[msg].format([tiddler.title, desc]));
};

config.macros.saveToWeb = { // XXX: hijack existing sync macro?
	locale: { // TODO: merge with plugin.locale?
		btnLabel: "save to web",
		btnTooltip: "synchronize changes",
		btnAccessKey: null
	},

	handler: function(place, macroName, params, wikifier, paramString, tiddler) {
		createTiddlyButton(place, this.locale.btnLabel, this.locale.btnTooltip,
			plugin.sync, null, null, this.locale.btnAccessKey);
	}
};

// hijack saveChanges to trigger remote saving
var _saveChanges = saveChanges;
saveChanges = function(onlyIfDirty, tiddlers) {
	if(window.location.protocol == "file:") {
		_saveChanges.apply(this, arguments);
	} else {
		plugin.sync(tiddlers);
	}
};

// override removeTiddler to flag tiddler as deleted -- XXX: use hijack to preserve compatibility?
TiddlyWiki.prototype.removeTiddler = function(title) { // XXX: should override deleteTiddler instance method?
	var tiddler = this.fetchTiddler(title);
	if(tiddler) {
		tiddler.tags = ["excludeLists", "excludeSearch", "excludeMissing"];
		tiddler.text = plugin.locale.removedNotice;
		tiddler.fields.deleted = "true"; // XXX: rename to removed/tiddlerRemoved?
		tiddler.fields.changecount = "1";
		this.notify(title, true);
		this.setDirty(true);
	}
};

// hijack ImportTiddlers wizard to handle cross-domain restrictions
var _onOpen = config.macros.importTiddlers.onOpen;
config.macros.importTiddlers.onOpen = function(ev) {
	var btn = $(resolveTarget(ev));
	var url = btn.closest(".wizard").find("input[name=txtPath]").val();
	if(window.location.protocol != "file:" && url.indexOf("://") != -1) {
		var host = url.split("/")[2];
		var macro = config.macros.importTiddlers;
		if(host != window.location.host) {
			btn.text(macro.cancelLabel).attr("title", macro.cancelPrompt);
			btn[0].onclick = macro.onCancel;
			$('<span class="status" />').text(plugin.locale.hostError).insertAfter(btn);
			return false;
		}
	}
	return _onOpen.apply(this, arguments);
};

})(jQuery);
//}}}
