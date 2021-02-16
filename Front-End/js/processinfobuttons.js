if (!getCookie("acceptCookies")){
  // If cookies are not accepted the default settings are loaded
  $("#originalImageCheck").prop("checked",true);
  $("#keywordsImageCheck").prop("checked",false);      
  $("#allCheck").prop("checked",true);
  for (var i = 0; i < newsSitesHashTag.length; i++) {
    $(newsSitesHashTag[i]).prop("checked",true);
  }
  setOriginalImages();                  
}
else {
  // If cookies are accepted the settings are loaded and set from the local storage
  $("#originalImageCheck").prop("checked",JSON.parse(localStorage.getItem("originalImageCheck")));
  $("#keywordsImageCheck").prop("checked",JSON.parse(localStorage.getItem("keywordsImageCheck")));      
  $("#allCheck").prop("checked",JSON.parse(localStorage.getItem("allCheck")));
  for (var i = 0; i < newsSitesHashTag.length; i++) {
    $(newsSitesHashTag[i]).prop("checked",JSON.parse(localStorage.getItem(newsSitesCheck[i])));
  }

  if($("#allCheck").is(':checked')){
    $("#allCheckLabel").html("Deselect All");
    for(var i = 0; i <newsSites.length; i++){
      if($("#" + newsSites[i] + "Check").is(':checked')){
        $("#" + newsSites[i]).show();
      } else {
        $("#" + newsSites[i]).hide();
      }
    }      
  } else {
    $("#allCheckLabel").html("Select All");
    for(var j = 0; j <newsSites.length; j++){
      if($("#" + newsSites[j] + "Check").is(':checked')){
        $("#" + newsSites[j]).show();
      } else {
        $("#" + newsSites[j]).hide();
      }
    }
  }

  if($("#originalImageCheck").is(':checked')){
    setOriginalImages();        
  }
  if($("#keywordsImageCheck").is(':checked')){
    setKeywordImages();         
  }

  // Handles the visibility of the news cards based on the set settings
  (function () {
    for (var i = 0; i < newsSites.length; i++) {
      if($("#" + newsSites[i] + "Check").is(':checked')){
        $("#" + newsSites[i]).show();
      } else {
        $("#" + newsSites[i]).hide();
      }          
    }
  })();
}

// Event listeners for opening info boxes
queryInfoButtonArr.forEach(site => {
  site.addEventListener('click', event => {
    openInfoBox(site.id.substring(0,site.id.length-10));
  });
});

// Event listeners for closing info boxes
queryInfoCloseButtonArr.forEach(siteClose => {
  siteClose.addEventListener('click', event => {
    closeInfoBox(siteClose.id.substring(0,siteClose.id.length-15));
  });
}); 

// Original image check setting
$("#originalImageCheck").on("change",function(){
  if(getCookie("acceptCookies")){
    localStorage.setItem("originalImageCheck", document.getElementById("originalImageCheck").checked);
    localStorage.setItem("keywordsImageCheck", !document.getElementById("originalImageCheck").checked);
  }      
  $("#keywordsImageCheck").prop("checked",!document.getElementById("originalImageCheck").checked);
  if($("#originalImageCheck").is(':checked')){
    setOriginalImages();
  } else {
    setKeywordImages();       
  }   
});   

// Keyword image check setting
$("#keywordsImageCheck").on("change",function(){
  if(getCookie("acceptCookies")){
    localStorage.setItem("keywordsImageCheck", document.getElementById("keywordsImageCheck").checked);
    localStorage.setItem("originalImageCheck", !document.getElementById("keywordsImageCheck").checked);      
  }
  $("#originalImageCheck").prop("checked",!document.getElementById("keywordsImageCheck").checked);
  if($("#keywordsImageCheck").is(':checked')){
    setKeywordImages();
  } else {
      setOriginalImages();                 
  }   
});

