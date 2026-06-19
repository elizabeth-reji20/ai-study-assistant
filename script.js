console.log("Frontend Loaded");

// Input and Result
const input = document.getElementById("notes");
const result = document.getElementById("result");

// -----------------------------
// Common API Function
// -----------------------------
async function callAPI(endpoint) {

    const text = input.value.trim();

    if (text === "") {
        result.innerText = "Please enter some text.";
        return;
    }

    result.innerText = "Generating...";

    try {

        const response = await fetch(`http://127.0.0.1:8000/${endpoint}`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })

        });

        const data = await response.json();

        if (endpoint === "summarize") {
            result.innerText = data.summary;
        }

        else if (endpoint === "quiz") {
            result.innerText = data.quiz;
        }

        else if (endpoint === "explain") {
            result.innerText = data.explanation;
        }

        else if (endpoint === "form") {
            result.innerText = data.form;
        }

        else if (endpoint === "ask") {
            result.innerText = data.answer;
        }

        else if (endpoint === "flashcards") {
            result.innerText = data.flashcards;
        }

    } catch (error) {

        console.error(error);

        result.innerText = "Something went wrong.";

    }

}

// -----------------------------
// Button Events
// -----------------------------

document.getElementById("summarizeBtn").addEventListener("click", () => {
    callAPI("summarize");
});

document.getElementById("quizBtn").addEventListener("click", () => {
    callAPI("quiz");
});

document.getElementById("explainBtn").addEventListener("click", () => {
    callAPI("explain");
});

document.getElementById("formBtn").addEventListener("click", () => {
    callAPI("form");
});

document.getElementById("askBtn").addEventListener("click", () => {
    callAPI("ask");
});

document.getElementById("flashBtn").addEventListener("click", () => {
    callAPI("flashcards");
});

// -----------------------------
// PDF Upload
// -----------------------------

document.getElementById("pdfBtn").addEventListener("click", async () => {

    const fileInput = document.getElementById("pdfFile");
    const file = fileInput.files[0];

    if (!file) {
        result.innerText = "Please upload a PDF file.";
        return;
    }

    result.innerText = "Reading PDF...";

    const formData = new FormData();
    formData.append("file", file);

    try {

        const response = await fetch("http://127.0.0.1:8000/pdf-summary", {

            method: "POST",

            body: formData

        });

        const data = await response.json();

// Automatically put PDF text into the textbox
document.getElementById("notes").value = data.text;

// Show summary
result.innerText = "✅ PDF uploaded successfully!\n\n" + data.summary;

    }

    catch (error) {

        console.error(error);

        result.innerText = "Error processing PDF.";

    }

});