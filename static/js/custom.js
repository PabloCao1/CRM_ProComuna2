$(function () {
	//Initialize Select2 Elements
	$('.select2').select2()

	//Initialize Select2 Elements
	$('.select2bs4').select2({
	  theme: 'bootstrap4'
	})
  });

$(".clickable-row").click(function() {
	// se agrrega la clase en filas <tr> de un table para que sean links a la vista de detalle del elemento
    window.location = $(this).data("href");
    });

setTimeout(function () {
	// desaparecer los Success messages
$(".alert").alert('close');
}, 3000);

$(".print").click(function () {
    //imprime los div excepto los elementos que tengan la clase 'd-print-none'
    window.print();
});

(function () {
	// Control de formularios invalidos.
	"use strict";
	window.addEventListener(
		"load",
		function () {
			// Get the forms we want to add validation styles to
			var forms = document.getElementsByClassName("needs-validation");
			// Loop over them and prevent submission
			var validation = Array.prototype.filter.call(forms, function (form) {
				form.addEventListener(
					"submit",
					function (event) {
						if (form.checkValidity() === false) {
							event.preventDefault();
							event.stopPropagation();
						}
						form.classList.add("was-validated");
					},
					false
				);
			});
		},
		false
	);
})();
