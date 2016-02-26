console.log("2L by Damnever <dxc.wolf@gmail.com>")

Vue.filter('toHTML', function(value) {
	return marked(value)
})

Vue.filter('toStr', function(value) {
	return value ? value : " "
})

Vue.filter('limitStr', function(value) {
	if (value.length > 28) {
		return value.slice(0, 25) + '...'
	}
	return value
})

///////////////////////////////////////////////////////////////////////////////
var vAlert = new Vue({
    el: '#msg-alert',
    data: {
        showDanger: false,
        showWarning: false,
        showInfo: false,
        showSuccess: false,
        msg: '',
    },
    methods: {
        danger: function(msg) {
            this.msg = msg
            this.showDanger = true
        },
        warning: function(msg) {
            this.msg = msg
            this.showWarning = true
        },
        info: function(msg) {
            this.msg = msg
            this.showInfo = true
        },
        success: function(msg) {
            this.msg = msg
            this.showSuccess = true
        },
    },
    components: {
        'alert': VueStrap.alert,
    }
})

///////////////////////////////////////////////////////////////////////////////
Vue.component('postComponent', {
	template: (function () {/*
		<li class="list-group-item post">
		  	<a class="badge post-comments" href="/post/${ postId }#${ commentCount }">${ commentCount }</a>
		  	<div class="post-avatar">
		  		<img src="${ 'data:image/*;base64,' + authorAvatar }" class="thumbnail" alt="${ authorName }" width="50" height="50">
		  	</div>
		  	<div class="post-info">
				<a class="post-title" href="/post/${ postId }#${ commentCount }">${ postTitle }</a>
				<div class="post-other-info">
					<a v-if="tag" class="label label-default" href="/topic/${ topicId }" style="margin-right: 10px;">${ topicName }</a>
					<a class="post-author" href="/user/${ authorName }">${ authorName }</a>
					<span class="post-date" style="margin-right: 10px;">发布于 ${ postDate }</span>
					<span v-if="commentCount > 0">
						<a class="post-user" href="/user/${ lastCommentName }">${ lastCommentName }</a>
						<span class="comment-date">回复于 ${ lastCommentDate }</span>
					</span>
					<span class="comment-date" v-else>还没有人回复</span>
				</div>
			</div>
	    </li>
	*/}).toString().split('\n').slice(1,-1).join(''),
	props: {
		tag: Boolean,
		postId: Number,
		postTitle: String,
		topicId: Number,
		topicName: String,
		authorAvatar: String,
		authorName: String,
		postDate: String,
		lastCommentName: String,
		lastCommentDate: String,
		commentCount: Number,
	},
})

Vue.component('topicComponent', {
	template: (function () {/*
		<div class="topic">
			<div class="header">
				<img src="${ 'data:image/*;base64,' + avatar }" class="thumbnail" alt="${ title }" width="60" height="60">
				<div class="text">
					<div class="title">
						${ name }
						<button type="button" class="btn btn-link btn-xs" @click="subscribe">
							<span v-if="isSubscribed">取消订阅</span>
							<span v-else>订阅</sapn>
						</button>
					</div>
					<a class="admin" href="/user/${ admin }">@${ admin }</a>
				</div>
			</div>
			<div class="clearfix"></div>
			<div class="description">${ description }</div>
			<div class="rules">
				<div class="rule" v-for="rule in rules.split('\n')">
					<span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span> ${ rule | toStr }
				</div>
				<a href="/topic/${ id }/new/post" v-show="bPost" class="btn btn-default" style="margin-top:10px;width:100%;" @click="newPost">发&emsp;帖</a>
			</div>
		</div>
	*/}).toString().split('\n').slice(1,-1).join(''),
	props: {
		id: Number,
		name: String,
		avatar: String,
		admin: String,
		description: String,
		rules: String,
		bPost: Boolean,
		isSubscribed: Boolean,
	},
	methods: {
		subscribe: function() {
			subUnsub(this)
		},
	}
})

