class TemplateMixin(object):
    # 定义生成HTML结果文件所需要的模板。

    STATUS = {
        0: 'pass',
        1: 'fail',
        2: 'error',
        3: 'skip',
    }

    DEFAULT_TITLE = '测试报告'
    DEFAULT_TITLE_en = 'Test Results'
    DEFAULT_DESCRIPTION = '测试描述'
    DEFAULT_DESCRIPTION_en = 'Test Description'

    HTML_TMPL = r"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <title>{title}</title>
  <meta name="generator" content="{generator}" />
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> {stylesheet}
  <script language="javascript" type="text/javascript">{js}</script>
</head>

<body onload="load()">
  <div id="wrapper" class="lang-{lang}">
    <div id="lang">
      <ul>
        <li>
          <a href="#cn" id="lang-cn" title="简体中文">cn</a>
        </li>
        <li>
          <a href="#en" id="lang-en" title="English">en</a>
        </li>
      </ul>
    </div>
    {heading} {log} {report} {ending}
    <div id="popup">
      <div class="bg">
        <img src="" alt="" />
      </div>
    </div>
  </div>
</body>

</html>
"""

    JS = r"""
output_list = Array();
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
    if (id.substr(0, 4) === "div_") { tr.className = "hiddenRow"; }
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
    document.getElementById("div_" + tid).className = "hiddenRow";
  }
}

function showTestDetail(div_id) {
  var details_div = document.getElementById(div_id);
  var className = details_div.className;
  if (className != "") {
    details_div.className = "";
  } else {
    details_div.className = "hiddenRow";
  }
}

function html_escape(s) {
  s = s.replace(/&/g, "&amp;");
  s = s.replace(/</g, "&lt;");
  s = s.replace(/>/g, "&gt;");
  return s;
}

