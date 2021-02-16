// Check if cookies have been accepted and sets the settings accordingly
if (!getCookie("acceptCookies")){
  $("#originalImageCheck").prop("checked",true);
  $("#keywordsImageCheck").prop("checked",false);
  $("#allCheck").prop("checked",true);
  for (var i = 0; i < newsSitesHashTag.length; i++) {
    $(newsSitesHashTag[i]).prop("checked",true);
  }         
} else {
  $("#originalImageCheck").prop("checked",JSON.parse(localStorage.getItem("originalImageCheck")));
  $("#keywordsImageCheck").prop("checked",JSON.parse(localStorage.getItem("keywordsImageCheck")));
  $("#allCheck").prop("checked",JSON.parse(localStorage.getItem("allCheck")));
  for (var i = 0; i < newsSitesHashTag.length; i++) {
    $(newsSitesHashTag[i]).prop("checked",JSON.parse(localStorage.getItem(newsSitesCheck[i])));
  }  
  if($("#allCheck").is(':checked')){
    $("#allCheckLabel").html("Deselect All");     
  } else {
    $("#allCheckLabel").html("Select All");     
  }        
}   

// Disable cookies by setting the acceptCookies to false, the expiration days to 0 and clearing the local storage
$("#disableCookiesButton").click(function(){
  setCookie("acceptCookies", false, 0);
  localStorage.clear();
});

$("#originalImageCheck").on("change",function(){
  if(getCookie("acceptCookies")){
    localStorage.setItem("originalImageCheck", document.getElementById("originalImageCheck").checked);
    localStorage.setItem("keywordsImageCheck", !document.getElementById("originalImageCheck").checked);
  }      
  $("#keywordsImageCheck").prop("checked",!document.getElementById("originalImageCheck").checked); 
});   

$("#keywordsImageCheck").on("change",function(){
  if(getCookie("acceptCookies")){
    localStorage.setItem("keywordsImageCheck", document.getElementById("keywordsImageCheck").checked);
    localStorage.setItem("originalImageCheck", !document.getElementById("keywordsImageCheck").checked);      
  }
  $("#originalImageCheck").prop("checked",!document.getElementById("keywordsImageCheck").checked);       
});   

$("#allCheck").on("change",function(){
  if(getCookie("acceptCookies")){
    localStorage.setItem("allCheck", document.getElementById("allCheck").checked);
  }    
  if($("#allCheck").is(':checked')){
    $("#allCheckLabel").html("Deselect All");
    for(var i = 0; i <newsSitesCheck.length; i++){
      $(newsSitesHashTag[i]).prop("checked",true);
      if(getCookie("acceptCookies")){
        localStorage.setItem(newsSitesCheck[i], document.getElementById(newsSitesCheck[i]).checked);
      }
    }      
  } else {
    $("#allCheckLabel").html("Select All");
    for(var j = 0; j <newsSitesCheck.length; j++){
      $(newsSitesHashTag[j]).prop("checked",false);
      if(getCookie("acceptCookies")){
        localStorage.setItem(newsSitesCheck[j], document.getElementById(newsSitesCheck[j]).checked);
      }
    }      
  }    
});

// Save checked settings if cookies are enabled
queryArray.forEach(item => {
  item.addEventListener('change', event => {
    if(getCookie("acceptCookies")){
      localStorage.setItem(item.id, document.getElementById(item.id).checked);      
    } 
  });
}); 