Vue.component('topicThumbnailComponent', {
	template: (function () {/*
		<li class="list-group-item">
		    <div class="topics">
		    	<div class="topic-avatar">
		    		<img src="${ 'data:image/*;base64,' + avatar }" class="thumbnail" alt="${ name }" width="60" height="60">
		    	</div>
		    	<div class="topic-text">
		    		<div class="header">
			    		<a href="/topic/${ id }" target="_blank">${ name }</a>
			    		<button type="button" class="btn btn-link btn-xs" @click="unsubscribe">
			    			<span v-if="isSubscribed">取消订阅</span>
			    			<span v-else>订阅</span>
			    		</button>
			    	</div>
			    	<div class="description">${ description }</div>
		    	</div>
	    	</div>
	    </li>
	*/}).toString().split('\n').slice(1,-1).join(''),
	props: {
		id: Number,
		name: String,
		avatar: String,
		description: String,
		isSubscribed: Boolean,
	},
	methods: {
		unsubscribe: function() {
			subUnsub(this)
		}
	}
})

Vue.component('commentComponent', {
	template: (function () {/*
		<li id="${ commentId }" class="list-group-item">
			<div class="comment-left">
				<img src="${ 'data:image/*;base64,' + commentAvatar }" class="thumbnail" alt="${ commentUser }" width="40" height="40">
			</div>
		  	<div class="comment-info">
		  		<a href="/user/${ commentUser }" class="comment-user">${ commentUser }</a>
		  		<span style="margin-left:5px;">
			  		<a href="javascript:;" @click="upVote" class="comment-up-votes"  :class="{'comment-voted': isUpVoted}">
						<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> ${ commentUpVotes }
					</a>
					<a href="javascript:;" @click="downVote" class="comment-down-votes"  :class="{'comment-voted': isDownVoted}">
						<span class="glyphicon glyphicon-thumbs-down" aria-hidden="true"></span> ${ commentDownVotes }
					</a>
				</span>
		  		<span class="comment-date">评论于 ${ commentDate }</span>
		  		<a class="comment-reply" href="javascript:;" @click="at">#${ commentIndex }</a>
		  		<div class="comment-content">
		  			{!! commentContent | toHTML !!}
		  		</div>
		  	</div>
	    </li>
	*/}).toString().split('\n').slice(1,-1).join(''),
	props: {
		commentIndex: Number,
		commentId: Number,
		commentUser: String,
		commentDate: String,
		commentContent: String,
		commentAvatar: String,
		commentUpVotes: Number,
		commentDownVotes: Number,
		atUsers: Array,
		isUpVoted: Boolean,
		isDownVoted: Boolean,
	},
	methods: {
		at: function() {
			for (var i=0; i < this.atUsers.length; i++) {
				if (this.atUsers[i] === ("@" + this.commentUser)) {
					return
				}
			}
			this.atUsers.push("@" + this.commentUser)
		},
		upVote: function() {
			var self = this
			var id  = this.commentId

			if (self.isUpVoted) {
				DELETE('/api/votes/comment/'+ id +'/up', {'token': getCookieByName('token')}, function(response) {
					if (response.status === 1) {
						self.commentUpVotes = response.count
						self.isUpVoted = false
					} else {
						if (response.code == 403) {
							vAlert.danger('您没有投票权限！')
						}
						console.log("VOTES COMMENT #" + id + " UP GOT ERROR: ", response.code, response.reason)
					}
				})
			} else {
				postJSON('/api/votes/comment/'+ id +'/up', {'token': getCookieByName('token')}, function(response) {
					if (response.status === 1) {
						self.commentUpVotes = response.count
						self.isUpVoted = true
					} else {
						if (response.code == 403) {
							vAlert.danger('您没有投票权限！')
						}
						console.log("VOTES COMMENT #" + id + " UP GOT ERROR: ", response.code, response.reason)
					}
				})
			}
		},
		downVote: function() {
			var self = this
			var id  = this.commentId

			if (self.isDownVoted) {
				DELETE('/api/votes/comment/'+ id +'/down', {'token': getCookieByName('token')}, function(response) {
					if (response.status === 1) {
						self.commentDownVotes = response.count
						self.isDownVoted = false
					} else {
						if (response.code == 403) {
							vAlert.danger('您没有投票权限！')
						}
						console.log("VOTES COMMENT #" + id + " DOWN GOT ERROR: ", response.code, response.reason)
					}
				})
			} else {
				postJSON('/api/votes/comment/'+ id +'/down', {}, function(response) {
					if (response.status === 1) {
						self.commentDownVotes = response.count
						self.isDownVoted = true
					} else {
						if (response.code == 403) {
							vAlert.danger('您没有投票权限！')
						}
						console.log("VOTES COMMENT #" + id + " DOWN GOT ERROR: ", response.code, response.reason)
					}
				})
			}
		}
	}
})

