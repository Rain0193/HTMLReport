class TemplateMixin(object):
    # 定义生成HTML结果文件所需要的模板。
    # 如果我们想改变HTML的格式等待，可以在这里进行改动

    STATUS = {
        0: 'pass',
        1: 'fail',
        2: 'error',
        3: 'skip',
    }

    DEFAULT_TITLE = '测试报告'
    DEFAULT_DESCRIPTION = '无测试描述'

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{title}</title>
    <meta name="generator" content="{generator}"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    {stylesheet}
    <script language="javascript" type="text/javascript">{js}</script>
</head>
<body onload="load()">

{heading}
{log}
{report}
{ending}
<div id="popup"><div class="bg"><img src="" alt=""/></div></div>
</body>
</html>
"""
    JS = r"""output_list = Array();

function showCase(level) {
trs = document.getElementsByTagName("tr");
for (var i = 0; i < trs.length; i++) {
tr = trs[i];
id = tr.id;
if (id.substr(0, 2) === "st") {
if (level === 4 || level === 3) {
tr.className = "";
} else {
tr.className = "hiddenRow";
}
}
if (id.substr(0, 2) === "ft") {
if (level === 4 || level === 2) {
tr.className = "";
} else {
tr.className = "hiddenRow";
}
}
if (id.substr(0, 2) === "pt") {
if (level === 4 || level === 1) {
tr.className = "";
} else {
tr.className = "hiddenRow";
}
}
}
}

function showClassDetail(cid, count) {
var id_list = Array(count);
var toHide = 1;
for (var i = 0; i < count; i++) {
tid0 = "t" + cid.substr(1) + "." + (i + 1);
tid = "f" + tid0;
tr = document.getElementById(tid);
if (!tr) {
tid = "p" + tid0;
tr = document.getElementById(tid);
if (tr === null) {
tid = "s" + tid0;
tr = document.getElementById(tid);
}
}
id_list[i] = tid;
if (tr.className) {
toHide = 0;
}
}
for (var i = 0; i < count; i++) {
tid = id_list[i];
if (toHide && tid.indexOf("p") !== -1) {
document.getElementById(tid).className = "hiddenRow";
} else {
document.getElementById(tid).className = "";
}
if (tid.indexOf("f") !== -1) {
document.getElementById("div_" + tid).style.display = "none";
}
}
}

function showTestDetail(div_id) {
var details_div = document.getElementById(div_id);
var displayState = details_div.style.display;
if (displayState != "block") {
displayState = "block";
details_div.style.display = "block";
} else {
details_div.style.display = "none";
}
}

function html_escape(s) {
s = s.replace(/&/g, "&amp;");
s = s.replace(/</g, "&lt;");
s = s.replace(/>/g, "&gt;");
return s;
}

function load() {
var imgs = document.getElementsByClassName("pic");
var lens = imgs.length;
var popup = document.getElementById("popup");
for (var i = 0; i < lens; i++) {
imgs[i].onclick = function(event) {
event = event || window.event;
var target = document.elementFromPoint(event.clientX, event.clientY);
showBig(target.src);
};
}
popup.onclick = function() {
popup.style.display = "none";
popup.style.zIndex = "-1";
};
function showBig(src) {
popup.getElementsByTagName("img")[0].src = src;
popup.style.display = "block";
popup.style.zIndex = "999999";
}
}"""

    STYLESHEET_TMPL = r"""<style type="text/css" media="screen">body{font-family:verdana,arial,helvetica,sans-serif;font-size:100%}
