import {getNewQuery} from './change_query_string.js';

document.addEventListener("DOMContentLoaded", function () {
    // Установка ссылок для пагинатора.
    let new_page_links = document.querySelectorAll('a[page_number]');

    for (let new_page_link of new_page_links) {
        let params = {
            'page': new_page_link.getAttribute('page_number'),
        }
        new_page_link.href = getNewQuery(params)
    }
});