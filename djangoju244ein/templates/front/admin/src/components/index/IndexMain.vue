<template>
	<div style="height: 100%;">
		<el-main :style='"horizontal" == "vertical" ? (2 == 1 ? {"minHeight":"100%","padding":"0","margin":"0 0 0 210px","position":"relative","display":"block"} : (2 == 2 ? (isCollapse ? {"minHeight":"100%","padding":"10px 0 0 64px","margin":"0","position":"relative","background":"#13a1e6","display":"block"} : {"minHeight":"100%","padding":"10px 0 30px 210px","margin":"0","position":"relative","background":"#13a1e6","display":"block"}) : "")) : {"minHeight":"100%","padding":"0px 0 0px","margin":"0","position":"relative","background":"#fff"}'>
			<!-- top -->
			<index-header :style='{"boxShadow":"0 0px 0px rgba(3, 152, 15, .05)","padding":"8px 150px 8px 20px","margin":"0 auto","borderColor":"#74d4fb","alignItems":"center","color":"#FFF","display":"flex","justifyContent":"space-between","borderRadius":"0","background":"#1d1f27","borderWidth":"0px 0","width":"calc(100% - 0px)","fontSize":"14px","position":"relative","borderStyle":"solid","zIndex":"1","height":"64px"}'></index-header>
			
			<!-- menu -->
			<template v-if="'horizontal' == 'vertical'">
			  <template v-if="2 == 1">
				<index-aside :style='{"boxShadow":"1px 0 6px  rgba(64, 158, 255, .3)","overflow":"hidden","top":"0","left":"0","background":"#304156","bottom":"0","width":"210px","fontSize":"0px","position":"fixed","height":"100%","zIndex":"1001"}'></index-aside>
			  </template>
			  <template v-if="2 == 2">
				<index-aside :is-collapse="isCollapse" @oncollapsechange="collapseChange" :style='isCollapse ? {"boxShadow":"0px 0 0px rgba(255,205,155,1)","padding":"45px 0 0","borderColor":"rgba(126, 96, 16, .2)","bottom":"0","transition":"width 0.3s","overflow":"hidden","top":"91px","left":"0","background":"#fff","borderWidth":"0 1px 0 0","width":"64px","fontSize":"0px","position":"fixed","borderStyle":"solid","height":"100%","zIndex":"1001"} : {"boxShadow":"0px 0 0px rgba(255,205,155,1)","padding":"10px 5px 180px","borderColor":"#74d4fb","bottom":"25px","transition":"width 0.3s","overflow":"hidden","top":"91px","borderRadius":"10px","left":"10px","background":"url(http://codegen.caihongy.cn/20230725/aae2696971c94690b15ac8920e43a549.png) no-repeat center bottom / 100% auto,#1688c7","borderWidth":"1px","width":"210px","fontSize":"16px","position":"fixed","borderStyle":"solid","height":"auto","zIndex":"1001"}'></index-aside>
			  </template>
			</template>
			<template v-if="'horizontal' == 'horizontal'">
			  <template v-if="2 == 1">
				<index-aside :style='{"width":"100%","borderColor":"#efefef","borderStyle":"solid","background":"#304156","borderWidth":"0 0 1px 0","height":"auto"}'></index-aside>
			  </template>
			  <template v-if="2 == 2">
				<index-aside :style='{"padding":"0 0px","borderColor":"#efefef","margin":"0 auto","display":"flex","top":"10px","left":"30%","background":"none","borderWidth":"0 0 0px 0","width":"calc(70% - 300px)","position":"absolute","borderStyle":"solid","height":"auto","zIndex":"9"}'></index-aside>
			  </template>
			</template>
			
			<!-- breadcrumb -->
			<bread-crumbs :title="title" :style='{"padding":"0px ","margin":"0 auto","borderColor":"#eee","borderWidth":"0 0 0px 0","background":"rgba(255,255,255,1)","display":"none","width":"100%","fontSize":"16px","borderStyle":"solid"}' class="bread-crumbs"></bread-crumbs>
			
			<!-- TagsView -->
			<tags-view />
			
			<router-view class="router-view"></router-view>
		</el-main>
	</div>
</template>

<script>
	import IndexAside from '@/components/index/IndexAsideStatic'
	import IndexHeader from '@/components/index/IndexHeader'
	import TagsView from '@/components/index/TagsView'
	import menu from "@/utils/menu";
	export default {
		components: {
			IndexAside,
			IndexHeader,
			TagsView
		},
		data() {
			return {
				menuList: [],
				role: "",
				currentIndex: -2,
				itemMenu: [],
				title: '',
				isCollapse: false,
			};
		},
		mounted() {
			let menus = menu.list();
			this.menuList = menus;
			this.role = this.$storage.get("role");
		},
		created() {
			this.init();
		},
		methods: {
			init(){
				this.$nextTick(()=>{
					
				})
			},
			collapseChange(collapse) {
				this.isCollapse = collapse
			},
			menuHandler(menu) {
				this.$router.push({
					name: menu.tableName
				});
				this.title = menu.menu;
			},
			titleChange(index, menus) {
				this.currentIndex = index
				this.itemMenu = menus;
			},
			homeChange(index) {
				this.itemMenu = [];
				this.title = ""
				this.currentIndex = index
				this.$router.push({
					name: 'home'
				});
			},
			centerChange(index) {
				this.itemMenu = [{
					"buttons": ["新增", "查看", "修改", "删除"],
					"menu": "修改密码",
					"tableName": "updatePassword"
				}, {
					"buttons": ["新增", "查看", "修改", "删除"],
					"menu": "个人信息",
					"tableName": "center"
				}];
				this.title = ""
				this.currentIndex = index
				this.$router.push({
					name: 'home'
				});
				
			}
		}
	};
</script>
<style lang="scss" scoped>
	a {
		text-decoration: none;
		color: #555;
	}

	a:hover {
		background: #00c292;
	}
	
	.el-main {
		padding: 0;
		display: block;
	}

	.nav-list {
		width: 100%;
		margin: 0 auto;
		text-align: left;
		margin-top: 20px;

		.nav-title {
			display: inline-block;
			font-size: 15px;
			color: #333;
			padding: 15px 25px;
			border: none;
		}

		.nav-title.active {
			color: #555;
			cursor: default;
			background-color: #fff;
		}
	}

	.nav-item {
		margin-top: 20px;
		background: #FFFFFF;
		padding: 15px 0;

		.menu {
			padding: 15px 25px;
		}
	}
	
	.detail-form-content {
	    background: transparent;
	}
</style>
