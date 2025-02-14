window.____PH_reqfn____ = async (arg) => {
    const response = await fetch("____PH_requrl____", {
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
