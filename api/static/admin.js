/**
 * Function to update all information on the page
 */
function update_state() {
    let myHeaders = new Headers({
        "Authorization": token
    });

    let myInit = {
        method: 'GET',
        headers: myHeaders,
        mode: 'cors',
        cache: 'default',
    };

    fetch('/state', myInit)
        .then(response => {
            return response.json();
        })
        .then(json => {
            manageMode(json.mode);
            manageStart(json.started);
            manageSeq(json.sequence);
            manageFps(json.fps);
            manageNetwork(json.net);
            $("#card").find("[data-toggle='toggle']").bootstrapToggle();
        })
}

/**
 * Function to manage Network informations
 * @param net network information
 */
function manageNetwork(net) {
    $('#ip1').val(net.ip1);
    $('#port1').val(net.port1);
    $('#ip2').val(net.ip2);
    $('#port2').val(net.port2);
}

/**
 * Function to send network data to api
 */
function sendNetwork() {
    let ip1 = $('#ip1').val();
    let port1 = $('#port1').val();
    let ip2 = $('#ip2').val();
    let port2 = $('#port2').val();
    let form = new FormData();
    form.append("ip1", ip1);
    form.append("ip2", ip2);
    form.append("port1", port1);
    form.append("port2", port2);
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

    fetch('/network', myInit)
        .then(response => {
            return response.json();
        }).then(json => {
        if (!json.state) {
            Swal.fire({
                type: 'error',
                title: 'Oops...',
                text: json.message,
            });
        } else {
            Swal.fire({
                type: 'success',
                title: 'Network set',
                text: json.message,
            });
        }
    });
}

/**
 * Function to manage fps information
 * @param fps fps information
 */
function manageFps(fps) {
    $('#slide_fps').val(fps);
    $('#spin_fps').val(fps);
}

/**
 * function to manage nb sequence in queue information
 */
function update_seq() {
    let myHeaders = new Headers({
        "Authorization": token
    });

    let myInit = {
        method: 'GET',
        headers: myHeaders,
        mode: 'cors',
        cache: 'default',
    };
    fetch('/state', myInit)
        .then(response => {
            return response.json();
        })
        .then(json => {
            $('#nbSeq').text(`${json.nb_seq_in_queue} sequence in queue`);
        })
}

/**
 * function to manage mode button
 * @param mode
 */
function manageMode(mode) {
    $(`#${mode}`).button("checked")
}

/**
 * callback function when spiner change
 * @param spiner spiner data
 */
function spinerChange(spiner) {
    $('#slide_fps').val(spiner.value);
    sendfps(spiner.value);
}

/**
 * callback function when slider change
 * @param slider slider data
 */
function sliderChange(slider) {
    $('#spin_fps').val(slider.value);
    sendfps(slider.value);
}

/**
 * function to send fps to api
 * @param fps fps to send
 */
function sendfps(fps) {
    let form = new FormData();
    form.append("fps", fps);
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

    fetch('/fps', myInit)
        .then(response => {
            return response.json();
        }).then(json => {
        if (!json.state) {
            Swal.fire({
                type: 'error',
                title: 'Oops...',
                text: json.message,
            });
            update_state();
        }
    });
}

/**
 * function to manage on/off cube button
 * @param started if cube is started or not
 */
function manageStart(started) {
    let check = $("#spanStart");
    let checked = (started) ? "checked" : "";
    let buffer = `<input id ="checkStart" type="checkbox" ${checked} data-toggle="toggle" data-onstyle="success" onchange="startChange(this)">`;
    check.html(buffer);
}

/**
 * function to manage sequence button
 * @param seq if sequence is started or not
 */
function manageSeq(seq) {
    let check = $("#spanSeq");
    let checked = (seq) ? "checked" : "";
    let buffer = `<input id ="checkSeq" type="checkbox" ${checked} data-toggle="toggle" data-onstyle="success" onchange="seqChange(this)">`;
    check.html(buffer);
}

/**
 * callback function to start cube button
 * @param btn button information
 */
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

/**
 * callback function to mode button
 * @param btn button information
 */
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

/**
 * callback function to sequence button
 * @param btn button information
 */
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

    fetch('/startseq', myInit)
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
            let old_check = check.prop("checked");
            check.bootstrapToggle("destroy");
            check.prop("checked", !old_check);
            check.bootstrapToggle();
        }
    });

}

/**
 * callback function to kill sequence button
 * @param btn button information
 */
function killSeq(btn) {
    let myHeaders = new Headers({
        "Authorization": token
    });

    let myInit = {
        method: 'GET',
        headers: myHeaders,
        mode: 'cors',
        cache: 'default',
    };
    fetch('/stopseq', myInit)
        .then(response => {
            return response.json();
        })
        .then(json => {
            update_seq();
        })
}

/**
 * callback function to reset sequence button
 * @param btn button information
 */
function reset(btn) {
    let myHeaders = new Headers({
        "Authorization": token
    });

    let myInit = {
        method: 'GET',
        headers: myHeaders,
        mode: 'cors',
        cache: 'default',
    };
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
            fetch('/reset', myInit)
                .then(response => {
                    return response.json();
                })
                .then(json => {
                    update_seq();
                })
        }
    });
}