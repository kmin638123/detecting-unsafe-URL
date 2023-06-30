// Initialize butotn with users's prefered color


let changeColor = document.getElementById("changeColor");
var power=0;
var level = "mid"


chrome.storage.sync.get("color", ({ color }) => {
  // 버튼 상태 유지 코드
  $(function(){
    var test = localStorage.input === 'true'? true: false;
    $('input').prop('checked', test || false);  
    console.log(localStorage.input)
    setPageBackgroundColor()
    
  });
  $('input').on('change', function() {
    localStorage.input = $(this).is(':checked');
    var power=1;
    if($(this).is(':checked')){
      document.getElementById("opt-2").style.color="#1F99D3";
      document.getElementById("opt-2").style.fontWeight="600";
      document.getElementById("opt-1").style.color="GRAY";
      power=1
      chrome.storage.sync.set({test: false}, function() {
        //alert('Value is set to ' + power);
      });
    }
    else{
      document.getElementById("opt-2").style.color="GRAY";
      document.getElementById("opt-1").style.fontWeight="600";
      document.getElementById("opt-1").style.color="BLACK";
      power=0;
      chrome.storage.sync.set({test: true}, function() {
        //alert('Value is set to ' + power);
      });
    } 
    console.log(power);
  });
});

function setPageBackgroundColor() {
  chrome.storage.sync.get(['test'], function(result) {
    var a_s= document.querySelectorAll("a[href]")
    console.log('Value currently is ' + result.test);
    console.log(document.URL)
    url_ = document.URL

    list= null
    new_as = []
    as_url = []
    
    /*for (var i = 0, l = a_s.length; i < l; i++){
      if (a_s[i].getAttribute('href').slice(0,4)=='http'){
        child = a_s[i].childNodes
        tagornot = true
        for (var j=0; j<child.length;j++){
          if (child[j].nodeName=='IMG' || child[j].nodeName=='I' ){
            tagornot = false
          }
          else if (child[j].nodeName=='SPAN'||child[j].nodeName=='DIV'){
            t_child = child[j].childNodes
            for (var k=0; k<t_child.length;k++){
              if (t_child[k].nodeName=='IMG' || t_child[k].nodeName=='I' ){
                tagornot = false
              }
            }
          }
        }
        if (tagornot){
          if (a_s[i]["href"].slice(0,4) == "https"){
            if (!as_url.includes(a_s[i]["href"].slice(7,-1))){
              as_url.push(a_s[i]["href"].slice(7,-1))
              console.log(a_s[i]["href"].slice(7,-1))
              new_as.push(a_s[i])
            }
          }
          else{
            if (!as_url.includes(a_s[i]["href"].slice(8,-1))){
              as_url.push(a_s[i]["href"].slice(8,-1))
              console.log(a_s[i]["href"].slice(8,-1))
              new_as.push(a_s[i])
            }
          }
        }
      }
    }*/
    for (var i = 0, l = a_s.length; i < l; i++){
      if (a_s[i].getAttribute('href').slice(0,4)=='http'){
        child = a_s[i].childNodes
        for (var j=0; j<child.length;j++){
          //console.log(child[j].nodeName)
          if (child[j].nodeName=='H3'||child[j].nodeName=='#text'){
            new_as.push(a_s[i])
            if (a_s[i]["href"].slice(0,4) == "https"){
              as_url.push(a_s[i]["href"].slice(7,-1))
              //console.log(a_s[i]["href"].slice(7,-1))
            }
            else{
              as_url.push(a_s[i]["href"].slice(8,-1))
              //console.log(a_s[i]["href"].slice(8,-1))
            }
            break
          }
        }
      }
    }
    //console.log(as_url.toString())
    urls = as_url.toString()
    state = []


    $.ajax({
      type: 'POST',
      url: 'http://127.0.0.1:1024',
      data: {urls:urls, test: result.test},
      dataType :'json',
      async: false,
      success: function(d){
        state = d
      },
      error: function(err){
        console.log("nothing")
      }
    })

    console.log(state)
    clear_as = []
    for (var i = 0, l = new_as.length; i < l; i++){
        child =new_as[i].childNodes
        if (Number(state[i])==1){
          //console.log(new_as[i])
          new_as[i].style.color = '	#B22222'
          /*if (new_as[i].style.textDecoration!='line-through'){
            for (var j=0; j<child.length;j++){
              console.log(new_as[i])
              child[j].style.color = 'gray'
              child[j].style.textDecoration = 'line-through'
              t_child = child[j].childNodes
              if (child[j].style.textDecoration!='line-through'){
                for (var k=0; k<t_child.length;k++){
                  t_child[k].style.color = 'gray'
                  t_child[k].style.textDecoration = 'line-through'
                }
              }
            }
          }*/
        }
        /*for (var j=0; j<child.length;j++){
          //console.log(child[j].nodeName)
          if (child[j].nodeName=='H3'||child[j].nodeName=='#text'){
            //new_as[i].insertAdjacentHTML('beforeend','<img class = safety  width = "16px" height = "16px" src = "https://cdn-icons-png.flaticon.com/16/1161/1161388.png" alt="safe">')  
            new_as[i].style.color = 'gray'
            new_as[i].style.textDecoration = 'line-through'
            break
          }*/
          //else if (child[j].nodeName=='SPAN'||child[j].nodeName=='DIV'){
            //t_child = child[j].childNodes
            //for (var k=0; k<t_child.length;k++){
              //console.log(t_child[k])
              //if (t_child[k].nodeName=='#text'){
              //  child[j].insertAdjacentHTML('beforeEnd','<img class = safety  width = "15px"  src = "https://cdn-icons-png.flaticon.com/512/1161/1161388.png" alt="safe">')
              //}
              //else if (t_child[k].nodeName=='SPAN'||t_child[k].nodeName=='DIV'){
              //  tt_child = t_child[k].childNodes
              //  for (var m=0; m<tt_child.length;m++){
              //    //console.log(tt_child[m].nodeName)
              //  }
              //}
            //}
          //}
        
      }
  });
}