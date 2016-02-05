console.log("2L by Damnever <dxc.wolf@gmail.com>")

/***** clear border when the link clicked *****/
$(document).ready(function() {
	$("a,button").bind("focus",function() {
	    if(this.blur) {this.blur()}
	})
})

Vue.filter('toHTML', function(value) {
	return marked(value)
})

Vue.filter('toStr', function(value) {
	return value ? value : ""
})

Vue.component('postComponent', {
	template: (function () {/*
		<li class="list-group-item post">
		  	<a class="badge post-comments" href="/post/${ postId }#${ commentCount }">${ commentCount }</a>
		  	<div class="post-avatar">
		  		<img src="${ authorAvatar }" class="thumbnail" alt="${ authorName }" width="50" height="50">
		  	</div>
		  	<div class="post-info">
				<a class="post-title" href="/post/${ postId }#${ commentCount }">${ postTitle }</a>
				<div class="post-other-info">
					<a v-if="tag" class="label label-default" href="/topic/${ topicId }" style="margin-right: 10px;">${ topicName }</a>
					<a class="post-author" href="/user/${ authorName }">${ authorName }</a>
					<span class="post-date" style="margin-right: 10px;">发布于 ${ postDate }前</span>
					<span v-if="lastCommentName">
						<a class="post-user" href="/user/${ lastCommentName }">${ lastCommentName }</a>
						<span class="comment-date">回复于 ${ lastCommentDate }前</span>
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
				<img src="${ avatar }" class="thumbnail" alt="${ title }" width="60" height="60">
				<div class="text">
					<div class="title">
						${ name }
						<button type="button" class="btn btn-link btn-xs">订阅</button>
					</div>
					<a class="admin" href="/user/${ admin }">@${ admin }</a>
				</div>
			</div>
			<div class="clearfix"></div>
			<div class="description">${ description }</div>
			<div class="rules">
				<div class="rule" v-for="rule in rules.split('|')">
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
	},
})

Vue.component('commentComponent', {
	template: (function () {/*
		<li id="${ commentId }" class="list-group-item">
			<div class="comment-vote">
				<div>
					<a href="javascript:;" @click="upVote" class="comment-up-votes">
						<span class="glyphicon glyphicon-chevron-up" aria-hidden="true"></span>
					</a>
				</div>
				<div>
					<a href="javascript:;" @click="downVote" class="comment-down-votes">
						<span class="glyphicon glyphicon-chevron-down" aria-hidden="true"></span>
					</a>
				</div>
			</div>
		  	<div class="comment-info">
		  		<a href="/user/${ commentUser }" class="comment-user">${ commentUser }</a>
		  		<span class="comment-date">评论于 ${ commentDate }</span>
		  		<a class="comment-reply" href="javascript:;" user="${ commentUser }" @click="at">#${ commentId }</a>
		  		<div class="comment-content">
		  			{!! commentContent | toHTML !!}
		  		</div>
		  	</div>
	    </li>
	*/}).toString().split('\n').slice(1,-1).join(''),
	props: {
		commentId: Number,
		commentUser: String,
		commentDate: String,
		commentContent: String,
		atUsers: Array,
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
			var id  = this.commentId
			postJSON('/api/votes/comment/'+ id +'/up', {}, function(response) {
				if (response.status === 1) {
					console.log("UP VOTES: ", response.count)
				} else {
					console.log("VOTES COMMENT #" + id + " UP GOT ERROR: ", response.code, " ", response.reason)
				}
			})
		},
		downVote: function() {
			var id  = this.commentId
			postJSON('/api/votes/comment/'+ id +'/down', {}, function(response) {
				if (response.status === 1) {
					console.log("DOWN VOTES: ", response.count)
				} else {
					console.log("VOTES COMMENT #" + id + " DOWN GOT ERROR: ", response.code, " ", response.reason)
				}
			})
		}
	}
})


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
	var r = document.cookie.match("\\b" + name + "=([^;]*)\\b")
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