function load() {
  var el_wrapper = document.getElementById('wrapper');
  document.getElementById('lang-cn').onclick = function () { el_wrapper.className = 'lang-cn'; };
  document.getElementById('lang-en').onclick = function () { el_wrapper.className = 'lang-en'; };

  var h = (location.hash || '').replace(/#/, '');
  var nav_lang;
  if (h != 'cn' || h != 'en') {
    el_wrapper.className = 'lang-' + h;
  }

  var imgs = document.getElementsByClassName("pic");
  var lens = imgs.length;
  var popup = document.getElementById("popup");
  for (var i = 0; i < lens; i++) {
    imgs[i].onclick = function (event) {
      event = event || window.event;
      var target = document.elementFromPoint(event.clientX, event.clientY);
      showBig(target.src);
    };
  }
  popup.onclick = function () {
    popup.getElementsByTagName("img")[0].src = "";
    popup.style.display = "none";
    popup.style.zIndex = "-1";
  };
  function showBig(src) {
    popup.getElementsByTagName("img")[0].src = src;
    popup.style.display = "block";
    popup.style.zIndex = "999999";
  }
}
"""

    STYLESHEET_TMPL = r"""<style type="text/css" media="screen">
  body {
    font-family: verdana, arial, helvetica, sans-serif;
    font-size: 100%
  }

  table {
    font-size: 100%
  }

  pre {
    word-wrap: break-word;
    word-break: break-all;
    overflow: auto
  }

  h1 {
    font-size: 16pt;
    color: gray
  }

  .heading {
    margin-top: 0;
    margin-bottom: 1ex
  }

  .heading .attribute {
    margin-top: 1ex;
    margin-bottom: 0
  }

  .heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex
  }

  a.popup_link:hover {
    color: red
  }

  .popup_window {
    display: block;
    position: relative;
    left: 0;
    top: 0;
    padding: 10px;
    background-color: #E6E6D6;
    font-family: "Lucida Console", "Courier New", Courier, monospace;
    text-align: left;
    font-size: 8pt
  }

  #show_detail_line {
    margin-top: 3ex;
    margin-bottom: 1ex
  }

  #result_table {
    width: 100%;
    border-collapse: collapse;
    border: 1px solid #777
  }

  #header_row {
    font-weight: 700;
    color: #fff;
    background-color: #777
  }

  #result_table td {
    border: 1px solid #777;
    padding: 2px;
    min-width: 35px
  }

  #total_row {
    font-weight: 700
  }

  .passClass {
    background-color: #97cc64;
    font-weight: bold
  }

  .failClass {
    background-color: #fd5a3e;
    font-weight: bold
  }

  .errorClass {
    background-color: #ffd050;
    font-weight: bold
  }

  .skipClass {
    background-color: #aaa;
    font-weight: bold
  }

  .passCase {
    background-color: #97cc64
  }

  .failCase {
    background-color: #fd5a3e
  }

  .errorCase {
    background-color: #ffd050
  }

  .skipCase {
    background-color: #aaa
  }

  .hiddenRow {
    display: none
  }

  .testcase {
    margin-left: 2em
  }

  #popup {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    text-align: center;
    display: none
  }

  #popup .bg {
    background-color: rgba(0, 0, 0, .5);
    width: 100%;
    height: 100%
  }

  @media \0screen\,screen\9 {
    #popup .bg {
      background-color: #000;
      filter: Alpha(opacity=50);
      position: static
    }
    #popup .bg img {
      position: relative
    }
  }

  #popup img {
    max-width: 100%;
    max-height: 100%;
    margin: auto;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0
  }

  img.pic {
    width: 500px;
  }

  #wrapper {
    margin: 0 auto;
    border-top: solid 2px #666;
  }

  #wrapper .lang-en {
    display: none;
  }

  #wrapper.lang-cn p.lang-cn {
    display: block;
  }

  #wrapper.lang-cn span.lang-cn {
    display: inline;
  }

  #wrapper.lang-cn .lang-en {
    display: none;
  }

  #wrapper.lang-en .lang-cn {
    display: none;
  }

  #wrapper.lang-en p.lang-en {
    display: block;
  }

  #wrapper.lang-en span.lang-en {
    display: inline;
  }

  #lang ul {
    float: right;
    margin: 0;
    padding: 2px 10px 4px 10px;
    background: #666;
    border-radius: 0 0 4px 4px;
    list-style: none;
  }

  #lang li {
    margin: 0;
    float: left;
    padding: 0 5px;
  }

  #lang li a {
    display: block;
    width: 24px;
    height: 24px;
    text-indent: -4em;
    overflow: hidden;
    background: transparent url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAHiSURBVHja1Ja/jtNAEMZ/Y2/icBdxXAMSEu/A1dBR0NJQ8CS8AQ0tb4CQgEegPgQFOh7ixJUX4vgSx96ZoUgOO3+KRDgFX7Or0Wg+f7PzeVfcnUMi4cA4OIEAARgAvY5r10AZgOGvl69Gkm4Xk9w3fJTg9f4MDz9+OA3AsSTC4OmThaQE3Bp9w+eRmy+hie2I8us3gOMABFNFkjlW5PTPIvOLAO7YVMjfC/Sd4YuK4nOGuyMiABv7v6pP7mKmACEAeK1YPuPoWU52FgkPUiaf+ngFDjCD+Q/Fproo1vrSbUPuvR4eF7kBwDRi4ynlzxkyUMrvKTZabbrPFb9Jd2qPh7BK4DGiRYFeTJmdC8nAsVKaUes72eOK6Xm2G0GaYhpXCTzPsXEBgOZN8unrktHbAddvAKrdCESwqmoItI74eILlkw0bjt4Zltdg+5hL8NhSYLGmurrCxuPN7Mv951+LAh1kLQWxBlUw68bDGtEqaStQiB0SRMWlbh1yXWPu+MIc/wzTiC0dslBQR0TArfWPwJdr21KyttLKaeJijvmaD0gTMF/z57pPt8W37E1xaylwU0iE5OhON2fgjreMVmuMXC/ntus7QYAT4BFwr+Piv4HL2xstu21Xh4jAXP77V8WfAQAixA0rudAk0AAAAABJRU5ErkJggg==") no-repeat 50% 50%;
  }

  #lang li a#lang-en {
    background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAIWSURBVHja1JY/SBthGIefu1xqS6K20KFDy0kopUiHmphIByUZotRAIZOTWZzFpYtbB0uh6KJTIdQhi9pBSwmmCOpgoUSKFItTh4AU6tCr16Rn5P58XZocDrlYuAz9wfHAcbzv9/2+932/k4QQdFIyHVbHE0iAAlwFgj7HNoG6AoRzudc/A4F/28yL2l7bb269yd9QgJAsS8zMjFIufyWRuHspXqtbnsHrH8oAIQlQJyfzlaGhCNFohJ2dI1Kp/iZ3d49IJvsvvJckmJ197JlACIEsy30KgGUJBgcjFIufSacfsLnpza2tL/x4+qx15fR0Uz84hL8HjG1blEqHJJP9bGx8IpMZ8CSAMIzWq1cUhO24CSzLYWTkPisrH8lm46yuenN9fZ+br156WmRZFgQLjR3YrK2VyWSiFAp7TEw88iTAyZNca4t6e6h/P3EbzTRtxscfks9vk83G27JaPcOuVls/v6o4pltlajo9L1KpebG8vC9isbm2jMXmRDsZhiEAVWn4NTU1ysJCkenpMRYXS55cWnrPcSThUUVhzrquNEeFOjz8vOI4CrXa+aU7+d3p29YJusMYwQD3Drb7AFRd14Xf0nXdtehbfAxdkhG13/5M0HCImiTcPhC2BVIAHMefOWrbCNxYqqZpvlukaVrTIrNye4CK1JH7xpSAXuAOcN3n4KfAceNG62qch4+ygHPpv/+r+DMAXV79BpyNnBoAAAAASUVORK5CYII=");
  }
