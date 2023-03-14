const searchBox = document.getElementById("searchBox");
const suggestionList = document.getElementById("suggestionList");

let delayTimer;

searchBox.addEventListener("input", () => {
  const inputValue = searchBox.value.trim();

  clearTimeout(delayTimer);
  if (inputValue.length > 3) {
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

async function fetchSuggestions(inputValue) {
  try {
    const response = await fetch(`/suggestions?q=${inputValue}`);
    const data = await response.json();

    if (data.length > 0) {
      displaySuggestions(data);
    } else {
      suggestionList.style.display = "none";
    }
  } catch (error) {
    console.error(error);
  }
}

function displaySuggestions(suggestions) {
  suggestionList.innerHTML = "";

  const suggestionListUl = document.createElement("ul");
  suggestionList.appendChild(suggestionListUl);

  suggestions.forEach((suggestion) => {
    const suggestionListLi = document.createElement("li");
    suggestionListLi.textContent = suggestion;
    suggestionListLi.addEventListener("click", () => {
      searchBox.value = suggestion;
      suggestionList.style.display = "none";
    });
    suggestionListUl.appendChild(suggestionListLi);
  });

  suggestionList.style.display = "block";
}
