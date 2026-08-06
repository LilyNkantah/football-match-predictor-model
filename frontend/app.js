// To run index.html, need to run a local server - run "python -m http.server 5500" in the frontend directory in terminal, 
// then open http://localhost:5500/index.html in a browser

const PAGE_SIZE = 10;
let currentPage = 1;
let currentSeasonId = 1;

/** Render a list of fixtures into the fixture table, including result badges and Explain buttons/N-A cells. */
function renderFixtures(fixtureList) {
  const tableBody = document.getElementById("fixture-table-body");

  // Clear out anything currently in the table 
  tableBody.innerHTML = "";

  // Loop through each fixture and build a row for it
  fixtureList.forEach(function (fixture) {
    const isNull = fixture.predicted_result === null;
    const isCorrect = fixture.actual_result === fixture.predicted_result;

    const badgeClass = isNull ? "bg-secondary" : isCorrect ? "bg-success" : "bg-danger";

    if (fixture.actual_result === 0) {
      fixture.actual_result = "Draw";
    } else if (fixture.actual_result === 1) {
      fixture.actual_result = "Home win";
    } else if (fixture.actual_result === 2) {
      fixture.actual_result = "Away win";
    }

    if (fixture.predicted_result === 0) {
      fixture.predicted_result = "Draw";
    } else if (fixture.predicted_result === 1) {
      fixture.predicted_result = "Home win";
    } else if (fixture.predicted_result === 2) {
      fixture.predicted_result = "Away win";
    }

    const actionCell = fixture.predicted_result === null
      ? `<td class="text-end">N/A</td>`
      : `<td class="text-end"><button class="btn btn-sm btn-outline-secondary explain-btn" data-fixture-id="${fixture.fixture_id}">Explain</button></td>`;

    const rowHtml = `
      <tr>
        <td>${fixture.home_team_name} vs ${fixture.away_team_name}</td>
        <td>${fixture.actual_result}</td>
        <td>${fixture.predicted_result}</td>
        <td>
          <span class="badge ${badgeClass}">
            ${isNull ? "Training Data" : isCorrect ? "Correct" : "Incorrect"}
          </span>
        </td>
        ${actionCell}
      </tr>
    `;

    // insertAdjacentHTML adds current row HTML onto the end of the table body without wiping out existing rows
    tableBody.insertAdjacentHTML("beforeend", rowHtml);
  });
}

/** Render the Previous/Next pagination controls for the current page and season. */
function renderPageSlice(seasonFixtureCount, pageNumber, pageSize) {
  const paginationControls = document.getElementById("pagination-controls");

  const startIndex = (pageNumber - 1) * pageSize;
  const endIndex = startIndex + pageSize;

  const controlsHtml = `
    <button class="btn btn-sm btn-outline-primary" ${pageNumber === 1 ? "disabled" : ""} data-page="${pageNumber - 1}">
      Previous
    </button>
    &nbsp;
    &nbsp;
    <span>Page ${pageNumber} / ${Math.ceil(seasonFixtureCount / pageSize)}</span>
    &nbsp;
    &nbsp;
    <button class="btn btn-sm btn-outline-primary" ${endIndex >= seasonFixtureCount ? "disabled" : ""} data-page="${pageNumber + 1}">
      Next
    </button>
  `;
  paginationControls.innerHTML = controlsHtml;
}

// Event delegation for pagination buttons
document.getElementById("pagination-controls").addEventListener("click", function (event) {
  const clickedButton = event.target.closest("button"); // find the closest button element that was clicked
  if (clickedButton) {
    const newPage = parseInt(clickedButton.getAttribute("data-page"));
    goToPage(newPage, currentSeasonId);
  }
});

// Event listener for season selection dropdown
document.getElementById("season-selection").addEventListener("change", function (event) {
  const newSeasonId = parseInt(event.target.value);
  currentSeasonId = newSeasonId;
  goToPage(1, currentSeasonId);
});

/** Fetch a page of fixtures for the given season/page from the API, then render the table and pagination controls. */
async function goToPage(pageNumber, seasonId) {
  const response = await fetch(`http://localhost:8000/fixtures/?season_id=${seasonId}&page_number=${pageNumber}`);
  const data = await response.json(); // parses the JSON body

  currentPage = pageNumber;
  currentSeasonId = seasonId;
  renderFixtures(data);
  renderPageSlice(data[0].season_fixture_count, currentPage, PAGE_SIZE);
}

// Event delegation for "Explain" buttons
document.getElementById("fixture-table-body").addEventListener("click", function (event) {
  const clickedButton = event.target.closest(".explain-btn");

  if (clickedButton) {
    const fixtureId = clickedButton.dataset.fixtureId;
    showExplanation(fixtureId);
  }
});

/** Fetch a fixture's prediction features and LLM explanation, then display them in the explanation panel. */
async function showExplanation(fixtureId) {
  const response = await fetch(`http://localhost:8000/explain/${fixtureId}`);
  const data = await response.json();
  console.log("Explanation data:", data);

  const panel = document.getElementById("explain-panel");
  const content = document.getElementById("explain-content");

  content.innerHTML = `
    <p><strong>Home team recent form:</strong> ${formatScore(data.home_form)} | <strong>Away team recent form:</strong> ${formatScore(data.away_form)}</p>
    <p><strong>Home team H2H form:</strong> ${formatScore(data.home_h2h_score)} | <strong>Away team H2H form:</strong> ${formatScore(data.away_h2h_score)}</p>
    <hr>
    <p>${data.llm_explanation}</p>
  `;

  panel.classList.remove("d-none");
}

/** Format a points-per-15 score for display, or "N/A" if the score is null (insufficient data). */
function formatScore(score) {
  return score === null ? "N/A" : `${Math.round(score * 15)}/15`;
}

// Call the function once DOMContentLoaded (page is fully loaded)
document.addEventListener("DOMContentLoaded", function () {
  goToPage(1, currentSeasonId); // render first page of fixtures
});