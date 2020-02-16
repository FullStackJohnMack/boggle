const $button = $("#button");
const $response = $("#response");
const $score = $("#high_score");
let score = 0;  //this score for this game
let num1StopsGame = 0; //when incremented, words can no longer be submitted by clicking the button

//Renders initial score on game board
$score.html(`Your score is ${score}`)


/**
 * Handles button clicks
 */
$button.on('click', (event) => {
    event.preventDefault()
    $response.html("")
    const guess = $("#guess").val()
    if (num1StopsGame != 1)
        checkIfValidFoundWord(guess);
    $("#guess").val("")
})

/**
 * Passes entered word to server to check validity and renders HTML response
 * Also disables button click submission after specficied timeout
 */
async function checkIfValidFoundWord(guess) {
    const resp = await axios.get("/check-word", { params: { word: guess } });
    $response.append(resp.data.result)
    if (resp.data.result == "ok") {
        score++;
        $score.html(`Your score is ${score}`);
    }
    setTimeout(function () {
        num1StopsGame = 1;
        updateGameEndStats();
    }, 60000);
}

/**
 * Updates high score on server side
 *
 */
async function updateGameEndStats() {
    const resp = await axios.get("/end-game", {
        params: {
            is_this_high_score: score
        }
    });
    checkForHighScore()
}

/**
 * Updates the high score on the server side
 *  
 */
async function checkForHighScore(potentialHighScore) {
    const resp = await axios.get("/check-high-score");
}