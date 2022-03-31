function make_api_deny_call(key) {
  const url = `/api/deny_request?key=${key}`;
  fetch(url)
    .then((res) => res.json())
    .then((out) => {
      switch (out.state) {
        case "success":
          window.location.replace(
            `${url_request}?u=${out.username}&a=${out.amount}&s=deny`
          );
          break;

        case "error":
          window.location.replace(`${url_request}?s=error`);
          break;

        default:
          throw "Invalid response!";
      }
    })
    .catch((err) => {
      throw err;
    });
}