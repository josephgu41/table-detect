(function () {
	"use strict";
	var t = {
			4662: function (t, e, n) {
				var i = n(6369),
					o = function () {
						var t = this,
							e = t._self._c;
						return e("div", { attrs: { id: "app" } }, [
							e("div", { staticClass: "container" }, [
								e(
									"div",
									{ staticClass: "left" },
									[
										e(
											"el-upload",
											{
												ref: "upload",
												staticClass: "upload-demo",
												attrs: {
													drag: "",
													action: t.actionURL,
													"show-file-list": !1,
													"on-success": t.onSuccess,
													"before-upload": t.beforeUpload,
												},
											},
											[
												e("i", { staticClass: "el-icon-upload" }),
												e("div", { staticClass: "el-upload__text" }, [
													t._v("将文件拖到此处，或"),
													e("em", [t._v("点击上传")]),
												]),
											]
										),
										t.thumbnail
											? e("div", { staticClass: "thumbnail" }, [
													e("img", { attrs: { src: t.thumbnail } }),
											  ])
											: t._e(),
										e(
											"el-button",
											{
												staticClass: "recognize-btn",
												attrs: {
													type: "primary",
													size: "large",
													loading: t.loading,
												},
												on: { click: t.recognizeImage },
											},
											[t._v(" 识别 ")]
										),
									],
									1
								),
								e(
									"div",
									{
										directives: [
											{
												name: "show",
												rawName: "v-show",
												value: "" !== t.result,
												expression: "result !== ''",
											},
										],
										staticClass: "right",
									},
									[
										e("div", {
											staticClass: "result",
											domProps: { innerHTML: t._s(t.result) },
										}),
									]
								),
							]),
						]);
					},
					r = [],
					a = {
						data() {
							return {
								imageFile: null,
								result: "",
								thumbnail: "",
								actionURL: "http://i-2.gpushare.com:44493/api/tr-run/",
								loading: !1,
							};
						},
						methods: {
							beforeUpload(t) {
								this.imageFile = t;
								const e = new FileReader();
								(e.onload = (t) => {
									this.thumbnail = t.target.result;
								}),
									e.readAsDataURL(t);
							},
							async recognizeImage() {
								if (!this.imageFile)
									return void this.$message.error("请先上传一张图片");
								this.loading = !0;
								const t = new FormData();
								t.append("file", this.imageFile);
								try {
									const e = await fetch(this.actionURL, {
											method: "POST",
											body: t,
										}),
										n = await e.json();
									console.log(n), (this.result = n.data), (this.loading = !1);
								} catch (e) {
									this.$message.error("识别失败，请重试"), (this.loading = !1);
								}
							},
							onSuccess(t, e, n) {
								this.$message({ message: "上传成功", type: "success" });
							},
						},
					},
					s = a,
					l = n(1001),
					u = (0, l.Z)(s, o, r, !1, null, "a1956386", null),
					c = u.exports,
					d = n(2140),
					f = n.n(d),
					p = n(8787),
					h = n.n(p),
					g = n(1540),
					v = n.n(g);
				i["default"].use(v()),
					i["default"].use(h()),
					(i["default"].prototype.$message = f()),
					(i["default"].config.productionTip = !1),
					new i["default"]({ render: (t) => t(c) }).$mount("#app");
			},
		},
		e = {};
	function n(i) {
		var o = e[i];
		if (void 0 !== o) return o.exports;
		var r = (e[i] = { exports: {} });
		return t[i](r, r.exports, n), r.exports;
	}
	(n.m = t),
		(function () {
			var t = [];
			n.O = function (e, i, o, r) {
				if (!i) {
					var a = 1 / 0;
					for (c = 0; c < t.length; c++) {
						(i = t[c][0]), (o = t[c][1]), (r = t[c][2]);
						for (var s = !0, l = 0; l < i.length; l++)
							(!1 & r || a >= r) &&
							Object.keys(n.O).every(function (t) {
								return n.O[t](i[l]);
							})
								? i.splice(l--, 1)
								: ((s = !1), r < a && (a = r));
						if (s) {
							t.splice(c--, 1);
							var u = o();
							void 0 !== u && (e = u);
						}
					}
					return e;
				}
				r = r || 0;
				for (var c = t.length; c > 0 && t[c - 1][2] > r; c--) t[c] = t[c - 1];
				t[c] = [i, o, r];
			};
		})(),
		(function () {
			n.n = function (t) {
				var e =
					t && t.__esModule
						? function () {
								return t["default"];
						  }
						: function () {
								return t;
						  };
				return n.d(e, { a: e }), e;
			};
		})(),
		(function () {
			n.d = function (t, e) {
				for (var i in e)
					n.o(e, i) &&
						!n.o(t, i) &&
						Object.defineProperty(t, i, { enumerable: !0, get: e[i] });
			};
		})(),
		(function () {
			n.g = (function () {
				if ("object" === typeof globalThis) return globalThis;
				try {
					return this || new Function("return this")();
				} catch (t) {
					if ("object" === typeof window) return window;
				}
			})();
		})(),
		(function () {
			n.o = function (t, e) {
				return Object.prototype.hasOwnProperty.call(t, e);
			};
		})(),
		(function () {
			n.r = function (t) {
				"undefined" !== typeof Symbol &&
					Symbol.toStringTag &&
					Object.defineProperty(t, Symbol.toStringTag, { value: "Module" }),
					Object.defineProperty(t, "__esModule", { value: !0 });
			};
		})(),
		(function () {
			var t = { 143: 0 };
			n.O.j = function (e) {
				return 0 === t[e];
			};
			var e = function (e, i) {
					var o,
						r,
						a = i[0],
						s = i[1],
						l = i[2],
						u = 0;
					if (
						a.some(function (e) {
							return 0 !== t[e];
						})
					) {
						for (o in s) n.o(s, o) && (n.m[o] = s[o]);
						if (l) var c = l(n);
					}
					for (e && e(i); u < a.length; u++)
						(r = a[u]), n.o(t, r) && t[r] && t[r][0](), (t[r] = 0);
					return n.O(c);
				},
				i = (self["webpackChunktable_detect"] =
					self["webpackChunktable_detect"] || []);
			i.forEach(e.bind(null, 0)), (i.push = e.bind(null, i.push.bind(i)));
		})();
	var i = n.O(void 0, [998], function () {
		return n(4662);
	});
	i = n.O(i);
})();
//# sourceMappingURL=app.a584187e.js.map