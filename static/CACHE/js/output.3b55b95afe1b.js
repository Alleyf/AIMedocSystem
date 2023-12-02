var KEYWORD
var IMG_UID
$(function(){get_info();})
function bindbtnimg(){console.log(IMG_UID)
$("#btn_img").click(function(){IMG_UID=$(this).siblings('<a>').first().attr('uid')
console.log(IMG_UID)
$.ajax({url:"/doc/img/",type:'post',data:{csrfmiddlewaretoken:'',uid:IMG_UID},dataType:'json',success:function(res){let card=$("#imgcard");card.children().remove();if(res.status===200){let img_residue=res.names.length;let num=0;first:for(let i=0;i<res.names.length;i++){let row=$("<div>")
row.attr({'class':'row','style':'width:100%;margin: 0 auto'})
if(i%4===0){for(let j=0;j<4;j++){if(res.names[i+j]===undefined){break first}else{html="<div style='width:25%;margin: 0 auto' class=\"card col-12 col-md-3 p-3 fanimate\">"+"<img style='min-width: 100%px!important;' width='128px' height='128px' src = "+"\""+res.paths[i+j]+"\""+" class =\"card-img-top\" alt = \"\">"+"<div class=\"card-body\">"+"<h5 class=\"card-title text-center\" >"+"页码-编号："+res.names[i+j]+"</h5></div>"
row.append(html)
card.append(row)}}}}}else{html="<h5 class='text-danger' style='width:50%;margin: 0 auto'>抱歉，该文献中未发现图片！</h5>"
card.append(html)
console.log(res)}}})})}
function get_info(){$("#search").click(function(){$(".info").children().remove()
let keyword=$("#keyword").val();$.ajax({url:"/doc/search/",type:'get',data:{'keyword':keyword},dataType:'json',success:function(res){if(res.code===200){$("#tb").attr('style','display:block')
trcss=['table-primary','table-secondary','table-success','table-danger','table-warning','table-light']
$(".page_str").html(res.page_info)
var page_info=res.page_info
for(let item in page_info){let id=page_info[item].id
IMG_UID=id;let uid=$('<th>').text(id)
let title=$('<td>').text(page_info[item].name)
let fedbakscore=$('<td>').text(page_info[item].fedbakscore)
let clkscore=$('<td>').text(page_info[item].clkscore)
let relscore=$('<td>').text(page_info[item].relscore)
let allscore=$('<td>').text(page_info[item].allscore)
let details=$('<a>').attr({"href":"/doc/details/?text="+keyword+"&uid="+id,"uid":id,"class":"btn btn-info btn-xs"})
let btn_img='<button id="btn_img" type="button" class="btn btn-xs btn-primary btn_img" \
                                        data-bs-toggle="modal" data-bs-target="#ImageModal"><i class="fa-solid fa-image"></i></button>'
details.html("<i class='fa-solid fa-eye'></i>")
let details_td=$("<td>")
details_td.append(details)
details_td.append(btn_img)
let tr=$('<tr>').attr({'uid':id,'class':trcss[item%6]})
tr.append(uid)
tr.append(title)
tr.append(fedbakscore)
tr.append(clkscore)
tr.append(relscore)
tr.append(allscore)
tr.append(details_td)
$(".info").append(tr)
console.log()}}else{console.log(res.error)}}});});};