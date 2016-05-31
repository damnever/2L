var usernameRe = /^[^0-9]\w{2,8}$/
var passwordRe = /^[a-zA-Z0-9,_]{6,20}$/
var emailRe = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/

var errorWrap = function(text) {
    return '<b class="text-danger">' + text + '</b>'
}

Vue.component('loginComponent', {
    template: (function () {/*
        <li id="login" class="for-nav">
            <a @click="showModal = true" href="javascript:;">登录</a>
            <modal :show.sync="showModal" effect="fade" width="200">
                <div slot="modal-header" class="modal-header">
                    <button type="button" class="close" @click="showModal = false"><span>&times;</span></button>
                    <h4 class="modal-title">
                      {!! title !!}
                    </h4>
                </div>
                <div slot="modal-body" class="modal-body">
                    <form slot="body" action="/login" method="POST" id="login-form">
                        <div class="form-group" :class="{'has-error': usernameWrong}">
                            <input type="text" class="form-control" placeholder="请输入用户名" v-model="username" @blur="checkUsername">
                        </div>
                        <div class="form-group" :class="{'has-error': passwordWrong}">
                            <input type="password" class="form-control" placeholder="请输入密码"v-model="password" @blur="checkPassword">
                        </div>
                        <div class="checkbox">
                            <label><input type="checkbox" v-model="expire" value="30"> 30天内记住我</label>
                        </div>
                    </form>
                </div>
                <div slot="modal-footer" class="modal-footer">
                    <button type="submit" class="btn btn-default" style="width:100%" @click="send">登&emsp;录</button>
                </div>
            </modal>
        </li>
    */}).toString().split('\n').slice(1,-1).join(''),
    props: {
        currentUser: String,
    },
    data: function() {
        return {
            showModal: false,
            title: '欢迎回来',
            username: '',
            password: '',
            expire: true,
            usernameWrong: false,
            passwordWrong: false,
        }
    },
    methods: {
        send: function() {
            if (this.usernameWrong || this.passwordWrong) {
                return
            }
            // POST /api/login
            var data = {
                'username': this.username,
                'password': this.password,
                'expire': this.expire ? 30 : 1,
            }
            postJSON('/api/login', data, this.handleResp)
        },
        handleResp: function(response) {
            if (response.status == 1) {
                this.showModal = false
                vAlert.success(response.username + '，欢迎回来！')
                this.currentUser = response.username
                this.username = ''
                this.password = ''
            } else {
                var errmsg = response.code.toString() + ' ' + response.reason
                console.log("LOGIN ERROR: ", errmsg)
                this.title = errorWrap(errmsg)
            }
        },
        checkUsername: function() {
            if (usernameRe.test(this.username)) {
                this.title = '用户名正确'
                this.usernameWrong = false
            } else {
                this.title = errorWrap('用户名为3~8个非汉字字符')
                this.usernameWrong = true
            }
        },
        checkPassword: function() {
            if (passwordRe.test(this.password)) {
                this.title = '密码正确'
                this.passwordWrong = false
            } else {
                this.title = errorWrap('密码为6~20个字符[0-9a-zA-Z,_]')
                this.passwordWrong = true
            }
        },
    },
    components: {
        'modal': VueStrap.modal
    }
})

Vue.component('registerComponent', {
    template: (function () {/*
        <li id="register" class="for-nav" style="margin-left:10px;">
            <a @click="showModal = true" href="javascript:;">注册</a>
            <modal :show.sync="showModal" effect="fade" width="200">
                <div slot="modal-header" class="modal-header">
                    <button type="button" class="close" @click="showModal = false"><span>&times;</span></button>
                    <h4 class="modal-title">
                        {!! title !!}
                    </h4>
                </div>
                <div slot="modal-body" class="modal-body">
                    <form slot="body" action="/register" method="POST" id="login-form">
                        <div class="form-group"  :class="{'has-error': usernameWrong}">
                            <input type="text" class="form-control" placeholder="请输入用户名" v-model="username" @blur="checkUsername">
                        </div>
                        <div class="form-group"  :class="{'has-error': emailWrong}">
                            <input type="text" class="form-control" placeholder="请输入邮箱" v-model="email" @blur="checkEmail">
                        </div>
                        <div class="form-group" :class="{'has-error': passwordWrong}">
                            <input type="password" class="form-control" placeholder="请输入密码" v-model="password" @blur="checkPassword">
                        </div>
                    </form>
                </div>
                <div slot="modal-footer" class="modal-footer">
                    <button type="submit" class="btn btn-default" style="width:100%" @click="send">注&emsp;册</button>
                </div>
            </modal>
        </li>
    */}).toString().split('\n').slice(1,-1).join(''),
    props: {
        currentUser: String,
    },
    data:  function() {
        return {
            showModal: false,
            title: '欢迎注册',
            username: '',
            password: '',
            email: '',
            usernameWrong: false,
            passwordWrong: false,
            emailWrong: false,
        }
    },
    methods: {
        send: function() {
            if (this.usernameWrong || this.passwordWrong || this.emailWrong) {
                return
            }
            // POST /api/register
            var data = {
                'username': this.username,
                'password': this.password,
                'email': this.email,
            }
            postJSON('/api/register', data, this.handleResp)
        },
        handleResp: function(response) {
            if (response.status == 1) {
                this.showModal = false
                this.currentUser = response.username
                vAlert.success(response.username + '，您已注册成功并登录！')
                this.username = ''
                this.password = ''
                this.email = ''
            } else {
                var errmsg = response.code.toString() + ' ' + response.reason
                console.log("REGISTER ERROR: ", errmsg)
                this.title = errorWrap(errmsg)
            }
        },
        checkUsername: function() {
            if (usernameRe.test(this.username)) {
                this.title = '用户名正确'
                this.usernameWrong = false
            } else {
                this.title = errorWrap('用户名为3~8个非汉字字符')
                this.usernameWrong = true
            }
        },
        checkPassword: function() {
            if (passwordRe.test(this.password)) {
                this.title = '密码正确'
                this.passwordWrong = false
            } else {
                this.title = errorWrap('密码为6~20个英文/数字/,/_ 字符')
                this.passwordWrong = true
            }
        },
        checkEmail: function() {
            if (emailRe.test(this.email)) {
                this.title = '邮箱格式正确'
                this.emailWrong = false
            } else {
                this.title = errorWrap('邮箱格式错误')
                this.emailWrong = true
            }
        }
    },
    components: {
        'modal': VueStrap.modal
    }
})
