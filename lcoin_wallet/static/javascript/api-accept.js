function make_api_accept_call(key) {
  const url = `/api/accept_request?key=${key}`;
  fetch(url)
    .then((res) => res.json())
    .then((out) => {
      switch (out.state) {
        case "success":
          window.location.replace(
            `{{url_for('request')}}?u=${out.username}&a=${out.amount}&s=accept`
          );
          break;

        case "error":
          window.location.replace(`{{url_for('request')}}?s=error`);
          break;

        default:
          throw "Invalid response!";
      }
    })
    .catch((err) => {
      throw err;
    });
}
