window.onload=function(){Particles.init
({selector:'.background'});};;var CLK_RANDOC_NUM=0
$(function(){thememode();get_rank();})
function get_rank(){$.ajax({url:"/rank/",type:'get',dataType:'json',success:function(res){let ranktbody=$("#ranktbody")
let rankinfo=res.rankinfo
ranktbody.children().remove()
for(let i=0;i<rankinfo.length;i++){if(i%2===0){class_status='even'}else{class_status='odd'}
let tr=$("<tr>").attr({'class':class_status,})
let td1=$("<td>").attr({'class':"text-center sorting_1"})
let td1_div=$("<div class='avatar avatar-md rounded-circle'>")
let avatar_img=$("<img alt='avatar' class='rounded-circle'>").attr('src',rankinfo[i].avatar)
td1_div.append(avatar_img);td1.append(td1_div)
let td2=$("<td>")
let usrname=$("<p class='tx-14 font-weight-semibold text-dark mb-1'>")
usrname.text(rankinfo[i].name)
td2.append(usrname)
let td3=$("<td>")
let read_num_span=$("<span class='badge bg-gradient text-muted tx-13'>").text(rankinfo[i].read_num)
td3.append(read_num_span)
let td4=$("<td>")
let upload_span=$("<span class='badge bg-light text-muted tx-13'>").text(rankinfo[i].upload_num)
td4.append(upload_span)
let td5=$("<td>")
let date_span=$("<span class='text-muted tx-13'>").text(rankinfo[i].register_date)
td5.append(date_span)
tr.append(td1)
tr.append(td2)
tr.append(td3)
tr.append(td4)
tr.append(td5)
ranktbody.append(tr)}}})}
function get_randoc(){$.ajax({url:"/doc/random/",type:'get',dataType:'json',data:{'cid':CLK_RANDOC_NUM},success:function(res){let doccard=$("#doccard")
doccard.children().remove()
let a=$("<a>").attr({'href':"/media/docs/"+res.doc_cover_name+".pdf",'class':"card",'style':"display:flex;align-items: center;"})
let cover=$("<img>").attr({'src':res.doc_cover_url,'alt':"图片不存在",'width':'256px','height':'256px','class':"animate__animated animate__flipInX"})
let doc_name=$("<div style='justify-content: center;display: flex;'>").text(res.doc_cover_name)
a.append(cover)
doccard.append(a)
doccard.append(doc_name)
CLK_RANDOC_NUM+=1}})}
function thememode(){const options={bottom:'unset',right:'unset',left:'15px',time:'0.5s',mixColor:'#fff',backgroundColor:'#fff',buttonColorDark:'#100f2c',buttonColorLight:'#fff',saveInCookies:true,label:'🌓',autoMatchOsTheme:true}
function addDarkmodeWidget(){let darkmode=new Darkmode(options);darkmode.showWidget();$(".darkmode-toggle").on('click',function(){if(darkmode.isActivated()){$(".panel").attr('class','panel panel-success')
$(".list-group-item[id]").css({"color":"#3c763d","background-color":"#a5d29a","border-color":"#d6e9c6"});}else{$(".panel").attr('class','panel panel-info')
$(".list-group-item[id]").css({"color":"#3c763d","background-color":"#dff0d8","border-color":"#d6e9c6"});}})}
window.addEventListener('load',addDarkmodeWidget);}
function getFormatDate(){var date=new Date();var month=date.getMonth()+1;var strDate=date.getDate();var hours=date.getHours();var minutes=date.getMinutes();var seconds=date.getSeconds();if(month>=1&&month<=9){month="0"+month;}
if(strDate>=0&&strDate<=9){strDate="0"+strDate;}
if(hours>=0&&hours<=9){hours="0"+hours;}
if(minutes>=0&&minutes<=9){minutes="0"+minutes;}
if(seconds>=0&&seconds<=9){seconds="0"+seconds;}
return date.getFullYear()+"-"+month+"-"+strDate
+" "+date.getHours()+":"+minutes+":"+seconds;};