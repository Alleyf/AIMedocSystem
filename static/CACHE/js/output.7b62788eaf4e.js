var code;changeImg();document.getElementById("id_code").onclick=changeImg;turnaudio();function changeImg(){var arrays=['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];code='';for(var i=0;i<4;i++){var r=parseInt(Math.random()*arrays.length);code+=arrays[r];}
document.getElementById('id_code').innerHTML=code;}
function check(){let input_code=document.getElementById('vcode').value;return input_code.toLowerCase()===code.toLowerCase();}
function turnaudio(){setInterval(function(){const show=document.querySelector('span[data-show]')
const next=show.nextElementSibling||document.querySelector('span:first-child')
const up=document.querySelector('span[data-up]')
if(up){up.removeAttribute('data-up')}
show.removeAttribute('data-show')
show.setAttribute('data-up','')
next.setAttribute('data-show','')},2000)};window.onload=function(){Particles.init
({selector:'.background'});};;