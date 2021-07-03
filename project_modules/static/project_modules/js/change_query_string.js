function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function isEmptyObject(obj) {
    for (let i in obj) {
        if (obj.hasOwnProperty(i)) {
            return false;
        }
    }
    return true;
}


export function getQueryStrings(string) {
    // Получение параметров запроса и создание словаря параметров {имя_параметра': 'значение_параметра'}.
    let assoc  = {},
        decode = function (s) { return decodeURIComponent(s.replace(/\+/g, " ")); },
        queryString = location.search.substring(1);

    if (string) queryString = string
    let keyValues = queryString.split('&');

    for (let keyVal of keyValues) {
        let key = keyVal.split('=');
        if (key.length > 1) {
            assoc[decode(key[0])] = decode(key[1]);
        }
    }

    return assoc;
}


export  function getNewQuery(new_params, path_name='') {
    // Замена параметров запроса на переданные и составление новой строки параметров запроса.
    let querystring = getQueryStrings(),
        new_query = '';

    for (let param_key in new_params) {
        if (new_params[param_key]) {
            querystring[param_key] = new_params[param_key]
        } else {
            delete querystring[param_key];
        }
    }

    let count_query_keys = Object.keys(querystring).length,
        counter = 0;

    if (!isEmptyObject(querystring)) {
        new_query += '?'
        for (let key in querystring) {
            counter += 1
            new_query += key + '=' +querystring[key]
            if (counter != count_query_keys) new_query += '&'
        }
    }

    if (new_query.length == 0 && path_name.length == 0) {
        new_query = window.location.href.split('?')[0]
    }

    return path_name + new_query
}


export function addCommonFilters(object_name, filter_names_list = [], path_name = '') {
    // Установка фильтров для отображаемых объектов.
    let objects_per_page = document.querySelector(`select[name="${object_name}_per_page"]`),
        all_query_params = {},

        current_query_params = getQueryStrings();

    for (let filter_name of filter_names_list) {
        all_query_params[filter_name] = document.querySelector(`input[name="${filter_name}"]`)
        all_query_params[filter_name].onchange = function () {
            setFiltervalues()
            document.location.href = getNewQuery(all_query_params,path_name);
        }
    }

    function setFiltervalues() {
        // Установка значений фильтров
        for (let filter_name in all_query_params) {
            let filter_value = all_query_params[filter_name].value;

            if (filter_value.length == 0) {
                filter_value = NaN
            }
            all_query_params[filter_name] = filter_value
        }
        all_query_params['page'] = NaN
    }

    if (objects_per_page) {
        objects_per_page.onchange = function () {
            // Управление колличеством отображаемых объектов на странице.
            setFiltervalues()

            document.cookie = `${object_name}_per_page=` + encodeURIComponent(this.value)
            document.location.href = getNewQuery(all_query_params);
        }

        for (let option of objects_per_page.options) {
            if (option.value == getCookie(`${object_name}_per_page`)){
                option.selected = true
            }
        }
    }
    // Получаем значения фильтров из запроса и устанавливаем эти значения в свои поля.
    for (let filter_name in all_query_params) {
        if (filter_name in current_query_params) {
            all_query_params[filter_name].value = current_query_params[filter_name]
        }
    }
}
