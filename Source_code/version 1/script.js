// -----------------------------Slide Show Function ------------------------------------------------------------
 jQuery(document).ready(function ($) {
         $(".slider-img").on("click", function () {
           if ($(this).hasClass("active")) {
             window.location.href = "./watch_page.html"; // Replace with the URL of the desired HTML page
           } else {
             $(".slider-img").removeClass("active");
             $(this).addClass("active");
           }
         });
       });

  jQuery(document).ready(function ($) {
        let currentIndex = 0;
        const images = $(".slider-img");
        const imageCount = images.length;

        function showNextImage() {
            images.removeClass("active");
            currentIndex = (currentIndex + 1) % imageCount;
            images.eq(currentIndex).addClass("active");
        }

        // Automatically change the image every 3 seconds
        setInterval(showNextImage, 5000);

        // Add click event to redirect when an active image is clicked

    });
    // ------------------------------------------------------------------------------------------

function AutoScroll_TRENDING() {
const arrows = document.querySelectorAll(".arrow");
const movieLists = document.querySelectorAll(".movie-list");

arrows.forEach((arrow, i) => {
  const itemNumber = movieLists[i].querySelectorAll("img").length;
  let clickCounter = 0;

  const clickNext = () => {
    const ratio = Math.floor(window.innerWidth / 270);
    clickCounter++;
    if (itemNumber - (4 + clickCounter) + (4 - ratio) >= 0) {
      const currentTranslateX = movieLists[i].computedStyleMap().get("transform")[0].x.value;
      movieLists[i].style.transform = `translateX(${currentTranslateX - 300}px)`;
    } else {
      movieLists[i].style.transform = "translateX(0)";
      clickCounter = 0;
    }
  };

  arrow.addEventListener("click", clickNext);

  console.log(Math.floor(window.innerWidth / 270));

  // Auto-click the next arrow after 2 seconds
  setInterval(clickNext, 2000);
});
}




//--------------- movie fetch --code block-----------------------------------------------


const Movies_API_URL =   "https://api.themoviedb.org/3/discover/movie?&api_key=6bfaa39b0a3a25275c765dcaddc7dae7";
const TVs_API_URL =   "https://api.themoviedb.org/3/discover/tv?&api_key=6bfaa39b0a3a25275c765dcaddc7dae7";
const Trending_API_URL =   "https://api.themoviedb.org/3/trending/all/day?api_key=af9b2e27c1a6bc3233af1832f4acc850";

const IMG_PATH = "https://image.tmdb.org/t/p/w1280";
const SEARCH_MOVIE_API = "https://api.themoviedb.org/3/search/movie?api_key=6bfaa39b0a3a25275c765dcaddc7dae7&query=";
const SEARCH_TV_API = "https://api.themoviedb.org/3/search/tv?api_key=6bfaa39b0a3a25275c765dcaddc7dae7&query=";

const ul = document.getElementById("movieUl");
const series_div = document.getElementById("seriesUl");
const Trending_div = document.getElementById("TrendingUl");



const form = document.getElementById("searchForm");
const search = document.getElementById("search_input");


if (ul) {
    getMovies(Movies_API_URL); // initial Movies
    getTV(TVs_API_URL); // initial Movies
    trendingShows(Trending_API_URL)
}






// SHOW MOVIES  SECTION
async function getMovies(url) {
  const res = await fetch(url);
  const data = await res.json();
  showMovies(data.results);
}

function showMovies(movies) {
  console.log(movies);
  ul.innerHTML = "";
  movies.forEach((movie) => {
    const { title, poster_path, id, vote_average, overview, release_date } = movie;
    const movieItem = document.createElement("div");
    movieItem.classList.add("box");
    movieItem.innerHTML = `
        <!-- box-1  -->

            <div class="box-img">
                <img src="${IMG_PATH + poster_path}"  alt="">
            </div>
            <h3>${title}</h3>
            <div class="container_span">
               <div style="color: gray;">${release_date}</div>
               <div style="color: gray;"> ${"★"} ${vote_average}</div>
            </div>

    `;

    // Add event listener to open another page when clicked
    movieItem.addEventListener("click", () => {
         window.location.href = "watch_page.html?id=" + id + "&type=movie";
       });

    ul.appendChild(movieItem);
  });
}


// SHOW TV SECTION
async function getTV(url) {
  const res = await fetch(url);
  const data = await res.json();
  showTV(data.results);
}

function showTV(movies) {
  console.log(movies);
  series_div.innerHTML = "";
  movies.forEach((movie) => {
    const {id, original_name, poster_path, vote_average, overview, first_air_date } = movie;
    const movieItem = document.createElement("div");
    movieItem.classList.add("box");
    movieItem.innerHTML = `
        <!-- box-1  -->

            <div class="box-img">
                <img src="${IMG_PATH + poster_path}"  alt="">
            </div>
            <h3>${original_name}</h3>
            <div class="container_span">
               <div style="color: gray;">${first_air_date}</div>
               <div style="color: gray;"> ${" \t\t\t ★"} ${vote_average}</div>
            </div>

    `;

    // Add event listener to open another page when clicked
    movieItem.addEventListener("click", () => {
         window.location.href = "watch_page.html?id=" + id + "&type=tv";
       });
    series_div.appendChild(movieItem);
  });
}

// SHOW TRENDING SECTION
async function trendingShows(url) {
  const res = await fetch(url);
  const data = await res.json();
  showsTrending(data.results);
}



function showsTrending(movies) {
  console.log(movies);
  Trending_div.innerHTML = "";
  movies.forEach((movie) => {
    const { original_title, original_name, poster_path, vote_average, overview, first_air_date } = movie;
    let title;

    if (original_title=== undefined) {
       title = original_name;

    } else {
       title = original_title;
    }
    const movieItem = document.createElement("div");
    movieItem.classList.add("movie-list-item");
    movieItem.innerHTML = `

                  <img class="movie-list-item-img" src="${IMG_PATH + poster_path}" alt="">
                  <button class="movie-list-item-button">Watch</button>
                  <div class="movie-list-item-title"> ${title}</div>


    `;
    Trending_div.appendChild(movieItem);
  });

   AutoScroll_TRENDING();
}



function Search_Results_SHOW(movies) {
  console.log(movies);
  search_R_div.innerHTML = "";
  movies.forEach((movie) => {
    const { original_title, original_name, poster_path, vote_average, overview, first_air_date } = movie;
    let title;

    if (original_title=== undefined) {
       title = original_name;

    } else {
       title = original_title;
    }
    const movieItem = document.createElement("div");
    movieItem.classList.add("movie-list-item");
    movieItem.innerHTML = `

              <!-- box-1  -->

                  <div class="box-img">
                      <img src="${IMG_PATH + poster_path}"  alt="">
                  </div>
                  <h3>${title}</h3>
                  <div class="container_span">
                     <div style="color: gray;">${first_air_date}</div>
                     <div style="color: gray;"> ${" \t\t\t ★"} ${vote_average}</div>
                  </div>


    `;
    search_R_div.appendChild(movieItem);
  });
}
// FOR SEARCH SUBMIT





form.addEventListener("submit", (e) => {
  e.preventDefault();
  const searchTerm = search.value;
  if (searchTerm && searchTerm !== "") {

    search.value = "";
    window.location.href = "S_Results.html?query=" + searchTerm; // Replace with the URL of the page you want to open
  } else {

  }
});
