$(document).ready(function() {
    $('.box-item').draggable({
      cursor: 'move',
      helper: "clone"
    });
  
    $("#container1").droppable({
      drop: function(event, ui) {
        var itemid = $(event.originalEvent.toElement).attr("itemid");
        $('.box-item').each(function() {
          if ($(this).attr("itemid") === itemid) {
            $(this).appendTo("#container1");
          }
        });
      }
    });
  
    $("#container2").droppable({
      drop: function(event, ui) {
        var itemid = $(event.originalEvent.toElement).attr("itemid");
        $('.box-item').each(function() {
          if ($(this).attr("itemid") === itemid) {
            $(this).appendTo("#container2");
          }
        });
      }
    });
  
    $("#container3").droppable({
      drop: function(event, ui) {
        var itemid = $(event.originalEvent.toElement).attr("itemid");
        $('.box-item').each(function() {
          if ($(this).attr("itemid") === itemid) {
            $(this).appendTo("#container3");
          }
        });
      }
    });
  
  });
  
  $(document).ready(function() {
    $("#submit-teams").click(function() {
  
      var friendly = document.getElementById("container2").querySelectorAll(".hero-item");
      var enemy = document.getElementById("container3").querySelectorAll(".hero-item");
  
      if (friendly.length==5 && enemy.length==5) {
        var r_1 = friendly[0].getAttribute('itemid');
        var r_2 = friendly[1].getAttribute('itemid');
        var r_3 = friendly[2].getAttribute('itemid');
        var r_4 = friendly[3].getAttribute('itemid');
        var r_5 = friendly[4].getAttribute('itemid');
        var d_1 = enemy[0].getAttribute('itemid');
        var d_2 = enemy[1].getAttribute('itemid');
        var d_3 = enemy[2].getAttribute('itemid');
        var d_4 = enemy[3].getAttribute('itemid');
        var d_5 = enemy[4].getAttribute('itemid');
       
        $.ajax({
          url: '/model/stacked/' + r_1 + '/' + r_2 + '/' + r_3 + '/' + r_4 + '/' + r_5 + '/' + d_1 + '/' + d_2 + '/' + d_3 + '/' + d_4 + '/' + d_5 + '/team',
          type: 'GET',
          contentType: 'json',
          success:function(response) {
            if (response.r_wins == true){
              $('#outcome').html("Hero team");
            }
            else {
              $('#outcome').html("Enemy team");
            }
          }
        });
      }
      else {
        alert("Each team must have 5 heroes added!!")
      }
    }); 
  });
  