function getCupcakes() {
	axios
		.get("/api/cupcakes")
		.then(function (response) {
			const cupcakes = response.data.cupcakes;
			$("#cupcake-list").empty();
			cupcakes.forEach(function (cupcake) {
				$("#cupcake-list").append(
					`<li>${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating}</li>`
				);
			});
		})
		.catch(function (error) {
			console.error("Error fetching cupcakes:", error);
		});
}

getCupcakes();

$("#cupcake-form").submit(function (e) {
	e.preventDefault();
	const data = {
		flavor: $("#flavor").val(),
		size: $("#size").val(),
		rating: $("#rating").val(),
		image: $("#image").val(),
	};

	axios
		.post("/api/cupcakes", data)
		.then(function (response) {
			// Clear form fields after successful submission
			$("#flavor").val("");
			$("#size").val("");
			$("#rating").val("");
			$("#image").val("");

			getCupcakes();
		})
		.catch(function (error) {
			console.error("Error adding cupcake:", error);
		});
});
