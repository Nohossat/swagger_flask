document.getElementById("lookup-panel").classList.add("active");


document.querySelectorAll(".panel-btn").forEach(el =>
  el.addEventListener("click", (e) => changePanel(e))
)


document.querySelector("#get-tweet-btn").addEventListener("click", async function(e) {
    await getId(e, "fetch-result")
});

document.querySelector("#sentiment-get-btn").addEventListener("click", async function(e) {
    await getId(e, "fetch-sentiment-result")
});

document.querySelector("#delete-get-btn").addEventListener("click", async function(e) {
    await getId(e, "fetch-delete-result")
});

document.querySelector("#compute-sentiment").addEventListener("click", async function(e) {
    await computeSentiment(e, "fetch-sentiment-result")
});

document.querySelector("#delete-btn").addEventListener("click", async function(e) {
    await deleteTweet(e, "fetch-delete-result")
});

document.querySelector("#post-btn").addEventListener("click", async function(e) {
    await postTweets(e, "post-results")
});

// get all tweets
getAllTweets()


function changePanel(e) {
  document.querySelectorAll(".panel-btn").forEach(el =>
    el.classList.remove("active")
  )
  e.target.classList.add("active")


  if (e.target.classList.contains("lookup-btn")) {
    document.getElementById("lookup-panel").classList.add("active");
    document.getElementById("results-panel").classList.remove("active");
  } else {
    document.getElementById("lookup-panel").classList.remove("active");
    document.getElementById("results-panel").classList.add("active");
  }

}

async function computeSentiment(e, displayElementId) {
    e.preventDefault()
    let parentForm = e.target.parentElement;
    let id = parentForm.querySelector(".tweet-id").value;

    document.getElementById(displayElementId).innerHTML = "computing sentiment value";

    const res = await fetch(
        'http://0.0.0.0:5000/api/v1/tweet/' + id,
        {
            headers: {
            'Content-Type' : 'application/json'
            },
            method: 'PUT'
        })

    const result = await res.json();

    let response = JSON.stringify(result, null, '\t');

    // change presentation to table
    document.getElementById(displayElementId).innerHTML = response;

    // refresh tweets table
    getAllTweets()
}

async function getId(e, displayElementId) {
    e.preventDefault()

    let targetId = "#" + displayElementId + " tr";

    document.querySelectorAll(targetId).forEach(e => e.remove());

    let parentForm = e.target.parentElement;
    let id = parentForm.querySelector(".tweet-id").value;

    const res = await fetch(
        'http://0.0.0.0:5000/api/v1/tweet/' + id,
        {
            headers: {
            'Content-Type' : 'application/json'
            },
            method: 'GET'
        })

    const result = await res.json();

    let table = document.getElementById(displayElementId);

    Object.entries(result).map((value, key) => {
        let newTr = document.createElement("tr");
        let newTd1 = document.createElement("td");
        let newTd2 = document.createElement("td");

        newTd1.append(value[0]);
        newTd2.append(value[1]);
        newTr.appendChild(newTd1);
        newTr.appendChild(newTd2);
        table.appendChild(newTr);
    })
}

async function deleteTweet(e, displayElementId) {
    e.preventDefault()
    let parentForm = e.target.parentElement;
    let id = parentForm.querySelector(".tweet-id").value;

    const res = await fetch(
        'http://0.0.0.0:5000/api/v1/tweet/' + id,
        {
            headers: {
            'Content-Type' : 'application/json'
            },
            method: 'DELETE'
        })

    const result = await res.json();

    let response = result["text"];

    if (result["text"] == undefined) {
        response = result["msg"]
    }

    // change presentation to table
    document.getElementById(displayElementId).innerHTML = response;

    // update big table
    await getAllTweets()
}

async function postTweets(e, displayElementId) {
    e.preventDefault()
    let parentForm = e.target.parentElement;
    let tweets_values = parentForm.querySelector(".post_json").value;

    const res = await fetch(
        'http://0.0.0.0:5000/api/v1/tweet/',
        {
            body: JSON.stringify({
                tweets : JSON.parse(tweets_values)
             }),
            headers: {
            'Content-Type' : 'application/json'
            },
            method: 'POST'
        })

    const result = await res.json();

    // display table
    let table = document.getElementById(displayElementId);
    let parentTable = table.parentElement;

    result["tweets"].forEach(item => {
        table.appendChild(convertToRow(item));
    })

    parentTable.classList.remove("hidden");

    // update big table
    await getAllTweets()

}

async function getAllTweets() {
    // reset table
    document.querySelectorAll('#tweets-results tr').forEach(e => e.remove());

    const res = await fetch(
        'http://0.0.0.0:5000/api/v1/tweet/tweets',
        {
            method: 'GET'
        })

    const result = await res.json();

    let table = document.getElementById("tweets-results");

    result["tweets"].forEach(item => {
        table.appendChild(convertToRow(item));
    })
}


function convertToRow(elements) {
    let row = document.createElement("tr");
    let res = Object.values(elements).forEach(item => {
        let tdItem = document.createElement("td");
        tdItem.append(item);
        row.appendChild(tdItem);
    })
    return row;
}