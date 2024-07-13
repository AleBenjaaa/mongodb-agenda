var contactoModal = document.getElementById('contactoModal');
    contactoModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget; // Botón que activó el modal
        var nombre = button.getAttribute('data-nombre');
        var edad = button.getAttribute('data-edad');
        var categoria = button.getAttribute('data-categoria');
        var telefono = button.getAttribute('data-telefono');
        var direccion = button.getAttribute('data-direccion');
        var favorito = button.getAttribute('data-favorito');

        document.getElementById('modalNombre').textContent = nombre;
        document.getElementById('modalEdad').textContent = edad;
        document.getElementById('modalCategoria').textContent = categoria;
        document.getElementById('modalTelefono').textContent = telefono;
        document.getElementById('modalDireccion').textContent = direccion;
        document.getElementById('modalFavorito').textContent = favorito;
    });