const $button = $("#button");
const $response = $("#response");
const $score = $("#high_score");
let score = 0;
let timeout = 0;

$score.html(`Your score is ${score}`)



$button.on('click', (event) => {
    event.preventDefault()
    $response.html("")
    const guess = $("#guess").val()
    if (timeout != 1)
        checkIfValidFoundWord(guess);

})

async function checkIfValidFoundWord(guess) {
    const resp = await axios.get("/check-word", { params: { word: guess } });
    $response.append(resp.data.result)
    if (resp.data.result == "ok") {
        score++;
        $score.html(`Your score is ${score}`);
    }
    setTimeout(function () { timeout = 1 }, 60000);
}

//left off step six