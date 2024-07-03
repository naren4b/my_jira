$(document).ready(function() {
    // Function to enable sorting for all sortable tables
    function enableTableSorting() {
        $('table.table-sortable').each(function() {
            var $table = $(this);
            $('th', $table).each(function(column) {
                var $header = $(this);
                $header.on('click', function() {
                    var rows = $table.find('tbody > tr').get();
                    rows.sort(function(rowA, rowB) {
                        var keyA = $(rowA).children('td').eq(column).text();
                        var keyB = $(rowB).children('td').eq(column).text();
                        if ($.isNumeric(keyA) && $.isNumeric(keyB)) {
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
    }

    // Call the function initially
    enableTableSorting();

    // Additional code to handle dynamic loading of tables or tabs
    $(document).on('shown.bs.tab', 'a[data-toggle="tab"]', function (e) {
        var targetTab = $(e.target).attr("href"); // activated tab
        if (targetTab === '#report_a' || targetTab === '#report_b' || targetTab === '#report_c' || targetTab === '#report_d' || targetTab === '#report_e') {
            enableTableSorting();
        }
    });
});
