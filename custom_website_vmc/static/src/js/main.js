lista1 = document.getElementsByName("p1");
lista2 = document.getElementsByName("p2");
lista3 = document.getElementsByName("porcent");

for (var x = 0; x < lista1.length; x++) {
    let v1 = parseFloat(lista1[x].innerHTML);
    let v2 = parseFloat(lista2[x].innerHTML);
    let calc = 100 - (Math.round(((v2 * 100 ) / v1)));
    if(calc == 0){
        document.getElementsByClassName("value_discount")[x].style.display ="none"
    }else{
        lista3[x].innerHTML = "-" + calc + "%"
    }
}