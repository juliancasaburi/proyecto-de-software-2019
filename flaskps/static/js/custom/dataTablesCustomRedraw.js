function customRedraw(tableToRedraw) {
    var info = tableToRedraw.page.info();
 
    if (info.page > 0) {
        // when we are in the second page or above
        if (info.recordsDisplay > info.page*info.length) {
            // after removing 1 from the total, there are still more elements
            // than the previous page capacity 
            tableToRedraw.draw( false )
        } else {
            // there are less elements, so we navigate to the previous page
            tableToRedraw.page( 'previous' ).draw( 'page' )
        }
    }
}