let token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjE2NTQ4MzIsIm5iZiI6MTU2MTY1NDgzMiwianRpIjoiY2RlMGVmODUtODE0Yi00MDMyLTg0MjYtMTFmNTdmNDU0YTMzIiwiaWRlbnRpdHkiOiJzdXBlcnVzZXIiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJtb2RlIjoic3VwZXJ1c2VyIn19.VikRbAUyitePctkQ51t1adr4jBOZImyL0LrR4xLmZLs";
$(window).on("load", function () {
    update_tab();
    $('#createForm').on("submit", function (e) {
        create();
        return false;
    });
});

function update_tab() {
    let myHeaders = new Headers({
        "Authorization": token,
    });

    let myInit = {
        method: 'GET',
        headers: myHeaders,
        mode: 'cors',
        cache: 'default'
    };

    fetch('/token', myInit)
        .then(response => {
            return response.json();
        })
        .then(json => {
            $.each(json, function (index, val) {
                let buffer = "";
                for (let i = 0; i < val.length; i++) {
                    let item = val[i];
                    let checked = (item.active) ? "checked" : "";
                    buffer += `<tr>
                            <td>${item.identity}</td>
                            <td>${item.mode}</td>
                            <td><button type="button" class="btn btn-sm btn-success" data-toggle="popover" title="Copy token" data-content="${item.token}">token</button></td>
                            <td>${get_days(item.date)}</td>`;
                    if (item.mode !== "superuser") {
                        buffer += `<td><input id ="${item.jti}" type="checkbox" ${checked} data-toggle="toggle" data-onstyle="dark" onchange="checkboxChange(this)"></td>`;
                        buffer += `<td><button value="${item.jti}" type="button" class="btn btn-sm btn-danger" onclick="deleteToken(this)">delete</button></td></tr>`;
                    } else {
                        buffer += `<td>-</td>`;
                        buffer += `<td>-</td>`;
                    }
                }
                $('tbody').html(buffer);
                $("[data-toggle='toggle']").bootstrapToggle();
                $("[data-toggle='popover']").popover();
            });
        })
}


function checkboxChange(checkbox) {
    let form = new FormData();
    form.append("jti", checkbox.id);
    let myHeaders = new Headers({
        "Authorization": token
    });

    let myInit = {
        method: 'PATCH',
        headers: myHeaders,
        mode: 'cors',
        cache: 'default',
        body: form
    };

    fetch('/token', myInit)
        .then(response => {
            return response.json();
        }).then(json => {
        if (!json.state) {
            Swal.fire({
                type: 'error',
                title: 'Oops...',
                text: json.message,
            });
            let check = $(`#${checkbox.id}`);
            old_check = check.prop("checked");
            check.bootstrapToggle("destroy");
            check.prop("checked", !old_check);
            check.bootstrapToggle();
        }
    });
}

function deleteToken(button) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.value) {
            let form = new FormData();
            form.append("jti", button.value);
            let myHeaders = new Headers({
                "Authorization": token
            });

            let myInit = {
                method: 'DELETE',
                headers: myHeaders,
                mode: 'cors',
                cache: 'default',
                body: form
            };

            fetch('/token', myInit)
                .then(response => {
                    return response.json();
                }).then(json => {
                if (json.state) {
                    update_tab();
                    Swal.fire(
                        'Deleted!',
                        json.message,
                        'success'
                    )
                } else {
                    Swal.fire({
                        type: 'error',
                        title: 'Oops...',
                        text: json.message,
                    });
                }
            });


        }
    });
}

function get_days(timestamp) {
    if (timestamp == 0) {
        return "unlimited"
    }
    let oneDay = 24 * 60 * 60 * 1000;
    let date = new Date(timestamp * 1000);
    let now = new Date();

    return Math.round(Math.abs((date.getTime() - now.getTime()) / (oneDay)));

}

function create() {
    let identity = $('#identity').val(); //need to parse prevent injection
    let date = $('#revokedDate').val();
    let mode = $('#mode').val();
    if ($('#checkUnlimited').prop("checked")) {
        date = 0
    } else {
        if (date.length === 0) {
            Swal.fire({
                type: 'error',
                title: 'Oops...',
                text: 'Your forgot to pick a date',
            });
            return false;
        } else {
            date = dateToTimestamp(date);
        }


    }

    let form = new FormData();
    form.append("identity", identity);
    form.append("date", date);
    form.append("mode", mode);
    let myHeaders = new Headers({
        "Authorization": token
    });

    let myInit = {
        method: 'POST',
        headers: myHeaders,
        mode: 'cors',
        cache: 'default',
        body: form
    };

    fetch('/token', myInit)
        .then(response => {
            return response.json();
        }).then(json => {
            console.log(json);
        if (json.state) {
            update_tab();
            Swal.fire({
                type: 'info',
                title: json.message,
                text: json.access_token,
            });

        } else {
            Swal.fire({
                type: 'error',
                title: 'Oops...',
                text: json.message,
            });
        }
    });
    return true;

}

function manageDate(checkbox) {
    let date = $('#revokedDate');
    date.prop("disabled", checkbox.checked);
    date.val('').blur();
    date.prop("required", !checkbox.checked);

}

function dateToTimestamp(date) {
    date = new Date(date);
    alert(date);
    return Math.round(date.getTime() / 1000);
}