///////////////////////////////////////////////////////////////////////////////
function subUnsub(obj) {
	var token = getCookieByName("token")
	if (obj.isSubscribed) {
		var url = "/api/unsubscribe/topic/" + obj.id
		DELETE(url, {"token": token}, function(response) {
			if (response.status === 1) {
				obj.isSubscribed = false
			} else {
				console.log("UNSUBSCRIBE TOPIC ", url, ", ERROR", response.code, response.reason)
			}
		})
	} else {
		var url = "/api/subscribe/topic/" + obj.id
		postJSON(url, {"token": token}, function(response) {
			if (response.status === 1) {
				obj.isSubscribed = true
			} else {
				console.log("SUBSCRIBE TOPIC ", url, ", ERROR", response.code, response.reason)
			}
		})
	}
}


///////////////////////////////////////////////////////////////////////////////
function getJSON(url, data, callback) {
	$.ajax({
		url: url,
		dataType: "json",
		type: "GET",
		data: data,
		success: function(response) {
			if (callback) {
				callback(response)
			}
		},
		error: function(response) {
			console.log("GET FROM " ,url, " GOT ERROR: ", response)
		}
	})
}

function postJSON(url, data, callback) {
	data._xsrf = getXSRF()
	$.ajax({
		url: url,
		data: $.param(data),
		dataType: "json",
		type: "POST",
		success: function(response) {
			if (callback) {
				callback(response)
			}
		},
		error: function(response) {
			console.log("POST TO " , url, " GOT ERROR: ", response)
		}
	})
}

function DELETE(url, data, callback) {
	data._xsrf = getXSRF()
	$.ajax({
		url: url,
		data: $.param(data),
		dataType: "json",
		type: "DELETE",
		success: function(response) {
			if (callback) {
				callback(response)
			}
		},
		error: function(response) {
			console.log("DELETE TO " , url, " GOT ERROR: ", response)
		}
	})
}

function getXSRF() {
	var xsrf = getCookieByName("_xsrf")
	if (!xsrf) {
    	var hidden = $('input[name="_xsrf"]')
    	if (hidden.length != 0) {
    		xsrf = hidden[0].value
    	}
    }
    return xsrf
}

function getCookieByName(name) {
	var r = document.cookie.match("\\b" + name + "=\"?([^;]*)\"?\\b")
	return (r ? r[1] : undefined)
}

// Format string
// http://witmax.cn/js-function-string-format.html
String.format = function(src){
    if (arguments.length == 0) return null;
    var args = Array.prototype.slice.call(arguments, 1);
    return src.replace(/\{(\d+)\}/g, function(m, i){
        return args[i];
    });
};

// Range function:
// http://stackoverflow.com/questions/3895478/does-javascript-have-a-method-like-range-to-generate-an-array-based-on-suppl
function range(start, count) {
    return Array.apply(0, Array(count)).map(function (element, index) {
    	return index + start;  
    });
}