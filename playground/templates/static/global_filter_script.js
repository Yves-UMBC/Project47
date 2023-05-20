$(function() {
    $(".chozen-select").chosen();
});

$('.chosen-toggle').each(function(index) {
    $(this).on('click', function(){
        $(this).parent().find('option').prop('selected', $(this).hasClass('select')).parent().trigger('chosen:updated');
    });
});