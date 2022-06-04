function activarInput(){
    document.getElementById("select_periodo").disabled = false;
    
}
function desactivarInput(){
    document.getElementById("select_periodo").disabled = true;
}
function validacion_pagos(){
    let nombre = document.getElementById("nombre_operacion").value 
    
    if (nombre != ""){
        var mensaje = confirm("Seguro que quieres salir del registro")
        if (mensaje){
            return null
        }
        else{
            return null
        }
    }
    else{
        null
    }
}
/*function validacion_gastos(){

}*/
function verFecha(){
    date = new Date();
    year = date.getFullYear();
    month = date.getMonth() + 1;
    day = date.getDate();
    return day + "/" + month + "/" + year;

}
console.log(verFecha());
