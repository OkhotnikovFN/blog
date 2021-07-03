// Предпросмотр фотографий для блога
document.addEventListener("DOMContentLoaded", function () {
    let load_photo_field = document.querySelector('[id="id_images"]');


    load_photo_field.addEventListener("change", function () {
        let image_style = 'upload-image',
            image_delete_style = 'delete-uploaded-image',
            image_box_style = 'upload-image-box',

            old_images = document.querySelectorAll(`.${image_box_style}`),
            input = this,
            images = this.files,
            image;

        let removeImage = function (index) {
            // Удаление выбранной фотографии из формы
            let dt = new DataTransfer(),
                change_event = new Event('change');

            for (let i = 0; i < images.length; i++) {
                image = images.item(i);
                if (i !== index)
                    dt.items.add(image)
            }
            input.files = dt.files
            input.dispatchEvent(change_event)
        }

        for (let old_image of old_images) {
            old_image.remove()
        }

        if (images) {
            for (let i = 0; i < images.length; i++) {
                image = images.item(i);

                let fr = new FileReader(),
                    image_box = document.createElement('div'),
                    image_field = document.createElement('img'),
                    image_delete = document.createElement('span');

                image_box.className = image_box_style
                image_field.className = image_style
                image_delete.className = image_delete_style

                image_delete.addEventListener("click", function() {removeImage(i)})

                fr.addEventListener("load", function () {
                    image_field.setAttribute('src', fr.result)
                }, false);

                fr.readAsDataURL(image);
                load_photo_field.after(image_box)
                image_box.append(image_field)
                image_box.append(image_delete)
            }
        }
    });
})