<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="/struts-tags" prefix="s" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Insert title here</title>
</head>
<body>
<h2>模板录入</h2>

    <s:fielderror />
    <s:form action="register" method="post">   
        <s:textfield label="站点名字" name="website.name" tooltip="站点名字 如：百度"></s:textfield>
        <s:textfield label="频道地址" name="website.channel" tooltip="频道的url地址"></s:textfield>
        <s:select name="website.region" list="#{'Territory':'境内','Abroad':'境外'}" label="境内外" headerKey="Territory" headerValue="选择境内外"></s:select>
        <s:select name="website.contry" list="#{'CN':'中国','US':'美国','JP':'日本','UK','英国'}" label="国家" headerKey="CN" headerValue="选择国家"></s:select>
        <s:select name="website.language" list="#{'CN':'中文','US':'英文','JP':'日文'}" label="语言" headerKey="CN" headerValue="选择语言"></s:select>
        <br />
        <!-- 
        <s:textfield label="start_time" name="website.start_time"></s:textfield>
        <s:textfield label="stop_time" name="website.stop_time" tooltip="age must over 16"></s:textfield>
         -->
        <s:textfield label="文章标题的path" name="website.title" tooltip="标签"></s:textfield>
        <s:textfield label="文章作者的path" name="website.author" tooltip="标签"></s:textfield>
        <s:textfield label="发布时间的path" name="website.pubtime" tooltip="i标签"></s:textfield>
        <s:textfield label="正文的path" name="website.content" tooltip="标签"></s:textfield>
        <s:textfield label="转发来源的path" name="website.source" tooltip="标签"></s:textfield>
		<br />
        <s:submit label="Register" value="录入"></s:submit>  
   		<s:submit label="Register" action="register2"  value="查看" ></s:submit>  
 	</s:form>
 	
 	
</body>
</html>