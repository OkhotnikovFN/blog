let findElementWidth = function (elements_list) {
    let elements_list_width = []

    elements_list.forEach(function (item) {
        elements_list_width.push(item.offsetWidth)
    })

    return Math.max.apply(null, elements_list_width) + 10
}

export let setMaxWidth = function (elements_list) {
    let max_width = findElementWidth(elements_list)

    elements_list.forEach(function (item) {
        item.style.width = max_width + 'px'
    })
}
