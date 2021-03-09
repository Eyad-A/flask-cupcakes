const BASE_URL = "http://127.0.0.1:5000/api";


/** Generate HTML about a specific cupcake */
function generateHTML(cupcake) {
    return `
        <div data-cupcake-id=${cupcake.id}>
            <li>
                ${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating}
                <button class="delete-button">X</button>
            </li>
            <img class="cupcake-img" src="${cupcake.image}">
        </div>
    `;
}


/** List all the cupcakes on the page */

async function showCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cupcakeData of response.data.cupcakes) {
        let newCupcake = $(generateHTML(cupcakeData));
        $("#cupcakes-list").append(newCupcake);
    }
}


/** Handle form submission for adding new cupcakes */

$("#new-cupcake-form").on("submit", async function(evt) {
    evt.preventDefault();

    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image 
    });

    let newCupcake = $(generateHTML(newCupcakeResponse.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");

    console.log(newCupcakeResponse);
});


/** Handle deleting a cupcake */

$("#cupcakes-list").on("click", ".delete-button", async function(evt) {
    evt.preventDefault();
    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");
    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});

$(showCupcakes);