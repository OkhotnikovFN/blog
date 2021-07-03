// Предпросмотр фотографии профиля
document.addEventListener("DOMContentLoaded", function () {
    let load_photo_field = document.querySelector('[id="id_user_photo"]'),
        img_field = document.querySelector('img.update-user-photo-image'),
        img_field_first_value = img_field.getAttribute('src'),

        image_delete_style = 'delete-uploaded-image';

    load_photo_field.addEventListener("change", function () {
        if (this.files && this.files[0]) {
            let fr = new FileReader(),
                photo_box = document.querySelector('div .update-user-photo-container'),
                input = this,
                image_delete = document.createElement('span');

            let removeImage = function (e) {
                // Удаление выбранной фотографии из формы
                let dt = new DataTransfer(),
                    delete_button = e.target,
                    change_event = new Event('change');

                input.files = dt.files
                input.dispatchEvent(change_event)
                delete_button.remove()
            }

            image_delete.className = image_delete_style
            photo_box.append(image_delete)
            image_delete.addEventListener("click", removeImage)

            fr.addEventListener("load", function () {
                img_field.setAttribute('src', fr.result)
            }, false);

            fr.readAsDataURL(this.files[0]);
        } else {
            img_field.setAttribute('src', img_field_first_value)
        }
    });
})
