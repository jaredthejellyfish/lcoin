
$(function () {
    $('html').on('click', function () {
        setInterval(function () {
            const url = `/api/pending_requests`;
            const notify_element = document.getElementById("notify");
            const notify = notify_element.classList.contains("badge1")
            fetch(url)
                .then((res) => res.json())
                .then((out) => {
                    
                    switch (out.notification_badge) {
                        case "true":

                            if (notify == false){
                                $('#notify').addClass('badge1');
                            };
                            
                            break;

                        case "false":
                            if (notify == true){
                                $('#notify').removeClass('badge1');
                            };
                            
                            break;

                        default:
                            
                            throw "Invalid response!";
                    }
                })
                .catch((err) => {
                    throw err;
                });

        }, 10000);
    });
});