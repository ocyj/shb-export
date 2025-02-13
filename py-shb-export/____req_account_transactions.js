window.____PH____ = async (arg) => {
    const response = await fetch("https://secure.handelsbanken.se/bb/seip/servlet/ipko?appName=ipko&appAction=GetAccountTransactions", {
        method: "POST",
        // Optionally set headers you need (e.g. Content-Type for JSON)
        headers: {
            "Content-Type": "application/json;charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json"
        },
        // Make sure to include credentials so cookies are sent if needed
        credentials: "include",
        body: JSON.stringify(arg)
    });
    return await response.json();
}
