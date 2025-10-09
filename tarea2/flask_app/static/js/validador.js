

const validarForm = () => {
    let msg = "";

    const validadorRegion = (region) => region !=='';
    const validadorComuna = (comuna) => comuna !=='';
    const validadorSector = (sector) => sector.length <= 100;
    const validadorNombre = (nombre) => nombre && nombre.length <= 200;
    const validadorEmail = (email) => {
      const regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
      return regex.test(email) && email.length <= 100 && email;
    };
    const validadorTelefono = (telefono) => {
      const regex = /^\+\d{3}\.\d{8}$/;
      return regex.test(telefono) || telefono == '';
    };
    const validadorRedSocial = (url) => url.length >= 4 && url.length <= 50;
    const validadorTipo = (tipo) => tipo && tipo !=='';
    const validadorCantidad = (cantidad) => cantidad && cantidad >= 1;
    const validadorEdad = (edad) => edad && edad >= 1;
    const validadorMedida = (medida) => medida && medida !=='';
    const validadorFecha = (fechaMinima, fechaIngresada) => {
      const minimo = new Date(fechaMinima); 
      const ingresada = new Date(fechaIngresada); 
        
      return ingresada >= minimo; 
    };
    const validadorFoto = (foto) => foto;


    const regionInput = document.getElementById("region");
    const comunaInput = document.getElementById("comuna");
    const sectorInput = document.getElementById("sector");
    const nombreInput = document.getElementById("nombre");
    const emailInput = document.getElementById("email");
    const telefonoInput = document.getElementById("telefono");

    const contactosDiv = document.getElementById('contactos');
    const inputsContactos  = contactosDiv.querySelectorAll('input');
    
    const radiosTipo = document.querySelectorAll('input[name="tipo"]');
    let tipoSeleccionado = "";

    radiosTipo.forEach(r => {
      if (r.checked) {
        tipoSeleccionado = r.value;
      }
    });

    const cantidadInput = document.getElementById("cantidad");
    const edadInput = document.getElementById("edad");

    const radiosUnidad = document.querySelectorAll('input[name="unidad"]');
    let unidadSeleccionado = "";

    radiosUnidad.forEach(r => {
      if (r.checked) {
        unidadSeleccionado = r.value;
      }
    });

    const fechaInput = document.getElementById("fecha_entrega")
    const fechaDefault = document.getElementById("fecha_entrega_default")
    const fotoInput = document.getElementById("foto")

    let isValid = false;

    if(!validadorRegion(regionInput.value)) {
      msg += "Falta region\n";
      regionInput.style.borderColor = "red"; 
    } else {
      regionInput.style.borderColor = "";
    }
    if(!validadorComuna(comunaInput.value)) {
      msg += "Falta comuna\n";
      comunaInput.style.borderColor = "red"; 
    } else {
      comunaInput.style.borderColor = "";
    }
    if(!validadorSector(sectorInput.value)) {
      msg += "Sector invalido\n";
      sectorInput.style.borderColor = "red"; 
    } else {
      sectorInput.style.borderColor = "";
    }
    if(!validadorNombre(nombreInput.value)) {
      msg += "nombre invalido\n";
      nombreInput.style.borderColor = "red"; 
    } else {
      nombreInput.style.borderColor = "";
    }
    if(!validadorEmail(emailInput.value)) {
      msg += "email invalido\n";
      emailInput.style.borderColor = "red"; 
    } else {
      emailInput.style.borderColor = "";
    }
    if(!validadorTelefono(telefonoInput.value)) {
      msg += "telefono invalido\n";
      telefonoInput.style.borderColor = "red"; 
    } else {
      telefonoInput.style.borderColor = "";
    }

    inputsContactos.forEach((input, i) => {
      const valor = input.value.trim();

      if(valor !== "" && !validadorRedSocial(valor)) {
        msg += `Medio de contacto ${i + 1} inválido\n`;
        input.style.borderColor = "red";
      } else {
        input.style.borderColor = "";
      }
    });

    if(!validadorTipo(tipoSeleccionado)) {
      msg += "Seleccione al menos un tipo (Perro o Gato)\n";

      radiosTipo.forEach(r => r.parentElement.style.color = "red");
    } else {
      radiosTipo.forEach(r => r.parentElement.style.color = "");
    }

    if (!validadorCantidad(cantidadInput.value)) {
      msg += 'Cantidad invalida\n'
      cantidadInput.style.borderColor = "red"; 
    } else {
      cantidadInput.style.borderColor = ""; 
    }
    if (!validadorEdad(edadInput.value)) {
      msg += 'edad invalida\n'
      edadInput.style.borderColor = "red"; 
    } else {
      edadInput.style.borderColor = ""; 
    }

    if(!validadorMedida(unidadSeleccionado)) {
      msg += "Seleccione al menos una unidad de medida (meses o años)\n";

      radiosUnidad.forEach(r => r.parentElement.style.color = "red");
    } else {
      radiosUnidad.forEach(r => r.parentElement.style.color = "");
    }
    if(!validadorFecha(fechaDefault.value,fechaInput.value)){
      msg += `Fecha minima ${fechaInput.defaultValue}\n`;
      fechaInput.style.borderColor = "red"; 
    } else {
      fechaInput.style.borderColor = "";
    }

    if (!validadorFoto(fotoInput.value)){
      msg += "selecciona por lo menos una foto\n";
      fotoInput.style.border = "2px solid red";
    } else {
      fotoInput.style.borderColor = "";
    }

    if(msg == "") {
      isValid = true;
    } else {
      alert(msg);
    }

    return isValid;

}

const enviarFormulario = () => {
    if(True){//validarForm()) {
        const confirmacion = confirm("¿Está seguro que desea agregar este aviso de adopción?");
        if(confirmacion) {
          document.querySelector("form").submit();
        } 
    }
}

const agregarAviso = document.getElementById("agregar_aviso");

agregarAviso.addEventListener("click",enviarFormulario)
