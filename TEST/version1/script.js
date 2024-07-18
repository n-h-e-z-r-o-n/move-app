// -----------------------------Slide Show Function ------------------------------------------------------------
var element = document.getElementById("trending_container");

function start_slider(){
 jQuery(document).ready(function ($) {
         $(".slider-img").on("click", function () {
           if ($(this).hasClass("active")) {
             const redirectUrl = this.dataset.redirectUrl;
             //console.log(redirectUrl);
             window.location.href = "watch_page.html?id=" + redirectUrl + "&type=movie";
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
  }
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
          const movieList = movieLists[i];
          const computedStyle = window.getComputedStyle(movieList);
          const transformValue = computedStyle.getPropertyValue("transform");
          const currentTranslateX = parseInt(transformValue.split(",")[4]) || 0;

          if (itemNumber - (4 + clickCounter) + (4 - ratio) >= 0) {
            movieList.style.transform = `translateX(${currentTranslateX - 300}px)`;
          } else {
            movieList.style.transform = "translateX(0)";
            clickCounter = 0;
          }
        };

        arrow.addEventListener("click", clickNext);
        setInterval(clickNext, 3000);   // Auto-click the next arrow after 3 seconds
      });
    }




//======================================= movie fetch --code block===================================================


const Movies_API_URL =   "https://api.themoviedb.org/3/discover/movie?&api_key=6bfaa39b0a3a25275c765dcaddc7dae7";
const TVs_API_URL =   "https://api.themoviedb.org/3/discover/tv?primary_release_year=2024&api_key=6bfaa39b0a3a25275c765dcaddc7dae7";
const Trending_API_URL =   "https://api.themoviedb.org/3/trending/all/day?primary_release_year=2024&api_key=af9b2e27c1a6bc3233af1832f4acc850";

const IMG_PATH = "https://image.tmdb.org/t/p/w1280";
const SEARCH_MOVIE_API = "https://api.themoviedb.org/3/search/movie?api_key=6bfaa39b0a3a25275c765dcaddc7dae7&query=";
const SEARCH_TV_API = "https://api.themoviedb.org/3/search/tv?api_key=6bfaa39b0a3a25275c765dcaddc7dae7&query=";

const Slider_div = document.getElementById("sliderUl");
const movie_div = document.getElementById("movieUl");
const series_div = document.getElementById("seriesUl");
const Trending_div = document.getElementById("TrendingUl");



const form = document.getElementById("searchForm");
const search = document.getElementById("search_input");


if (movie_div) {
    trendingShows(Trending_API_URL)
    Latest_Movies(2);
    Slider_Movies(Movies_API_URL); // initial Movies
    Latest_shows(2);
    //getTV(TVs_API_URL); // initial Movies
}

//SLIDER_ function --------------------------------------------------------------------------------

async function Slider_Movies(url) {
  const res = await fetch(url);
  const data = await res.json();
  Slider_Display(data.results);
}

function Slider_Display(movies) {
  Slider_div.innerHTML = "";
  let count = 1
  let start = 0;
  movies.forEach((movie) => {
    if (count < 10){
          const { title, backdrop_path, poster_path, id, vote_average, overview, release_date } = movie;
          const movieItem = document.createElement("div");
          movieItem.classList.add("slider-img");
          movieItem.innerHTML = `
                <img src="${IMG_PATH + backdrop_path}" />
                <div class="details">
                  <h2 class="details_h2">${title}</h2>
                  <p class="details_p">&#9733; ${vote_average}</p>
                </div>
          `;
          movieItem.dataset.redirectUrl = `${id}`;
          Slider_div.appendChild(movieItem);
          start = movieItem;
          count++;
    }
  });
  start_slider();
  start.classList.add("active");

}


// SHOW MOVIES  SECTION --------------------------------------------------------


function showMovies(movies) {
  movie_div.innerHTML = "";
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
               <div style="color: gray;"> &starf; &starf; &#9734;  ${vote_average}</div>
            </div>

    `;

    // Add event listener to open another page when clicked
    movieItem.addEventListener("click", () => {
         window.location.href = "watch_page.html?id=" + id + "&type=movie";
       });

    movie_div.appendChild(movieItem);
  });
}


// SHOW TV SECTION -----------------------------------------------------------------------
async function getTV(url) {
  const res = await fetch(url);
  const data = await res.json();
  showTV(data.results);
}

function showTV(movies) {
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
               <div style="color: gray;"> &starf; &starf; &#9734;   ${vote_average}</div>
            </div>

    `;

    // Add event listener to open another page when clicked
    movieItem.addEventListener("click", () => {
         window.location.href = "watch_page.html?id=" + id + "&type=tv";
       });
    series_div.appendChild(movieItem);
  });
}

