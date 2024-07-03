$(document).ready(function() {
    $('table.table-sortable').each(function() {
        var $table = $(this);
        $('th', $table).each(function(column) {
            var $header = $(this);
            $header.on('click', function() {
                var rows = $table.find('tbody > tr').get();
                rows.sort(function(rowA, rowB) {
                    var keyA = $(rowA).children('td').eq(column).text();
                    var keyB = $(rowB).children('td').eq(column).text();
                    if($.isNumeric(keyA) && $.isNumeric(keyB)) {
                        return keyA - keyB;
                    } else {
                        return keyA.localeCompare(keyB);
                    }
                });
                $.each(rows, function(index, row) {
                    $table.children('tbody').append(row);
                });
            });
        });
    });
});
