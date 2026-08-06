// To run index.html, need to run a local server - run "python -m http.server 5500" in the frontend directory in terminal, 
// then open http://localhost:8000 in a browser

/* fake data shaped like what the real API will return
const fixtures = [
  {
    fixtureId: 101,
    homeTeam: "Arsenal",
    awayTeam: "Chelsea",
    actualResult: "Home win",
    predictedResult: "Home win"
  },
  {
    fixtureId: 102,
    homeTeam: "Everton",
    awayTeam: "Liverpool",
    actualResult: "Draw",
    predictedResult: "Away win"
  },
  {
    fixtureId: 103,
    homeTeam: "Man United",
    awayTeam: "Newcastle",
    actualResult: "Home win",
    predictedResult: "Home win"
  },
  {
    fixtureId: 104,
    homeTeam: "Tottenham",
    awayTeam: "Brighton",
    actualResult: "Away win",
    predictedResult: "Draw"
  },
  {
    fixtureId: 105,
    homeTeam: "Aston Villa",
    awayTeam: "West Ham",
    actualResult: "Home win",
    predictedResult: "Home win"
  },
  {
    fixtureId: 106,
    homeTeam: "Brentford",
    awayTeam: "Fulham",
    actualResult: "Draw",
    predictedResult: "Draw"
  },
  {
    fixtureId: 107,
    homeTeam: "Crystal Palace",
    awayTeam: "Wolves",
    actualResult: "Home win",
    predictedResult: "Away win"
  },
  {
    fixtureId: 108,
    homeTeam: "Bournemouth",
    awayTeam: "Nottingham Forest",
    actualResult: "Away win",
    predictedResult: "Away win"
  },
  {
    fixtureId: 109,
    homeTeam: "Leicester",
    awayTeam: "Southampton",
    actualResult: "Home win",
    predictedResult: "Home win"
  },
  {
    fixtureId: 110,
    homeTeam: "Burnley",
    awayTeam: "Man City",
    actualResult: "Away win",
    predictedResult: "Away win"
  },
  {
    fixtureId: 111,
    homeTeam: "Liverpool",
    awayTeam: "Arsenal",
    actualResult: "Draw",
    predictedResult: "Home win"
  },
  {
    fixtureId: 112,
    homeTeam: "Chelsea",
    awayTeam: "Everton",
    actualResult: "Home win",
    predictedResult: "Home win"
  },
  {
    fixtureId: 113,
    homeTeam: "Newcastle",
    awayTeam: "Tottenham",
    actualResult: "Away win",
    predictedResult: "Away win"
  },
  {
    fixtureId: 114,
    homeTeam: "Brighton",
    awayTeam: "Man United",
    actualResult: "Draw",
    predictedResult: "Draw"
  },
  {
    fixtureId: 115,
    homeTeam: "West Ham",
    awayTeam: "Brentford",
    actualResult: "Home win",
    predictedResult: "Home win"
  },
  {
    fixtureId: 116,
    homeTeam: "Fulham",
    awayTeam: "Crystal Palace",
    actualResult: "Away win",
    predictedResult: "Draw"
  },
  {
    fixtureId: 117,
    homeTeam: "Wolves",
    awayTeam: "Bournemouth",
    actualResult: "Home win",
    predictedResult: "Home win"
  },
  {
    fixtureId: 118,
    homeTeam: "Nottingham Forest",
    awayTeam: "Leicester",
    actualResult: "Draw",
    predictedResult: "Draw"
  },
  {
    fixtureId: 119,
    homeTeam: "Southampton",
    awayTeam: "Burnley",
    actualResult: "Home win",
    predictedResult: "Away win"
  },
  {
    fixtureId: 120,
    homeTeam: "Man City",
    awayTeam: "Aston Villa",
    actualResult: "Home win",
    predictedResult: "Home win"
  },
  {
    fixtureId: 121,
    homeTeam: "Arsenal",
    awayTeam: "Newcastle",
    actualResult: "Home win",
    predictedResult: "Home win"
  },
  {
    fixtureId: 122,
    homeTeam: "Chelsea",
    awayTeam: "Brighton",
    actualResult: "Draw",
    predictedResult: "Draw"
  },
  {
    fixtureId: 123,
    homeTeam: "Liverpool",
    awayTeam: "Fulham",
    actualResult: "Home win",
    predictedResult: "Home win"
  },
  {
    fixtureId: 124,
    homeTeam: "Everton",
    awayTeam: "Wolves",
    actualResult: "Away win",
    predictedResult: "Draw"
  },
  {
    fixtureId: 125,
    homeTeam: "Tottenham",
    awayTeam: "Leicester",
    actualResult: "Home win",
    predictedResult: "Home win"
  },
  {
    fixtureId: 126,
    homeTeam: "Aston Villa",
    awayTeam: "Bournemouth",
    actualResult: "Home win",
    predictedResult: "Away win"
  },
  {
    fixtureId: 127,
    homeTeam: "West Ham",
    awayTeam: "Southampton",
    actualResult: "Draw",
    predictedResult: "Draw"
  },
  {
    fixtureId: 128,
    homeTeam: "Brentford",
    awayTeam: "Man City",
    actualResult: "Away win",
    predictedResult: "Away win"
  },
  {
    fixtureId: 129,
    homeTeam: "Crystal Palace",
    awayTeam: "Liverpool",
    actualResult: "Away win",
    predictedResult: "Away win"
  },
  {
    fixtureId: 130,
    homeTeam: "Man United",
    awayTeam: "Chelsea",
    actualResult: "Home win",
    predictedResult: "Draw"
  }
];
*/

const PAGE_SIZE = 10;
let currentPage = 1;
let currentSeasonId = 1;

// Takes an array of fixtures and renders them into the table 
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

// Renders pagination controls based on the current page and total number of fixtures
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

// Fetches fixtures for a given page and season, then renders them along with pagination controls
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

// Fetches explanation data for a fixture and displays it in the explanation panel
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

function formatScore(score) {
  return score === null ? "N/A" : `${Math.round(score * 15)}/15`;
}

// Call the function once DOMContentLoaded (page is fully loaded)
document.addEventListener("DOMContentLoaded", function () {
  goToPage(1, currentSeasonId); // render first page of fixtures
});
