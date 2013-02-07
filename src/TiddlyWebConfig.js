/***
|''Name''|TiddlyWebConfig|
|''Description''|configuration settings for TiddlyWebWiki|
|''Author''|FND|
|''Version''|1.3.2|
|''Status''|stable|
|''Source''|http://svn.tiddlywiki.org/Trunk/association/plugins/TiddlyWebConfig.js|
|''License''|[[BSD|http://www.opensource.org/licenses/bsd-license.php]]|
|''Requires''|TiddlyWebAdaptor ServerSideSavingPlugin|
|''Keywords''|serverSide TiddlyWeb|
!Code
***/
//{{{
(function($) {

if(!config.extensions.ServerSideSavingPlugin) {
	throw "Missing dependency: ServerSideSavingPlugin";
}
if(!config.adaptors.tiddlyweb) {
	throw "Missing dependency: TiddlyWebAdaptor";
}

if(window.location.protocol != "file:") {
	config.options.chkAutoSave = true;
}

var adaptor = tiddler.getAdaptor();
var recipe = tiddler.fields["server.recipe"];
var workspace = recipe ? "recipes/" + recipe : "bags/common";

var plugin = config.extensions.tiddlyweb = {
	host: tiddler.fields["server.host"].replace(/\/$/, ""),
	username: null,
	status: {},

	getStatus: null, // assigned later
	getUserInfo: function(callback) {
		this.getStatus(function(status) {
			callback({
				name: plugin.username,
				anon: plugin.username ? plugin.username == "GUEST" : true
			});
		});
	},
	hasPermission: function(type, tiddler) {
		var perms = tiddler.fields["server.permissions"];
		if(perms) {
			return perms.split(", ").contains(type);
		} else {
			return true;
		}
	}
};

config.defaultCustomFields = {
	"server.type": tiddler.getServerType(),
	"server.host": plugin.host,
	"server.workspace": workspace
};

// modify toolbar commands

config.shadowTiddlers.ToolbarCommands = config.shadowTiddlers.ToolbarCommands.
	replace("syncing ", "revisions syncing ");

config.commands.saveTiddler.isEnabled = function(tiddler) {
	return plugin.hasPermission("write", tiddler) && !tiddler.isReadOnly();
};

config.commands.deleteTiddler.isEnabled = function(tiddler) {
	return !readOnly && plugin.hasPermission("delete", tiddler);
};

// hijack option macro to disable username editing
var _optionMacro = config.macros.option.handler;
config.macros.option.handler = function(place, macroName, params, wikifier,
		paramString) {
	if(params[0] == "txtUserName") {
		params[0] = "options." + params[0];
		var self = this;
		var args = arguments;
		args[0] = $("<span />").appendTo(place)[0];
		plugin.getUserInfo(function(user) {
			config.macros.message.handler.apply(self, args);
		});
	} else {
		_optionMacro.apply(this, arguments);
	}
};

// hijack isReadOnly to take into account permissions and content type
var _isReadOnly = Tiddler.prototype.isReadOnly;
Tiddler.prototype.isReadOnly = function() {
	return _isReadOnly.apply(this, arguments) ||
		!plugin.hasPermission("write", this);
};

var getStatus = function(callback) {
	if(plugin.status.version) {
		callback(plugin.status);
	} else {
		var self = getStatus;
		if(self.pending) {
			if(callback) {
				self.queue.push(callback);
			}
		} else {
			self.pending = true;
			self.queue = callback ? [callback] : [];
			var _callback = function(context, userParams) {
				var status = context.serverStatus || {};
				for(var key in status) {
					if(key == "username") {
						plugin.username = status[key];
						config.macros.option.propagateOption("txtUserName",
							"value", plugin.username, "input");
					} else {
						plugin.status[key] = status[key];
					}
				}
				for(var i = 0; i < self.queue.length; i++) {
					self.queue[i](plugin.status);
				}
				delete self.queue;
				delete self.pending;
			};
			adaptor.getStatus({ host: plugin.host }, null, _callback);
		}
	}
};
(plugin.getStatus = getStatus)(); // XXX: hacky (arcane combo of assignment plus execution)

})(jQuery);
//}}}
