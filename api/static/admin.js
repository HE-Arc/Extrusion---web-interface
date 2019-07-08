function update_state() {

    fetch('/state')
        .then(response => {
            return response.json();
        })
        .then(json => {
            manageMode(json.mode);
            manageStart(json.started);
            manageSeq(json.sequence);
            $("#card").find("[data-toggle='toggle']").bootstrapToggle();
        })
}

function update_seq() {

    fetch('/state')
        .then(response => {
            return response.json();
        })
        .then(json => {
            $('#nbSeq').text(`${json.nb_seq_in_queue} sequence in queue`);
        })
}

function manageMode(mode) {
    $(`#${mode}`).button("checked")
}

function manageStart(started) {
    let check = $("#spanStart");
    let checked = (started) ? "checked" : "";
    let buffer = `<input id ="checkStart" type="checkbox" ${checked} data-toggle="toggle" data-onstyle="success" onchange="startChange(this)">`;
    check.html(buffer);
}

function manageSeq(seq) {
    let check = $("#spanSeq");
    let checked = (seq) ? "checked" : "";
    let buffer = `<input id ="checkSeq" type="checkbox" ${checked} data-toggle="toggle" data-onstyle="success" onchange="seqChange(this)">`;
    check.html(buffer);
}

function startChange(btn) {
    let startStop = (btn.checked) ? "start" : "stop";
    let myHeaders = new Headers({
        "Authorization": token
    });

    let myInit = {
        method: 'GET',
        headers: myHeaders,
        mode: 'cors',
        cache: 'default',
    };

    fetch(` /${startStop}`, myInit)
        .then(response => {
            return response.json();
        }).then(json => {
        update_state();

    });

}

function modeChange(btn) {
    let form = new FormData();
    form.append("mode", btn.id);
    let myHeaders = new Headers({
        "Authorization": token
    });

    let myInit = {
        method: 'POST',
        headers: myHeaders,
        mode: 'cors',
        cache: 'default',
        body: form,
    };

    fetch('/changemode', myInit)
        .then(response => {
            return response.json();
        }).then(json => {
        update_state();
    });

}

function seqChange(btn) {
    let form = new FormData();
    form.append("start", btn.checked);
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

    fetch('/changeseq', myInit)
        .then(response => {
            return response.json();
        }).then(json => {
        if (!json.state) {
            Swal.fire({
                type: 'error',
                title: 'Oops...',
                text: json.message,
            });
            let check = $(`#${btn.id}`);
            console.log(btn.id);
            let old_check = check.prop("checked");
            check.bootstrapToggle("destroy");
            check.prop("checked", !old_check);
            check.bootstrapToggle();
        }
    });

}

function killSeq(btn) {
    fetch('/stopseq')
        .then(response => {
            return response.json();
        })
        .then(json => {
            console.log(json.message);
            update_seq();
        })
}

function reset(btn) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, Reset!'
    }).then((result) => {
        if (result.value) {
            fetch('/reset')
                .then(response => {
                    return response.json();
                })
                .then(json => {
                    console.log(json.message);
                    update_seq();
                })
        }
    });
}