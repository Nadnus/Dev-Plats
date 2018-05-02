$(document).ready(function(){

  $("div.profile").click(function(){
    //Brings up the profile of the person
  });

  $("#arrowSubmit").click(function(){
    //Submit text
    var text = document.getElementById("inputUser").value;
    document.getElementById("inputUser").value = "";
    alert(text);
    var bub = document.getElementById("userBubble");
    var bclone = bub.cloneNode(true);
    bclone.innerHTML = text;
    bclone.setAttribute("hidden") = false;
    document.getElementById("chatBox").appendChild(bclone);
  });

  var chat = document.getElementById('def-chat');
  $("#def-chat").hide();
  //Gets the default chat elements to be copied
});
