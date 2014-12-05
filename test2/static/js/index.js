$('doucment').ready(function(){
  $('.question').on('click', '.replyBtn', function(event){
    var $replyBtn = $(event.target);
    $replyBtn.next().toggle(function(){
      if ($replyBtn.text() === '回复TA') {
        $replyBtn.text('收起回复')
      } else {
        $replyBtn.text('回复TA')
      }
    });
  });
  $('.replyForm').on('submit', function(event){
    event.preventDefault();
    var $agrs = $(this).serialize();
    $.post('/reply', $agrs, function(data){
      var $replyForm = $(event.target);
      $replyForm.parent().parent().append(data);
      $replyForm.parent().prev().click()
      $replyForm[0].reset();
    })
  })
});

