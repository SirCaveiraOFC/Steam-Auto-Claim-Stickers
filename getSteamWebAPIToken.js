(async function() {
    const current_token = await getWebapiToken();

    prompt("Current SteamWebAPIToken (copy this and paste into 'steam_webapi_token.txt' file):", current_token);
})();

async function getWebapiToken() {
    let webapi_token = null;

    if (window.application_config?.dataset?.loyalty_webapi_token) {
        webapi_token = JSON.parse(window.application_config.dataset.loyalty_webapi_token);
    } else {
        const res = await fetch('/category/action');
        const html = await res.text();
        const doc = new DOMParser().parseFromString(html, 'text/html');
        const token = doc.getElementById('application_config')?.dataset?.loyalty_webapi_token;
        if (!token) {
            throw new Error('No valid API token found. Are you logged in?');
        }
        webapi_token = JSON.parse(token);
    }
    return webapi_token;
}