table{font-size:100%}
pre{word-wrap:break-word;word-break:break-all;overflow:auto}
h1{font-size:16pt;color:gray}
.heading{margin-top:0;margin-bottom:1ex}
.heading .attribute{margin-top:1ex;margin-bottom:0}
.heading .description{margin-top:4ex;margin-bottom:6ex}
a.popup_link:hover{color:red}
.popup_window{display:none;position:relative;left:0;top:0;padding:10px;background-color:#E6E6D6;font-family:"Lucida Console","Courier New",Courier,monospace;text-align:left;font-size:8pt}
#show_detail_line{margin-top:3ex;margin-bottom:1ex}
#result_table{width:100%;border-collapse:collapse;border:1px solid #777}
#header_row{font-weight:700;color:#fff;background-color:#777}
#result_table td{border:1px solid #777;padding:2px}
#total_row{font-weight:700}
.passClass{background-color:#6c6}
.failClass{background-color:#c60}
.errorClass{background-color:#c00}
.skipClass{background-color:#c95}
.failCase{color:#c60;font-weight:700}
.errorCase{color:#c00;font-weight:700}
.skipCase{color:#c95;font-weight:700}
.hiddenRow{display:none}
.testcase{margin-left:2em}
#popup{position:fixed;left:0;top:0;width:100%;height:100%;text-align:center;display:none}
#popup .bg{background-color:rgba(0,0,0,.5);width:100%;height:100%}
@media \0screen\,screen\9{#popup .bg{background-color:#000;filter:Alpha(opacity=50);position:static}
#popup .bg img{position:relative}
}
#popup img{max-width:100%;max-height:100%;margin:auto;position:absolute;top:0;left:0;bottom:0;right:0}
</style>"""

    HEADING_TMPL = r"""<div class='heading'>
<h1>{title}</h1>
{parameters}
<p class='description'>{description}</p>
</div>"""
    HEADING_ATTRIBUTE_TMPL = r"""<p class='attribute'><strong>{name}：</strong> {value}</p>"""
    REPORT_TMPL = r"""<p id='show_detail_line'>筛选
<a href='javascript:showCase(0)'>摘要</a>
<a href='javascript:showCase(1)'>通过</a>
<a href='javascript:showCase(2)'>失败</a>
<a href='javascript:showCase(3)'>跳过</a>
<a href='javascript:showCase(4)'>全部</a>
</p>
<table id='result_table'>
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row'>
    <td>Test Group/Test case</td>
    <td>计数</td>
    <td>通过</td>
    <td>失败</td>
    <td>错误</td>
    <td>跳过</td>
    <td>查看</td>
</tr>
{test_list}
<tr id='total_row'>
    <td>合计</td>
    <td>{count}</td>
    <td>{Pass}</td>
    <td>{fail}</td>
    <td>{error}</td>
    <td>{skip}</td>
    <td>&nbsp;</td>
</tr>
</table>
"""
    REPORT_CLASS_TMPL = r"""
<tr class='{style}'>
    <td>{desc}</td>
    <td>{count}</td>
    <td>{Pass}</td>
    <td>{fail}</td>
    <td>{error}</td>
    <td>{skip}</td>
    <td><a href="javascript:showClassDetail('{cid}',{count})">细节</a></td>
</tr>
"""
    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='{tid}' class='{Class}'>
    <td class='{style}'><div class='testcase'>{desc}</div></td>
    <td colspan='6' align='center'>

    <!--css div popup start-->
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_{tid}')" >
        {status}</a>

    <div id='div_{tid}' class="popup_window">
        <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_{tid}').style.display = 'none' " >
           [x]</a>
        </div>
        <pre>
            {script}
        </pre>
        <div>{img}</div>
    </div>
    <!--css div popup end-->

    </td>
</tr>
"""
    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='{tid}' class='{Class}'>
    <td class='{style}'><div class='testcase'>{desc}</div></td>
    <td colspan='6' align='center'>{status}</td>
</tr>
"""
    REPORT_TEST_OUTPUT_TMPL = r"""
{id}: {output}
"""
    ENDING_TMPL = r"""<div id='ending'>&nbsp;</div>"""
    REPORT_LOG_FILE_TMPL = r"""
<a href='{log_file}'>下载日志文件</a>
"""
    REPORT_IMG_TMPL = r"""
<img class="pic" src='{img_src}' style="width: 500px;">
    """
