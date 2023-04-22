function handleData()
{
    var form_data = new FormData(document.querySelector("form"));
    
    //si dentro de los selectores de form.form_data no esta el nombre lenguajes[]
    if(!form_data.has("lenguaje_prog[]"))
    {
        alert("debe seleccionar un lenguaje de programacion")
        return false;
    }
}