// Select or deselect all setting
$("#allCheck").on("change",function(){
  if(getCookie("acceptCookies")){
    localStorage.setItem("allCheck", document.getElementById("allCheck").checked);
  }    
  if($("#allCheck").is(':checked')){
    $("#allCheckLabel").html("Deselect All");
    for(var i = 0; i <newsSites.length; i++){
      $("#" + newsSites[i] + "Check").prop("checked",true);
      if(getCookie("acceptCookies")){
        localStorage.setItem(newsSites[i] + "Check", document.getElementById(newsSites[i] + "Check").checked);
      }
      if($("#" + newsSites[i] + "Check").is(':checked')){
        $("#" + newsSites[i]).show();
      } else {
        $("#" + newsSites[i]).hide();
      }
    }      
  } else {
    $("#allCheckLabel").html("Select All");
    for(var j = 0; j <newsSites.length; j++){
      $("#" + newsSites[j] + "Check").prop("checked",false);
      if(getCookie("acceptCookies")){
        localStorage.setItem(newsSites[j] + "Check", document.getElementById(newsSites[j] + "Check").checked);
      }
      if($("#" + newsSites[j] + "Check").is(':checked')){
        $("#" + newsSites[j]).show();
      } else {
        $("#" + newsSites[j]).hide();
      }
    }      
  }    
});  

// Event listeners for the supported news sites checkboxes
queryArray.forEach(item => {
  item.addEventListener('change', event => {
    if(getCookie("acceptCookies")){
      localStorage.setItem(item.id, document.getElementById(item.id).checked);     
    }
    if($("#"+item.id).is(':checked')){
      $("#" + item.id.substring(0,item.id.length - 5)).show();
    } else {
      $("#" + item.id.substring(0,item.id.length - 5)).hide();
    }     
  });
}); 

// Shows(Opens) all the Info Box related objects for the provided site name
function openInfoBox(site){
  $("#" + site + "InfoBox").show();
  $("#" + site + "DateTime").show();
  $("#" + site + "ImageSource").show();
  $("#" + site + "InfoCloseButton").show();
  $("#" + site + "InfoButton").hide();
  $("#" + site + "InfoButtonBack").hide();
}

// Hides(Closes) all the Info Box related objects of the provided site name
function closeInfoBox(site){
  $("#" + site + "InfoBox").hide();
  $("#" + site + "DateTime").hide();
  $("#" + site + "ImageSource").hide();
  $("#" + site + "InfoCloseButton").hide();
  $("#" + site + "InfoButton").show();
  $("#" + site + "InfoButtonBack").show();
}

// Sets images source of images to original images read from the csv data file
function setOriginalImages() {
  $.ajax({
  url:"newsData.csv",
  cache:false,
  dataType:"text",
  success:function(data)
  {
    var array = data.split(/\r?\n|\r/);
    for (var i = 1; i <= newsSites.length; i++) {
      var cell_data = array[i].split(",");
      if(i == 3 || i == 6){
        document.getElementById(newsSites[i-1]+"Image").src = 'images/'+ newsSites[i-1]+ 'Keyword.jpg' + '?' + Date.now();
        document.getElementById(newsSites[i-1]+'ImageSource').href = cell_data[7];
      } else {
        document.getElementById(newsSites[i-1]+"Image").src = 'images/'+ newsSites[i-1]+ 'Original.jpg' + '?' + Date.now();
        document.getElementById(newsSites[i-1]+'ImageSource').href = cell_data[4];       
      }
    } 
  }});   
}

// Sets images source of images to keyword images read from the csv data file
function setKeywordImages(){
  $.ajax({
  url:"newsData.csv",
  cache:false,
  dataType:"text",
  success:function(data)
  {  
    var array = data.split(/\r?\n|\r/);
    for (var i = 1; i <= newsSites.length; i++) {
      var cell_data = array[i].split(",");
      document.getElementById(newsSites[i-1]+"Image").src = 'images/'+ newsSites[i-1]+ 'Keyword.jpg' + '?' + Date.now();
      document.getElementById(newsSites[i-1]+'ImageSource').href = cell_data[7];
    }
  }});      
}