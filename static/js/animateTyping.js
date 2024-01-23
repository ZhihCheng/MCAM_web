function animateTyping(elementId, cursorId, text, displayElementId, callback) {
    const textElement = document.querySelector(`#${elementId}`);
    const finalCursor = document.querySelector(`#${cursorId}`);
    const displayElement = displayElementId ? document.querySelector(`#${displayElementId}`) : null;
    const textArray = text.split('');

    finalCursor.style.display = 'inline-block';
    textElement.innerHTML = '';

    textArray.forEach((char, index) => {
        setTimeout(() => {
            textElement.innerHTML += char;
            if (index === textArray.length - 1) {
                finalCursor.style.display = 'none';
                if (displayElement) {
                    displayElement.style.display = 'block';
                }
                if (callback && typeof callback === 'function') {
                    callback();
                }
            }
        }, index * 50);
    });
}

function windows_under(){
    window.scrollTo(0, document.body.scrollHeight);
}