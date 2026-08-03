// fake data shaped like what the real API will return
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

const PAGE_SIZE = 10;
const currentPage = 1;

// Takes an array of fixtures and renders them into the table 
function renderFixtures(fixtureList) {
  const tableBody = document.getElementById("fixture-table-body");

  // Clear out anything currently in the table 
  tableBody.innerHTML = "";

  // Loop through each fixture and build a row for it
  fixtureList.forEach(function (fixture) {
    const isCorrect = fixture.actualResult === fixture.predictedResult;

    const rowHtml = `
      <tr>
        <td>${fixture.homeTeam} vs ${fixture.awayTeam}</td>
        <td>${fixture.actualResult}</td>
        <td>${fixture.predictedResult}</td>
        <td>
          <span class="badge ${isCorrect ? "bg-success" : "bg-danger"}">
            ${isCorrect ? "Correct" : "Incorrect"}
          </span>
        </td>
        <td class="text-end">
          <button class="btn btn-sm btn-outline-secondary explain-btn" data-fixture-id="${fixture.fixtureId}">
            Explain
          </button>
        </td>
      </tr>
    `;

    // insertAdjacentHTML adds current row HTML onto the end of the table body without wiping out existing rows
    tableBody.insertAdjacentHTML("beforeend", rowHtml);
  });
}

// Renders pagination controls based on the current page and total number of fixtures
function renderPageSlice(fullFixtures, pageNumber, pageSize) {
  const paginationControls = document.getElementById("pagination-controls");

  const startIndex = (pageNumber - 1) * pageSize;
  const endIndex = startIndex + pageSize;

  const controlsHtml = `
    <button class="btn btn-sm btn-outline-primary" ${pageNumber === 1 ? "disabled" : ""} data-page="${pageNumber - 1}">
      Previous
    </button>
    &nbsp;
    &nbsp;
    <span>Page ${pageNumber} / ${Math.ceil(fullFixtures.length / pageSize)}</span>
    &nbsp;
    &nbsp;
    <button class="btn btn-sm btn-outline-primary" ${endIndex >= fullFixtures.length ? "disabled" : ""} data-page="${pageNumber + 1}">
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
    goToPage(newPage);
  }
});

// Helper function to go to a specific page
function goToPage(pageNumber) {
  renderFixtures(fixtures.slice((pageNumber - 1) * PAGE_SIZE, pageNumber * PAGE_SIZE));
  renderPageSlice(fixtures, pageNumber, PAGE_SIZE);
}

// Event delegation for "Explain" buttons
document.getElementById("fixture-table-body").addEventListener("click", function (event) {
  const clickedButton = event.target.closest(".explain-btn");

  if (clickedButton) {
    const fixtureId = clickedButton.dataset.fixtureId;
    showExplanation(fixtureId);
  }
});

// Placeholder for the explanation function
// function showExplanation(fixtureId) {}

// Call the function once DOMContentLoaded (page is fully loaded)
document.addEventListener("DOMContentLoaded", function () {
  goToPage(1); // render first page of fixtures
});

/*
const predictions = [
        { fixture_id: 1208113, predicted_result: 2, home_form: '2022-08-05 19:00:00.000000', away_form: 52, home_h2h_score: 42, away_h2h_score: 42, t1_home_form_gs: 0, t1_away_form_gs: 2, t1_away_form_gc: 1, t2_home_form_gs: 0, t2_home_form_gc: 1, t2_away_form_gs: 2, t2_away_form_gc: 1, t1_home_h2h_gs: 42, t1_home_h2h_gc: 42, t1_away_h2h_gs: 42, t1_away_h2h_gc: 42, t2_home_h2h_gs: 42, t2_home_h2h_gc: 42, t2_away_h2h_gs: 42, t2_away_h2h_gc: 3, llm_explanation: null },
        { fixture_id: 1208114, predicted_result: 1, home_form: '2022-08-06 11:30:00.000000', away_form: 36, home_h2h_score: 40, away_h2h_score: 40, t1_home_form_gs: 2, t1_away_form_gs: 2, t1_away_form_gc: 2, t2_home_form_gs: 0, t2_home_form_gc: 2, t2_away_form_gs: 2, t2_away_form_gc: 2, t1_home_h2h_gs: 40, t1_home_h2h_gc: 3, t1_away_h2h_gs: 40, t1_away_h2h_gc: 40, t2_home_h2h_gs: 40, t2_home_h2h_gc: 40, t2_away_h2h_gs: 40, t2_away_h2h_gc: 40, llm_explanation: null },
        { fixture_id: 1208115, predicted_result: 0, home_form: '2022-08-06 14:00:00.000000', away_form: 35, home_h2h_score: 66, away_h2h_score: 66, t1_home_form_gs: 2, t1_away_form_gs: 0, t1_away_form_gc: 1, t2_home_form_gs: 0, t2_home_form_gc: 1, t2_away_form_gs: 0, t2_away_form_gc: 1, t1_home_h2h_gs: 66, t1_home_h2h_gc: 66, t1_away_h2h_gs: 66, t1_away_h2h_gc: 66, t2_home_h2h_gs: 66, t2_home_h2h_gc: 66, t2_away_h2h_gs: 66, t2_away_h2h_gc: 66, llm_explanation: null },
    ];
*/