</style>"""

    HEADING_TMPL = r"""<div class='heading'>
  <h1>{title}</h1>
  <p class='attribute'>
    <strong>
      <span class="lang-cn">启动时间：</span>
      <span class="lang-en">Start Time:</span>
    </strong> {startTime}
  </p>
  <p class='attribute'>
    <strong>
      <span class="lang-cn">结束时间：</span>
      <span class="lang-en">End Time:</span>
    </strong> {endTime}
  </p>
  <p class='attribute'>
    <strong>
      <span class="lang-cn">运行时长：</span>
      <span class="lang-en">Duration:</span>
    </strong> {duration}
  </p>
  <p class='attribute'>
    <strong>
      <span class="lang-cn">结果：</span>
      <span class="lang-en">Status:</span>
    </strong>
    <span class="lang-cn">合计：</span>
    <span class="lang-en">Total:</span>{total}&nbsp;&nbsp;&nbsp;&nbsp;
    <span class="lang-cn">通过：</span>
    <span class="lang-en">Passed:</span>{Pass}&nbsp;&nbsp;&nbsp;&nbsp;
    <span class="lang-cn">失败：</span>
    <span class="lang-en">Failed:</span>{fail}&nbsp;&nbsp;&nbsp;&nbsp;
    <span class="lang-cn">错误：</span>
    <span class="lang-en">Error:</span>{error}&nbsp;&nbsp;&nbsp;&nbsp;
    <span class="lang-cn">跳过：</span>
    <span class="lang-en">Skipped:</span>{skip}&nbsp;&nbsp;&nbsp;&nbsp;
  </p>
  <p class='description'>{description}</p>
</div>"""

    REPORT_TMPL = r"""
<p id='show_detail_line'>筛选
  <a href='javascript:showCase(0)'>
    <span class="lang-cn">摘要</span>
    <span class="lang-en">Summary</span>
  </a>
  <a href='javascript:showCase(1)'>
    <span class="lang-cn">通过</span>
    <span class="lang-en">Pass</span>
  </a>
  <a href='javascript:showCase(2)'>
    <span class="lang-cn">失败</span>
    <span class="lang-en">Fail</span>
  </a>
  <a href='javascript:showCase(3)'>
    <span class="lang-cn">跳过</span>
    <span class="lang-en">Skip</span>
  </a>
  <a href='javascript:showCase(4)'>
    <span class="lang-cn">全部</span>
    <span class="lang-en">All</span>
  </a>
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
    <td>
      <span class="lang-cn">测试组/测试用例</span>
      <span class="lang-en">Test Group/Test case</span>
    </td>
    <td>
      <span class="lang-cn">计数</span>
      <span class="lang-en">Count</span>
    </td>
    <td>
      <span class="lang-cn">通过</span>
      <span class="lang-en">Pass</span>
    </td>
    <td>
      <span class="lang-cn">失败</span>
      <span class="lang-en">Fail</span>
    </td>
    <td>
      <span class="lang-cn">错误</span>
      <span class="lang-en">Error</span>
    </td>
    <td>
      <span class="lang-cn">跳过</span>
      <span class="lang-en">Skip</span>
    </td>
    <td>
      <span class="lang-cn">查看</span>
      <span class="lang-en">View</span>
    </td>
  </tr>
  {test_list}
  <tr id='total_row'>
    <td>
    <span class="lang-cn">合计</span>
    <span class="lang-en">Total</span>
    </td>
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
  <td>
    <a href="javascript:showClassDetail('{cid}',{count})">
      <span class="lang-cn">细节</span>
      <span class="lang-en">Detail</span>
    </a>
  </td>
</tr>
"""

    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='{tid}' class='{Class}'>
  <td class='{style}'>
    <div class='testcase'>{desc}</div>
  </td>
  <td class='{style}' colspan='6' align='center'>
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_{tid}')">{status}</a>
  </td>
</tr>
<tr id='div_{tid}' class="hiddenRow">
  <td colspan='7'>
    <div class="popup_window">
      <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_{tid}').className = 'hiddenRow' ">[x]</a>
      </div>
      <pre>{script}</pre>
      <div>{img}</div>
    </div>
  </td>
</tr>
"""

    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='{tid}' class='{Class}'>
  <td class='{style}'>
    <div class='testcase'>{desc}</div>
  </td>
  <td class='{style}' colspan='6' align='center'>{status}</td>
</tr>
"""

    REPORT_TEST_OUTPUT_TMPL = r"""
{id}: 
{output}
"""

    ENDING_TMPL = r"""<div id='ending'>&nbsp;</div>"""

    REPORT_LOG_FILE_TMPL = r"""
<a href='{log_file}'>
  <span class="lang-cn">下载日志文件</span>
  <span class="lang-en">Download log file</span>
</a>
"""

    REPORT_IMG_TMPL = r"""
<img class="pic" src='{img_src}'>
"""
