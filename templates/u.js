
let opr = {
	searching: false,
	lengthMenu: [[50, 100, 150, 200], [50, 100, 150, 200]],
	paging: true,
	scrollY: 500
	// ordering:  false
};
// $('.display').DataTable(opr);
function make_tds(data, id) {
	//---
	var r = $('#' + id).DataTable(opr);
	//---
	var numb = 0;
	//---
	$.each(data, function(index, va){
		if (index != 'test') {
			if (id == 'users') {
				numb += 1;
                r.row.add([index, va.count]).draw(false)
			} else {
				numb += va.count;
                var ind = index.replace(/-/g, '');
                r.row.add([index, va.count]).attr('data-sort', index).draw(false);
			}
		};
	});
	//---
	if (id == 'users') {
		$('#users-all').text(numb);
	} else {
		$('#downloads-all').text(numb);
	}
	//---
};

$(document).ready( function () {
	fetch('/users')
		.then(response => response.json())
		.then(data => make_tds(data, 'users'));

	fetch('/dates')
	.then(response => response.json())
		.then(data => make_tds(data, 'dates'));
	} );