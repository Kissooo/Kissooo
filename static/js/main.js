const modal = document.getElementById('addModal');
const form = document.getElementById('itemForm');
const modalTitle = document.getElementById('modalTitle');

// This function is now for the "Add Item" button
function openAddModal() {
    // Reset form for adding
    form.reset();
    form.action = '/add'; // The action for the form
    modalTitle.innerText = 'เพิ่มครุภัณฑ์ใหม่';
    modal.classList.remove('hidden');
}

function openEditModal(id, name, code, purchaseDate, price, status) {
    form.reset();
    // Populate form for editing
    form.action = `/update/${id}`; // The action for the form, specific to the item
    modalTitle.innerText = 'แก้ไขข้อมูลครุภัณฑ์';

    document.getElementById('name').value = name;
    document.getElementById('code').value = code;
    document.getElementById('purchase_date').value = purchaseDate;
    document.getElementById('price').value = price;
    document.getElementById('status').value = status;

    modal.classList.remove('hidden');
}

function closeModal() {
    modal.classList.add('hidden');
}

// Close modal if clicking outside of it
window.onclick = function(event) {
    // Check if the modal element itself is the target of the click
    if (event.target == modal) {
        closeModal();
    }
}

// Note: The original HTML had an `onclick="openModal('addModal')"`
// I have renamed openModal to openAddModal for clarity.
// The button in the HTML will need to be updated to call `openAddModal()`.
// The edit buttons will continue to call `openEditModal(...)` as before.
// The cancel buttons will call `closeModal()` as before.
// I will also need to add event listeners if I want to get rid of onclick attributes completely,
// but for now, this is a direct translation of the logic.
