const searchBox = document.getElementById("searchBox");
const suggestionList = document.getElementById("suggestionList");

let delayTimer;

searchBox.addEventListener("input", () => {
  const inputValue = searchBox.value.trim();

  clearTimeout(delayTimer);
  if (inputValue.length > 5) {
    delayTimer = setTimeout(() => fetchSuggestions(inputValue), 500);
  } else {
    suggestionList.style.display = "none";
  }
});

searchBox.addEventListener("focus", () => {
  suggestionList.style.display = "none";
});

searchBox.addEventListener("blur", () => {
  suggestionList.style.display = "none";
});

function fetchSuggestions(inputValue) {
  try {
    const response = fetch(`/suggestions?q=${inputValue}`);
    const data = response.json();

    if (data.length > 0) {
      displaySuggestions(data);
    } else {
      suggestionList.style.display = "none";
    }
  } catch (error) {
    console.error(error);
  }
}

// // try this
// fetch('your-api-endpoint')
//   .then(response => response.json())
//   .then(data => {
//     const listItems = data.map(verse => `<li>${verse.book.name} ${verse.chapter}:${verse.number} ${verse.text.trim()}</li>`);
//     const suggestionsUL = document.getElementById('suggestionUL');
//     suggestionsUL.innerHTML = listItems.join('');
//   })
//   .catch(error => console.log(error));

function displaySuggestions(suggestions) {
  suggestionList.innerHTML = "";

  const suggestionListUl = document.createElement("ul");
  suggestionList.appendChild(suggestionListUl);

  const results = suggestions.map(
    (v) =>
      `${JSON.stringify(v.book.name)} ${JSON.stringify(
        v.chapter
      )}:${JSON.stringify(v.number)} ${JSON.stringify(v.text)}`
  );
  results.forEach((result) => {
    const suggestionListLi = document.createElement("li");

    suggestionListLi.textContent = result;
    suggestionListLi.addEventListener("click", () => {
      searchBox.value = result;
      suggestionList.style.display = "none";
    });
    suggestionListUl.appendChild(suggestionListLi);
  });

  suggestionList.style.display = "block";
}
