// Dropdown Menu
var dropdown = document.querySelectorAll('.dropdown');
var dropdownArray = Array.prototype.slice.call(dropdown,0);
dropdownArray.forEach(function(el){
	var button = el.querySelector('div[data-toggle="dropdown"]'),
			menu = el.querySelector('.dropdown-menu'),
			arrow = button.querySelector('i.icon-right');

	button.onclick = function(event) {
		if(!menu.hasClass('show')) {
			closeAll();
			menu.classList.add('show');
			menu.classList.remove('hide');
			arrow.classList.add('open');
			arrow.classList.remove('close');
			event.preventDefault();
		}
		else {
			menu.classList.remove('show');
			menu.classList.add('hide');
			arrow.classList.remove('open');
			arrow.classList.add('close');
			event.preventDefault();
		}
	};
});
function closeAll() {
	dropdownArray.forEach(function(el){
		var button = el.querySelector('div[data-toggle="dropdown"]'),
		menu = el.querySelector('.dropdown-menu'),
		arrow = button.querySelector('i.icon-right');
		
		menu.classList.remove('show');
		menu.classList.add('hide');
		arrow.classList.remove('open');
		arrow.classList.add('close');
	});
}
Element.prototype.hasClass = function(className) {
	return this.className && new RegExp("(^|\\s)" + className + "(\\s|$)").test(this.className);
};

/********************************** 操作表 ************************************/
/********************************************** 灯开关 **********************************************/
$(document).on('click', '.light-action', function() {
	var buttons1 = [ {
		text : '请选择',
		label : true
	}, {
		text : '打开',
		bold : true,
		onClick : function() {
			$.alert("你打开了电灯");
		}
	}, {
		text : '关闭',
		bold : true,
		color : 'danger',
		onClick : function() {
			$.alert("你关闭了电灯");
		}
	} ];
	var buttons2 = [ {
		text : '取消',
		bg : 'danger'
	} ];
	var groups = [ buttons1, buttons2 ];
	$.actions(groups);
});
/********************************************** 可调节等 **********************************************/
$(document).on('click', '.adjusting-light-action', function() {
	var buttons1 = [ {
		text : '请选择',
		label : true
	}, {
		text : '打开',
		bold : true,
		onClick : function() {
			$.alert("你打开了电灯");
		}
	}, {
		text : '关闭',
		bold : true,
		color : 'danger',
		onClick : function() {
			$.alert("你关闭了电灯");
		}
	}, {
		text : '一级',
		bold : true,
		onClick : function() {
			$.alert("你将电灯调节为一级亮度");
		}
	}, {
		text : '二级',
		bold : true,
		onClick : function() {
			$.alert("你将电灯调节为二级亮度");
		}
	} ];
	var buttons2 = [ {
		text : '取消',
		bg : 'danger'
	} ];
	var groups = [ buttons1, buttons2 ];
	$.actions(groups);
});
/********************************************** 排插 **********************************************/
$(document).on('click', '.socket-action', function() {
	var buttons1 = [ {
		text : '请选择',
		label : true
	}, {
		text : '打开',
		bold : true,
		onClick : function() {
			$.alert("你打开了排插电源");
		}
	}, {
		text : '关闭',
		bold : true,
		color : 'danger',
		onClick : function() {
			$.alert("你关闭了排插电源");
		}
	} ];
	var buttons2 = [ {
		text : '取消',
		bg : 'danger'
	} ];
	var groups = [ buttons1, buttons2 ];
	$.actions(groups);
});
/********************************************** 窗帘 **********************************************/
$(document).on('click', '.curtains-action', function() {
	var buttons1 = [ {
		text : '请选择',
		label : true
	}, {
		text : '打开',
		bold : true,
		onClick : function() {
			$.alert("你打开窗帘中");
		}
	}, {
		text : '关闭',
		bold : true,
		color : 'danger',
		onClick : function() {
			$.alert("你关闭窗帘中");
		}
	}, {
		text : '停止',
		bold : true,
		onClick : function() {
			$.alert("你停止窗帘关闭");
		}
	} ];
	var buttons2 = [ {
		text : '取消',
		bg : 'danger'
	} ];
	var groups = [ buttons1, buttons2 ];
	$.actions(groups);
});
/********************************************** 安防报警 **********************************************/
$(document).on('click', '.security-action', function() {
	var buttons1 = [ {
		text : '请选择',
		label : true
	}, {
		text : '布防',
		bold : true,
		onClick : function() {
			$.alert("你打开了安防系统");
		}
	}, {
		text : '撤防',
		bold : true,
		color : 'danger',
		onClick : function() {
			$.alert("你关闭安防系统");
		}
	} ];
	var buttons2 = [ {
		text : '取消',
		bg : 'danger'
	} ];
	var groups = [ buttons1, buttons2 ];
	$.actions(groups);
});
/********************************************** 风扇 **********************************************/
$(document).on('click', '.fan-action', function() {
	var buttons1 = [ {
		text : '请选择',
		label : true
	}, {
		text : '打开',
		bold : true,
		onClick : function() {
			$.alert("风扇打开");
		}
	}, {
		text : '关闭',
		bold : true,
		color : 'danger',
		onClick : function() {
			$.alert("风扇关闭");
		}
	}, {
		text : '摇头',
		bold : true,
		onClick : function() {
			$.alert("风扇开始摇头");
		}
	} ];
	var buttons2 = [ {
		text : '取消',
		bg : 'danger'
	} ];
	var groups = [ buttons1, buttons2 ];
	$.actions(groups);
});
/********************************************** 音响 **********************************************/
$(document).on('click', '.sound-action', function() {
	var buttons1 = [ {
		text : '请选择',
		label : true
	}, {
		text : 'USB选择',
		bold : true,
		onClick : function() {
			$.alert("USB选择");
		}
	}, {
		text : '静音',
		bold : true,
		onClick : function() {
			$.alert("静音");
		}
	}, {
		text : '上一首',
		bold : true,
		onClick : function() {
			$.alert("上一首");
		}
	}, {
		text : '下一首',
		bold : true,
		onClick : function() {
			$.alert("下一首");
		}
	}, {
		text : '播放',
		bold : true,
		onClick : function() {
			$.alert("播放");
		}
	}, {
		text : '暂停',
		bold : true,
		onClick : function() {
			$.alert("暂停");
		}
	}, {
		text : '音量+',
		bold : true,
		onClick : function() {
			$.alert("音量+");
		}
	}, {
		text : '音量-',
		bold : true,
		onClick : function() {
			$.alert("音量-");
		}
	} ];
	var buttons2 = [ {
		text : '取消',
		bg : 'danger'
	} ];
	var groups = [ buttons1, buttons2 ];
	$.actions(groups);
});
/********************************************** 门禁 **********************************************/
$(document).on('click', '.entrance-guard-action', function() {
	var buttons1 = [ {
		text : '请选择',
		label : true
	}, {
		text : '开门',
		bold : true,
		onClick : function() {
			$.alert("开门");
		}
	}, {
		text : '关门',
		bold : true,
		color : 'danger',
		onClick : function() {
			$.alert("关门");
		}
	} ];
	var buttons2 = [ {
		text : '取消',
		bg : 'danger'
	} ];
	var groups = [ buttons1, buttons2 ];
	$.actions(groups);
});