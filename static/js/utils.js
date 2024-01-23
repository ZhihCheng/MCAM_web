function setDisplay(elements, displayStyle) {
    elements.forEach(element => {
        document.getElementById(element).style.display = displayStyle;
    });
}