// SHOW TRENDING SECTION --------------------------------------------------------
async function trendingShows(url) {
  const res = await fetch(url);
  const data = await res.json();
  showsTrending(data.results);
}



function showsTrending(movies) {
  Trending_div.innerHTML = "";
  movies.forEach((movie) => {
    const { id, media_type, original_title, original_name, poster_path, vote_average, overview, first_air_date } = movie;
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
                  <button class="movie-list-item-button" onclick="redirect_function(${id}, '${media_type}')">Watch</button>
                  <div class="movie-list-item-title"> ${title}</div>
    `;

    Trending_div.appendChild(movieItem);
  });
   AutoScroll_TRENDING();
}

function redirect_function(id, media_type) {
  console.log("watch clicker", id, media_type);
  window.location.href = "watch_page.html?id=" + id + `&type=${media_type}`;
}


async function Latest_Movies(page) {
  let count = 1;

  let data_json = [];
    console.log();
    while (count <= page) {

      let res = await fetch(`https://vidsrc.to/vapi/movie/new/${count}`);
      let data = await res.json();

      data_json = data_json.concat(data['result']['items']) ;
      count++;
    }

  let hold = [];
  for (let i = 0; i < data_json.length; i++) {
    let res2 = await fetch(`https://api.themoviedb.org/3/movie/${data_json[i]['tmdb_id']}&?api_key=6bfaa39b0a3a25275c765dcaddc7dae7`);
    let data2 = await res2.json();
    hold.push({poster_path:data2['poster_path'], release_date:data2['release_date'], vote_average:data2['vote_average'], title:data2['title'], id:data2['id']});
  }
  showMovies(hold);
}


async function Latest_shows(page) {
  let count = 1;

  let data_json = [];
  let id_prev = 0;

  while (count <= page) {
      let res = await fetch(`https://vidsrc.to/vapi/episode/latest/${count}`);
      let data = await res.json();
      if(Array.isArray(data['result']['items'])){
        data_json = data_json.concat(data['result']['items']) ;
        count++;
      }else{
        itemValues = Object.values(data.result.items);
        data_json = data_json.concat(itemValues) ;
        count++;
      }
    }
  let hold = [];
  for (let i = 0; i < data_json.length; i++) {
      try{
          let res2 = await fetch(`https://api.themoviedb.org/3/tv/${data_json[i]['tmdb_id']}&?api_key=6bfaa39b0a3a25275c765dcaddc7dae7`);
          let data2 = await res2.json();
          if(`${data2['poster_path']}` !== `undefined`){
            if (id_prev !==data2['id']){
              hold.push({poster_path:data2['poster_path'], first_air_date:data2['first_air_date'], vote_average:data2['vote_average'], original_name:data2['original_name'], id:data2['id']});
              id_prev = data2['id'];
            }
          }
        }finally{continue;}
  }
  showTV(hold);
}


//========================================================================================
//========================================================================================

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
                     <div style="color: gray;"> &starf; &starf; &#9734;   ${vote_average}</div>
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

//
//  ----------------------------------------------------------------------------
