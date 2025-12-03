document.addEventListener('DOMContentLoaded', () => {
    initTokenTests();
    initApiTests();
    initAuthTests();
    initTokenAuthTests(); 
});

function initTokenTests() {
    let btn = document.getElementById("api-user-token-button");
    let res = document.getElementById("api-user-token-result");
    if(btn) btn.addEventListener('click', () => {
        fetch(`/user`, {
            method: 'GET',
            headers: {  
                "Authorization": "Basic YWRtaW46YWRtaW4=",
            }
        })
        .then(r => {
            if(r.status == 200) {
                r.json().then(j => {

                    let [_, jwtPayload, __] = j.data.split('.');

                    let payloadJson = JSON.parse(
                        atob(jwtPayload.replace(/-/g, '+').replace(/_/g, '/'))
                    );

                    res.innerHTML =
                        `<i id="token">${j.data}</i><pre>` +
                        JSON.stringify(payloadJson, null, 4) +
                        `</pre>`;

                });

            }
            else {
                r.text().then(t => {res.innerHTML = t});
            }

        }); 
    });
}

function initApiTests() {
    const apiNames = ["user", "order","product"];
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
        let tokenElement = document.getElementById("token");
        let auth = tokenElement ? `Bearer ${tokenElement.innerText}` : "Basic YWRtaW46YWRtaW4=";

        let conf = {
            method: apiMethod.toUpperCase(),
            headers: {
                // YWRtaW46YWRtaW46    admin:admin
                // YWRtaW46YWRtaW0=    admin:admin
                // YWRtaW46YWRtaW4=    admin:admin
                "Authorization": auth,
                "Custom-Header": "custom-value"
            }


    };
    const body = btn.getAttribute("data-body");
    if(body) {
        conf.body = body;
        conf.headers["Content-Type"] = "application/json; charset=utf-8";

    }
    fetch(`/${apiName}`, conf)
        .then(r => {
            if(r.status == 200) {
                r.json().then(j => {res.textContent = JSON.stringify(j, null, 4);});
            }
            else {
                r.text().then(t => {res.innerHTML = t});
            }
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




function initTokenAuthTests() {

    const tests = [
        ["api-user-token-ok-button",     "api-user-token-ok-result",     "VALID"],
        ["api-user-token-wrong-button",  "api-user-token-wrong-result",  "WRONG"],
        ["api-user-token-broken-button", "api-user-token-broken-result", "BROKEN"],
    ];

    for (let [btnId, resId, mode] of tests) {
        let btn = document.getElementById(btnId);
        if (!btn) continue;

        btn.addEventListener("click", () => {
            let res = document.getElementById(resId);

            fetch("/user", {
                method: "GET",
                headers: { "Authorization": "Basic YWRtaW46YWRtaW4=" }
            })
            .then(r => r.json())
            .then(j => {
                let token = j.data;

                if (mode === "WRONG") token = token.slice(0, -2) + "xx";
                if (mode === "BROKEN") token = "12345";

                fetch("/user", {
                    method: "GET",
                    headers: { "Authorization": "Bearer " + token }
                })
                .then(r => r.json())
                .then(j => { res.textContent = JSON.stringify(j, null, 4); });
            });
        });
    }
}


function initAuthTests() {
    const tests = [
        ["api-user-auth-ok-button", "api-user-auth-ok-result",  "Basic YWRtaW46YWRtaW4="],      // admin:admin
        ["api-user-auth-wrong-pass-button", "api-user-auth-wrong-pass-result", "Basic YWRtaW46d3Jvbmc="], // admin:wrong
        ["api-user-auth-wrong-login-button", "api-user-auth-wrong-login-result", "Basic d3Jvbmc6YWRtaW4="], // wrong:admin
    ];

    for (let [btnId, resId, authString] of tests) {
        let btn = document.getElementById(btnId);
        if (!btn) continue;

        btn.addEventListener("click", () => {
            let res = document.getElementById(resId);
            fetch("/user", {
                method: "GET",
                headers: {
                    "Authorization": authString,
                    "Custom-Header": "custom-value"
                }
            })
            .then(r => r.json())
            .then(j => { res.textContent = JSON.stringify(j, null, 4); })
        });
    }
}
