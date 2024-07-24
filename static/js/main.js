let cart = [];

function login() {
  const customerId = document.getElementById("customer-id").value;

  axios
    .post("/login", { customer_id: customerId })
    .then(function (response) {
      if (response.data.success) {
        document.getElementById("login-form").style.display = "none";
        document.getElementById("shopping-window").style.display = "block";
        location.reload();
      } else {
        document.getElementById("result").innerHTML =
          "Error: " + response.data.error;
      }
    })
    .catch(function (error) {
      document.getElementById("result").innerHTML =
        "Error: " + error.response.data.error;
    });
}

function logout() {
  axios
    .get("/logout")
    .then(function (response) {
      if (response.data.success) {
        location.reload();
      }
    })
    .catch(function (error) {
      document.getElementById("result").innerHTML =
        "Error: " + error.response.data.error;
    });
}

function addToCart(productId) {
  document.getElementById("result").innerHTML = ""; // Clear the checkout success message
  if (!cart.includes(productId)) {
    cart.push(productId);
    console.log("Added product to cart: " + productId);
    updateCartDisplay();
  } else {
    console.log("Product already in cart: " + productId);
  }
}

function updateCartDisplay() {
  const cartItems = document.getElementById("cart-items");
  cartItems.innerHTML = ""; // Clear existing cart items
  cart.forEach((productId) => {
    const li = document.createElement("li");
    li.textContent = `Product ID: ${productId}`;
    cartItems.appendChild(li);
  });
}

function getProductIdsFromCart() {
  return cart;
}

function checkout() {
  const productIds = getProductIdsFromCart();
  axios
    .post("/checkout", { product_ids: productIds })
    .then((response) => {
      if (
        response.data.invalid_products &&
        response.data.invalid_products.length > 0
      ) {
        displayInvalidProducts(response.data.invalid_products);
      }
      if (
        response.data.products_missing_category &&
        response.data.products_missing_category.length > 0
      ) {
        displayMissingCategoryProducts(response.data.products_missing_category);
      }
      if (
        response.data.point_earning_rules_missing &&
        response.data.point_earning_rules_missing.length > 0
      ) {
        displayMissingPointEarningRules(
          response.data.point_earning_rules_missing
        );
      }
      document.getElementById(
        "result"
      ).innerHTML = `Checkout successful! You earned ${response.data.total_points_earned} points.`;
      cart = []; // Clear the cart after successful checkout
      updateCartDisplay(); // Update the cart display
    })
    .catch((error) => {
      document.getElementById(
        "result"
      ).innerHTML = `Error: ${error.response.data.error}`;
    });
}

function displayInvalidProducts(invalidProducts) {
  const errorMessagesDiv = document.getElementById("error-messages");
  errorMessagesDiv.innerHTML =
    "<h3>Warning: Some products could not be processed</h3>";
  const ul = document.createElement("ul");
  invalidProducts.forEach((productId) => {
    const li = document.createElement("li");
    li.textContent = `Product ID ${productId} is invalid or not available.`;
    ul.appendChild(li);
  });
  errorMessagesDiv.appendChild(ul);
}

function displayMissingCategoryProducts(missingCategoryProducts) {
  const errorMessagesDiv = document.getElementById("error-messages");
  errorMessagesDiv.innerHTML +=
    "<h3>Warning: Some products are missing categories</h3>";
  const ul = document.createElement("ul");
  missingCategoryProducts.forEach((productId) => {
    const li = document.createElement("li");
    li.textContent = `Product ID ${productId} has no category defined.`;
    ul.appendChild(li);
  });
  errorMessagesDiv.appendChild(ul);
}

function displayMissingPointEarningRules(missingPointEarningRules) {
  const errorMessagesDiv = document.getElementById("error-messages");
  errorMessagesDiv.innerHTML +=
    "<h3>Warning: Some products are missing point earning rules</h3>";
  const ul = document.createElement("ul");
  missingPointEarningRules.forEach((productId) => {
    const li = document.createElement("li");
    li.textContent = `Product ID ${productId} has no point earning rules defined.`;
    ul.appendChild(li);
  });
  errorMessagesDiv.appendChild(ul);
}
