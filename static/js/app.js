document.addEventListener('DOMContentLoaded', function () {
    let listProductHTML = document.querySelector('.listProduct');
    let listCartHTML = document.querySelector('.listCart');
    let iconCart = document.querySelector('.icon-cart');
    let iconCartSpan = document.querySelector('.icon-cart span');
    let body = document.querySelector('body');
    let closeCart = document.querySelector('.close');
    let products = [];
    let cart = [];
    const closeButton = document.querySelector('.close');

    document.querySelector('.close').addEventListener('click', () => {
        body.classList.toggle('showCart');
    });
    document.body.addEventListener('click', function (event) {
        if (event.target.classList.contains('close')) {
            console.log('Close button clicked');
            body.classList.toggle('showCart');
        }
    });

    
    if (closeButton) {
        // Attach the click event listener to the close button
        closeButton.addEventListener('click', function () {
            console.log('Close button clicked'); // Log to check if the click event is triggered
            body.classList.toggle('showCart');
        });
    } else {
        console.error('Close button not found'); // Log an error if the close button is not found
    }

   
    document.querySelector('.paybtn').addEventListener('click', () => {
        console.log('Checkout button clicked');
        let am_paise = Math.round(calculateTotal() * 100);
        console.log('Total Amount in paise:', am_paise);
        initiateRazorpay(am_paise);
    });
    

    const calculateTotal = () => {
        let totalPrice = 0;
    
        cart.forEach(item => {
            let product = products[item.product_id];
            if (product) {
                totalPrice += product.price * item.quantity;
            }
        });
    
        // Display the total price in the cart tab with the Rupees symbol (₹)
        document.getElementById('cartTotalPrice').innerText = `₹${totalPrice.toFixed(2)}`;
    
        // Check if the checkout button exists before adding the event listener
        let checkoutBtn = document.querySelector('.checkoutBtn');
        if (checkoutBtn) {
            checkoutBtn.addEventListener('click', () => {
                let am_paise = Math.round(totalPrice * 100);
                initiateRazorpay(am_paise);
            });
        }
    
        return totalPrice; 
    };
    
    
    

    document.querySelector('.calculateTotal').addEventListener('click', calculateTotal);
    

    iconCart.addEventListener('click', () => {
        body.classList.toggle('showCart');
    });

    closeCart.addEventListener('click', () => {
        body.classList.toggle('showCart');
    });

  
const displayProductDetails = (product) => {
    const productDetailsPopup = document.getElementById('productDetailsPopup');
    productDetailsPopup.innerHTML = `
        <img src="${product.img}" alt="${product.name}">
        <h2>${product.name}</h2>
        <p>${product.desc}</p>
        <div class="price">₹${product.price}</div>
        <button class="addCart">Add To Cart</button>
    `;

    const modal = document.getElementById('productModal');
    modal.style.display = 'block';
};

// Close the modal when the close button or outside the modal is clicked
const closeModal = () => {
    const modal = document.getElementById('productModal');
    modal.style.display = 'none';
};

// Attach event listener to the close button
document.querySelector('.close').addEventListener('click', closeModal);

// Attach event listener to close the modal when clicking outside of it
window.addEventListener('click', (event) => {
    const modal = document.getElementById('productModal');
    if (event.target === modal) {
        closeModal();
    }
});

// Modify the addDataToHTML function to handle nested product structure
const addDataToHTML = () => {
    if (products && typeof products === 'object') {
        Object.keys(products).forEach(key => {
            const product = products[key];
            let newProduct = document.createElement('div');
            newProduct.dataset.id = key; // Use the key as the product id
            newProduct.classList.add('item');
            newProduct.innerHTML = `
                <img src="${product.img}" alt="">
                <h2>${product.name}</h2>
                <div class="price">₹${product.price}</div>
                <button class="addCart">Add To Cart</button>`;
            listProductHTML.appendChild(newProduct);

            // Add event listener to each Add To Cart button
            newProduct.querySelector('.addCart').addEventListener('click', () => {
                addToCart(key); // Pass the key as the product id
            });

            // Add event listener to display product details
            newProduct.addEventListener('click', () => {
                displayProductDetails(product);
            });
        });
    }
};

// Modify the addToCart function to use the product_id directly
const addToCart = (product_id) => {
    let positionThisProductInCart = cart.findIndex((value) => value.product_id === product_id);
    if (cart.length <= 0) {
        cart = [{
            product_id: product_id,
            quantity: 1
        }];
    } else if (positionThisProductInCart < 0) {
        cart.push({
            product_id: product_id,
            quantity: 1
        });
    } else {
        cart[positionThisProductInCart].quantity = cart[positionThisProductInCart].quantity + 1;
    }
    addCartToHTML();
    addCartToMemory();
    calculateTotal(); // Recalculate total after adding an item
};




    let rzp;

  

    const initiateRazorpay = (amount) => {
        var options = {
            key: 'rzp_test_knV2MvCOmcINdw', // Replace with your actual Razorpay API key
            amount: amount, // Amount in paise
            currency: 'INR',
            name: 'Clothify inc.',
            description: 'Purchase Description',
            image: '', // Replace with your company logo URL
            handler: function (response) {
                alert('Payment successful! Payment ID: ' + response.razorpay_payment_id);
            },
            prefill: {
                name: 'clotthify inc.',
                email: 'dpshah1232@gmail.com',
                contact: '6352972571'
            },
            notes: {
                address: 'Razorpay Corporate Office'
            },
            theme: {
                color: '#4CAF50'
            }
        };
    
        rzp = new Razorpay(options);

        rzp.on('payment.failed', function (response) {
            console.error('Payment failed:', response.error.code, response.error.description);
        });
    
        rzp.open();

        
    };
    
    const addCartToMemory = () => {
        localStorage.setItem('cart', JSON.stringify(cart));
    };

    const addCartToHTML = () => {
        listCartHTML.innerHTML = '';
        let totalQuantity = 0;
    
        if (cart.length > 0) {
            cart.forEach(item => {
                totalQuantity += item.quantity;
    
                let product = products[item.product_id];
    
                let newItem = document.createElement('div');
                newItem.classList.add('item');
                newItem.dataset.id = item.product_id;
    
                listCartHTML.appendChild(newItem);
                newItem.innerHTML = `
                    <div class="image">
                        <img src="${product.img}" alt="${product.name}">
                    </div>
                    <div class="name">
                        ${product.name}
                    </div>
                    <div class="totalPrice">₹${product.price * item.quantity}</div>
                    <div class="quantity">
                        <span class="minus"><</span>
                        <span>${item.quantity}</span>
                        <span class="plus">></span>
                    </div>
                `;
            });
        }
    
        iconCartSpan.innerText = totalQuantity;
    };
    
    listCartHTML.addEventListener('click', (event) => {
        let positionClick = event.target;
        if (positionClick.classList.contains('minus') || positionClick.classList.contains('plus')) {
            let product_id = positionClick.parentElement.parentElement.dataset.id;
            let type = 'minus';
            if (positionClick.classList.contains('plus')) {
                type = 'plus';
            }
            changeQuantityCart(product_id, type);
        }
    });
    

    const changeQuantityCart = (product_id, type) => {
        let positionItemInCart = cart.findIndex((value) => value.product_id == product_id);
        if (positionItemInCart >= 0) {
            switch (type) {
                case 'plus':
                    cart[positionItemInCart].quantity = cart[positionItemInCart].quantity + 1;
                    break;
                default:
                    let changeQuantity = cart[positionItemInCart].quantity - 1;
                    if (changeQuantity > 0) {
                        cart[positionItemInCart].quantity = changeQuantity;
                    } else {
                        cart.splice(positionItemInCart, 1);
                    }
                    break;
            }
        }
        addCartToHTML();
        addCartToMemory();
        calculateTotal(); // Recalculate total after changing quantity
    };

    const initApp = () => {
        // get data product
        fetch('/jsonfile')
            .then(response => response.json())
            .then(data => {
                console.log(data);  
                products = data;
                addDataToHTML();

                // get data cart from memory
                if (localStorage.getItem('cart')) {
                    cart = JSON.parse(localStorage.getItem('cart'));
                    addCartToHTML();
                    calculateTotal(); // Initial total calculation
                }
            });
    };
    
    
    initApp();
});
