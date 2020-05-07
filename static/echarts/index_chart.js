$(function() {
  /* ChartJS
   * -------
   * index html charts
   */
    $.ajax({
    url:"/data_detail",
    data:{id:id},
    type:"get",
    dataType:"json",
    success:function (data) {
      f(data.labels,data.data);
    }
  });

});