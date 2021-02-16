// Read the csv data file and fills titles and links
$.ajax({
url:"newsData.csv",
cache:false,
dataType:"text",
success:function(data)
{  
  var array = data.split(/\r?\n|\r/);
  var newsSites = ["nyTimes","yahoo","nbc","cbs","fox","cnbc"];
  for (var i = 1; i < 7; i++) {
    var cell_data = array[i].split(",");
    $('#'+ newsSites[i-1]+ 'Name').html(cell_data[0]); 
    $('#'+ newsSites[i-1]+ 'title').html(cell_data[1]);
    document.getElementById(newsSites[i-1]+ "LinkId").href = cell_data[3];
    document.getElementById(newsSites[i-1]+ "ImagesLinkId").href = cell_data[3];
    $('#'+ newsSites[i-1]+ 'DateTime').html('Date and Time of Scan' + "<br>" + cell_data[2]);    
  }
  $('#footerDateTime').html(array[7].split(",")[1]);
}
});