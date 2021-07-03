let hidden_image_class = 'blog-images__item_hidden',
    active_dot_class = 'active-dot';

function makeHidden (item, dot_button) {
    // Cделать фотографию видимой
    item.classList.add(`${hidden_image_class}`)
    dot_button.classList.remove(`${active_dot_class}`)
}

function makeVisible (item, dot_button) {
    // Сделать фотографию невидимой
    item.classList.remove(`${hidden_image_class}`)
    dot_button.classList.add(`${active_dot_class}`)
}

function showNextImage(item_list, dot_buttons){
    // Показать следующее изображение
    for (let i = 0; i < item_list.length; ++i) {
        let item = item_list[i];

        if (!item.classList.contains(`${hidden_image_class}`)) {
            makeHidden(item, dot_buttons[i])
            if (i < item_list.length - 1) {
                let index = i + 1;
                makeVisible(item_list[index], dot_buttons[index])
            } else {
                let index = 0;
                makeVisible(item_list[index],dot_buttons[index])
            }
        break
        }
    }
}

function showPrevImage(item_list, dot_buttons) {
    // Показать предыдущее изображение
    for (let i = 0; i < item_list.length; ++i) {
        let item = item_list[i];

        if (!item.classList.contains(`${hidden_image_class}`)) {
            makeHidden(item, dot_buttons[i])
            if (i > 0) {
                let index = i - 1;
                makeVisible(item_list[index], dot_buttons[index])
            } else {
                let index = item_list.length - 1;
                makeVisible(item_list[index], dot_buttons[index])
            }
        break
        }
    }
}

function setStartValues(buttons, images) {
    // Установить стартовые значения классов для элементов карусели изображений
    buttons[0].classList.add(`${active_dot_class}`)
    images.forEach(function (item) {
        item.classList.add(`${hidden_image_class}`)
    })
}

document.addEventListener("DOMContentLoaded", function () {
    let hidden_image_items = document.querySelectorAll('div.blog-images__item:not(:first-child)'),
        all_images = document.querySelectorAll('div.blog-images__item'),
        button_next = document.querySelector("span.blog-images__button_next"),
        button_prev = document.querySelector("span.blog-images__button_prev"),
        dot_buttons_class = 'dot-buttons-box__button';

    let blog_images = document.querySelector("div.blog-images"),
        dot_buttons_box = document.createElement('div');

    dot_buttons_box.className = "dot-buttons-box"
    blog_images.after(dot_buttons_box)

    for (let i = 0; i < all_images.length; ++i) {
        let dot_button = document.createElement('div');

        dot_button.className = dot_buttons_class
        dot_buttons_box.append(dot_button)
        dot_button.addEventListener('click', function () {
            // Сделать фотографию видимой по нажатии на кнопку
            for (let i = 0; i < all_images.length; ++i) {
                let image = all_images[i]
                if (!image.classList.contains(`${hidden_image_class}`)) {
                    makeHidden(all_images[i], dot_buttons[i])
                }
            }
            makeVisible(all_images[i], dot_button)
        })
    }

    let dot_buttons = document.querySelectorAll(`div.${dot_buttons_class}`);

    setStartValues(dot_buttons, hidden_image_items)

    button_next.addEventListener('click', function() { showNextImage(all_images, dot_buttons) })
    button_prev.addEventListener('click', function() { showPrevImage(all_images, dot_buttons) })
})