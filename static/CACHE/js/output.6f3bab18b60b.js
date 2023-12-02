$(function(){add_avatar_value();})
function add_avatar_value(){$('input[id=id_avatar]').change(function(){if($(this).val()!==''){console.log($(this).val())
showImg($(this)[0]);$("#avatar_value").text($(this).val())}else{}});}
function showImg(obj){var objUrl=getObjectURL(obj.files[0]);if(objUrl){$("#avatar_wrapper").css('border','medium')
$("#avatar_container").html('<img class="rounded-circle" src="'+objUrl+'" alt="" style="width:88px;height:88px;margin: auto">')}}
function getObjectURL(file){var url=null;if(window.createObjectURL!==undefined){url=window.createObjectURL(file);}else if(window.URL!==undefined){url=window.URL.createObjectURL(file);}else if(window.webkitURL!==undefined){url=window.webkitURL.createObjectURL(file);}
return url;};