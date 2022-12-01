"use strict";

// Class definition
var KTLandingPage = function () {
    // Private methods
    var initTyped = function() {
        var typed = new Typed("#kt_landing_hero_text", {
            strings: ["The Best Theme Ever", "The Most Trusted Theme", "#1 Selling Theme"],
            typeSpeed: 50
        });
    }

    var startSocket = function (socketPool) {
        let socket = new WebSocket("ws://fyp.h5.sg/ws");
        let submitBtn = document.querySelector("#detect_submit");

        socket.onopen = function(e) {
            console.log("[open] Connection established");
            socket.send("start");
        };

        socket.onmessage = function(event) {
            try {
                let data = JSON.parse(event.data)

                if (data.status === "error") {
                    // Enable button
                    submitBtn.setAttribute("data-kt-indicator", "off");
                    submitBtn.removeAttribute("disabled")
                    alert("Error: " + data.reason)
                }

                if (data.status === "processing") {
                    console.log(data.action)
                }

                if (data.status === "success") {
                    // Enable button
                    submitBtn.setAttribute("data-kt-indicator", "off");
                    submitBtn.removeAttribute("disabled")
                    console.log(data)

                    // video stats
                    document.querySelector("#stats_frames").innerHTML = data.info.total_frames
                    document.querySelector("#stats_size").innerHTML = data.info.size + " MB"
                    document.querySelector("#stats_duration").innerHTML = data.info.duration
                    document.querySelector("#stats_title").innerHTML = data.info.title
                    document.querySelector("#stats_raw_url").setAttribute("href", data.info.url)

                    //results
                    let ratio, color, text
                    if (data.real > data.fake) {
                        ratio = (data.real / (data.real + data.fake)) * 100
                        color = "#35D29A"
                        text = "Without Face Forgery"
                    } else {
                        ratio = (data.fake / (data.real + data.fake)) * 100
                        color = "#F9666E"
                        text = "With Face Forgery"
                    }

                    document.querySelector("#res_accuracy").innerHTML = `${Math.round(ratio * 10) / 10}%`;
                    document.querySelector("#acc_card").style.backgroundColor = color;
                    document.querySelector("#res_text").innerHTML = text;
                    document.querySelector("#yt_video").setAttribute("src", data.info.yt_embed)

                    document.querySelector("#result_body").classList.remove("d-none");
                }
            } catch (err) {

            }
        };

        socket.onclose = function(e) {
            console.log('Socket is closed. Reconnect will be attempted in 2 seconds.', e.reason);
            setTimeout(function() {
                startSocket(socketPool);
            }, 2000);
        };
        socketPool.pop()
        socketPool.push(socket)
    }

    var main = function() {
        let socketPool = []
        startSocket(socketPool);

        document.querySelector("#detect_submit").addEventListener("click", function (event) {
            event.preventDefault()

            // disable the button
            this.setAttribute("data-kt-indicator", "on");
            this.setAttribute("disabled", "true")

            let url = document.querySelector("#search_input").value;
            socketPool[0].send(url)
            console.log("Clicked!")
        })
    }

    // Public methods
    return {
        init: function () {
            // initTyped();
            main();
        }
    }
}();

// Webpack support
if (typeof module !== 'undefined') {
    module.exports = KTLandingPage;
}

// On document ready
KTUtil.onDOMContentLoaded(function() {
    KTLandingPage.init();
});
