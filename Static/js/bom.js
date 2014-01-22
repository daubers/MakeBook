function newBoMPost() {
    var url = '/BoM/New/';
    var form = $('<form action="' + url + '" method="post">' +
        '<input type="text" name="projid" value="' + Return_URL + '" />' +
        '</form>');
    $('body').append(form);
    $(form).submit();
}