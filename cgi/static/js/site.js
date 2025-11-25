document.addEventListener('DOMContentLoaded', () => {
    initApiTests();
});

function initApiTests() {
    const apiNames = ["user", "order"];
    const apiMethods = ["get","post","put","patch","delete"];
    for(let apiName of apiNames) {
        for(let apiMethod of apiMethods) {
            let id = `api-${apiName}-${apiMethod}-button`;
            let btn = document.getElementById(id);
            if(btn) btn.addEventListener('click', apiButtonClick);
        }
    }
}

function apiButtonClick(e) {
    const btn = e.target;
    const [_, apiName, apiMethod, __] = btn.id.split('-');
    const resId = `api-${apiName}-${apiMethod}-result`;
    const res = document.getElementById(resId);
    if(res) {
    let conf = {
        method: apiMethod.toUpperCase(),
    };
    const body = btn.getAttribute("data-body");
    if(body) {
        conf.body = body;
        conf.headers = {
            "Content-Type": "application/json; charset=utf-8"
        };
    }
    fetch(`/${apiName}`, conf).then(r => r.json())
    .then(j => {
       res.textContent = JSON.stringify(j, null, 4);
    })
    }
    else throw resId + " not found";
}


function objToHtml(j, level=0) {
    let sp = "&emsp;".repeat(level);
    let html = "{<br/>";
    html += Object.keys(j).map(k => {
        let val = typeof j[k] == 'object' ? objToHtml(j[k], level + 1) : j[k];
        return `${sp}&emsp;${k}: ${val}<br/>`;
    }).join(",<br/>");
    // for(let k in j) {
    //     let val = typeof j[k] == 'object' ? objToHtml(j[k], level + 1) : j[k];
    //     html += `${sp}&emsp;${k}: ${val}<br/>`;
    // }
    html += `<br/>${sp}}`;
    return html;
}
