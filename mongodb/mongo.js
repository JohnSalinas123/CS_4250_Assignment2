db = connect( 'localhost:27017' );



printjson( db.document.find({}) )